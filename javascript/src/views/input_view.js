define([
    'jquery',
    'underscore',
    'views/base_view',
    'views/editable/feedback-mixin',
], function ($, _, BaseView, FeedbackMixin) {
    var InputView = BaseView.extend(FeedbackMixin).extend({

        events: {
            "click .editable": "changeElement",
            "blur .savable":  "commitEdit",
            "keyup .savable": "cancelOnEscape",
            "keypress .savable": "updateOnEnter",
        },

        // Returns jquery wrapped version of the input element
        inputElement: function (name, value) {
            return $('<input>', {
                value: value,
                name: name,
                class: "editable-input"
            });
        },

        // Override if you want to massage edit widget
        postChangeElement: function () {},  // param: $el

        // Override if you want to make changes after change/cancel,
        // but pre render
        preRender: function () {},  // param: event

        getElementValue: function (el) {
            return el.value;
        },

        // Listeners
        changeElement: function (e){
            var $t = $(e.target),
                $target = $t.hasClass("editable") ? $t : $t.parents(".editable"),
                name = $target.data('name'),
                value = this.model ? this.model.get(name) : "",
                $el;
            $el = this.inputElement(name, value)
                .addClass('savable')
                .replaceAll($target)
                .focus();
            this.postChangeElement && this.postChangeElement($el);
        },

        cancelOnEscape: function (e) {
            if (e.keyCode === 27) { // Escape
                this.$(e.target).removeClass('savable');
                this.preRender(e);
                this.render();
            }
        },

        updateOnEnter: function (e) {
            if (e.which === 13) { // Enter
                this.commitEdit(e);
            }
        },

        commitEdit: function (e) {
            var element = e.target,
                name = element.getAttribute("name"),
                old_value = this.model.get(name) || "",  // Cast undefined to ""
                value = this.getElementValue(element);

            // Save only if value is different
            if (old_value !== value) {
                this.model.set(name, value);
                this.saveFlag = true;
                this.model.save();
                // Avoid duplicate saves
                this.$(e.target).removeClass('savable');
            }
            this.preRender(e);
            this.render();
        },

        initialize: function () {
            this.attachFeedback(); // Comes from FeedbackMixin
        }
    });
    return InputView;
});
