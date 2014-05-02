define([
    'underscore',
    'backbone',
    'views/editable/feedback-mixin',
], function (_, Backbone, FeedbackMixin) {

    var EditableField = Backbone.View.extend(FeedbackMixin).extend({

        events: {
            "click .editable": "changeElement",
            "blur .savable":  "commitEdit",
            "keyup .savable": "cancelOnEscape",
            "keypress .savable": "updateOnEnter",
        },

        // Class to add when displaying placeholder text for  missing vlaues
        // Can be a strig or a function that returns the class name
        missingClass: 'missing',

        // Class to add to show el is editable
        editableClass: 'editable',

        // Class to add to the input element
        inputClass: 'editable-input',

        // what sort of input am ?
        // e.g. to use a textarea, set inputTagName = 'textarea' and 
        // valueAttributeName = 'text'
        inputTagName: 'input',

        // which attribute to use for the editable value
        valueAttributeName: 'value',

        // Text to display when there is no value in the model
        // Can be a strig or a function that returns the class name
        placeholderText: function () {
            return this.options.placeholderText || "Click to add";
        },

        constructor: function (options) {
            Backbone.View.apply(this, arguments);
            this.options = options;
            this.editing = false;
        },

        // Prepare the value to be displayed
        displayValue: function(value) {
            return value;
        },

        // retrn the 'savable' value from the input element
        getElementValue: function (el) {
            return el.value;
        },

        render: function () {
            if (this.editing){
                this.renderInput();
            } else {
                this.renderDisplay();
            }
        },

        renderDisplay: function () {
            this.$el.replaceWith(this.el);
            var name = this.options.fieldName,
                value = this.model.get(name);
            if (value) {
                this.$el.html(this.displayValue(value));
            } else {
                this.$el.html(_.result(this, 'placeholderText'));
                this.$el.addClass(_.result(this, 'missingClass'));
            }
            this.$el.addClass(_.result(this, 'editableClass'));
            this.$el.data('name', this.options.fieldName);
            return this;
        },

        renderInput: function () {
            if (!this.inputEl) {
                this.inputEl = $('<' + this.inputTagName + '>')
                    .attr('name', this.options.fieldName);
            }
            this.inputEl
                .attr(this.valueAttributeName,
                      this.model.get(this.options.fieldName))
                .addClass('savable')
                .replaceAll(this.$el)
                .focus();
            this.postChangeElement && this.postChangeElement(this.inputEl);
        },


        // Listeners
        changeElement: function () {
            this.editing = true;
            this.render();
        },

        cancelOnEscape: function (e) {
            if (e.keyCode === 27) { // Escape
                this.$(e.target).removeClass('savable');
                this.editing = false;
                this.render();
            }
        },

        updateOnEnter: function (e) {
            if (e.which === 13) { // Enter
                this.commitEdit(e);
            }
        },

        commitEdit: function (e) {
            var element = e.target;
            this.model.set(element.name, this.getElementValue(element));
            this.model.save();
            // Avoid duplicate saves
            this.$(e.target).removeClass('savable');
            this.render();
        },

        initialize: function () {
            this.attachFeedback(); // Comes from FeedbackMixin
        }

    });

    // When creating as a Backbone.Subview, use this function and pass the
    // placeholder element as a 'placeholder' option, plus other view options
    // (e.g. 'model').  Values from the placeholder override these options
    // which, in turn, override any defaults.  e.g.:
    //
    //    subviewCreators: {
    //        'editableField': function (placeholder) {
    //            return EditableField.creator({
    //                placeholder: placeholder
    //                model: this.model,
    //            });
    //        }
    //    },
    EditableField.creator = function (options) {
        var placeholder = options.placeholder,
            viewOptions = _.extend({}, options, {
                tagName: placeholder.prop('tagName'),
                className: placeholder.attr('class'),
                id: placeholder.attr('id'),
                fieldName: placeholder.data('fieldname'),
                placeholderText: placeholder.text(),
            });
        return new EditableField(viewOptions);
    };

    return EditableField;

});
