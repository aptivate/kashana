define([
    'underscore',
    'backbone',
    'jquery',
    'views/editable/field',
    'backbone_subviews',
], function (_, BB, $, EditableField) {
    var runtests = function () {
        var editableViewInstance,
            data = {name: "abc"},
            model = new BB.Model(data),
            placeholderText = 'Special Placeholder',
            View = BB.View.extend({
                initialize: function () {
                    Backbone.Subviews.add(this);
                },
                render: function () {
                    this.$el.html(
                        '<span id="foo" class="bar bas" ' +
                        'data-fieldname="name" data-subview="editableName">' +
                        placeholderText +
                        '</span>');
                    return this;
                },
                subviewCreators: {
                    'editableName': function (placeholder) {
                        editableViewInstance = EditableField.creator({
                                model: this.model,
                                placeholder: placeholder
                            });
                        return editableViewInstance;
                    }
                },
            });

        test("Render normal value", function () {
            var view = new View({model: model}).render(),
                el = view.$el.children().first();
            equal(el.text(), data.name,
                "Content is Model's name attribute");
            equal(el.prop('tagName').toLowerCase(), 'span',
                "Non-default (div) tagName from Placeholder");
            equal(el.attr('id'), 'foo',
                "Id is #foo");
            ok(el.hasClass('bar'), "Has bar class");
            ok(el.hasClass('bas'), "Has bas class");
            ok(!el.hasClass(EditableField.prototype.missingClass),
                "Does not have missing class");
            ok(el.hasClass(EditableField.prototype.editableClass),
                "Has editable class");
            equal(el.data('name'), 'name',
                "field name is 'name'");
        });

        test("Render normal unsaved view", function () {
            var model = new BB.Model({name: ""}),
                view = new View({model: model}).render(),
                el = view.$el.children().first();
            equal(el.text(), placeholderText,
                "Content is placeholder text");
            equal(el.prop('tagName').toLowerCase(), 'span',
                "Non-default (div) tagName from Placeholder");
            equal(el.attr('id'), 'foo',
                "Id is #foo");
            ok(el.hasClass('bar'), "Has bar class");
            ok(el.hasClass('bas'), "Has bas class");
            ok(el.hasClass(EditableField.prototype.missingClass),
                "Has missing class");
            ok(el.hasClass(EditableField.prototype.editableClass),
                "Has editable class");
            equal(el.data('name'), 'name',
                "field name is 'name'");
        });

        test("Input element ", function () {
            var view = new View({model: model}).render();
            editableViewInstance.editing = true;
            editableViewInstance.render();
            el = view.$el.children().first();
            equal(el.val(), data.name);
            ok(el.hasClass('savable'),
                "Has savable class");
        });
    };

    return runtests;

});
