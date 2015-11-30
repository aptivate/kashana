define([
    'underscore',
    'backbone',
    'jquery',
    'views/editable/field',
    'backbone_subviews',
], function (_, BB, $, EditableField) {
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

    describe("Editable View Tests", function() {
    	it("Render normal value", function () {
            var view = new View({model: model}).render(),
                el = view.$el.children().first();
            
            since("Content is Model's name attribute");
            expect(el.text()).toEqual(data.name);
            
            since("Non-default (div) tagName from Placeholder");
            expect(el.prop('tagName').toLowerCase()).toEqual('span');
            
            since("Id is #foo");
            expect(el.attr('id')).toEqual('foo');
            
            since("Has bar class");
            expect(el.hasClass('bar')).toEqual(true);
            
            since("Has bas class")
            expect(el.hasClass('bas')).toEqual(true);
            
            since("Does not have missing class");
            expect(el.hasClass(EditableField.prototype.missingClass)).toEqual(false);
            
            since("Has editable class");
            expect(el.hasClass(EditableField.prototype.editableClass)).toEqual(true);
            
            since("field name is 'name'");
            expect(el.data('name')).toEqual('name');
    	});

    	it("Render normal unsaved view", function () {
            var model = new BB.Model({name: ""}),
                view = new View({model: model}).render(),
                el = view.$el.children().first();
            
            since("Content is placeholder text");
            expect(el.text()).toEqual(placeholderText);
            
            since("Non-default (div) tagName from Placeholder");
            expect(el.prop('tagName').toLowerCase()).toEqual('span');
            
            since("Id is #foo");
            expect(el.attr('id')).toEqual('foo');
            
            since("Has bar class");
            expect(el.hasClass('bar')).toEqual(true);
            
            since("Has bas class")
            expect(el.hasClass('bas')).toEqual(true);
            
            since("Has missing class");
            expect(el.hasClass(EditableField.prototype.missingClass)).toEqual(true);
            
            since("Has editable class");
            expect(el.hasClass(EditableField.prototype.editableClass)).toEqual(true);
            
            since("field name is 'name'");
            expect(el.data('name')).toEqual('name');
        });

        it("Input element ", function () {
            var view = new View({model: model}).render();
            editableViewInstance.editing = true;
            editableViewInstance.render();
            el = view.$el.children().first();
            expect(el.val()).toEqual(data.name);
            since("Has savable class");
            expect(el.hasClass('savable')).toEqual(true);
        });
    });

});
