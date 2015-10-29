define([
    'underscore',
    'jquery',
    'views/input_view',
    'pen',
], function (_, $, Editable, Pen) {
    var EditableText = Editable.extend({

        events: {
            "click .editable": "openEditor",
            "change .savable":  "commitEdit",
            "click .savable.close-now":  "commitEdit",
            "blur .savable": "conditionalCommit",
            "keyup .savable": "cancelOnEscape",
        },

        conditionalCommit: function (e) {
            var menuOn = !!this.editor.menuOn;
            if (!menuOn) {
                this.commitEdit(e);
                e.stopPropagation();
            }
        },

        preRender: function () {
            $(".pen-editor-menu").remove();

            // Remove handlers
            $(".body").off("click");
        },

        inputElement: function (name, value) {
            var $el = $('<div>', {
                name: name,
                // cid used for distinguishing instances
                class: "editable-textarea " + this.cid
            }).html(value);
            this.editor = new Pen({
                editor: $el[0],
                stay: false,
                class: "pen-editor",
                list: ['bold', 'italic', 'createlink'],
                textarea: '<textarea name="' + name + '"></textarea>'
            });
            return $el;
        },

        openEditor: function (e) {
            // First close any open editor before opening this one
            $(".savable").addClass("close-now").each(function (i, el) {
                el.click();
            });
            // Remove old handlers, if there are any
            $(document).off("click.editableText", ".body");

            this.changeElement(e);
        },

        postChangeElement: function () {
            function bodyHandler(e) {
                // Need to fix target first to point at editor
                // (if editor wasn't handled by blur listener)
                // Make sure you select the right one if more are opened
                var $el = $(".editable-textarea." + self.cid);
                if ($el.length) {
                    e.target = $el[0];
                    self.commitEdit.call(self, e);
                }
                e.stopPropagation();
            }

            var self = this;
            $(document).on("click", ".pen-menu, .pen-editor", function (e) {
                e.stopPropagation();
            }).on("click.editableText", ".body", bodyHandler);
        },

        getElementValue: function (el) {
            var tag = el.tagName ? el.tagName.toLowerCase() : "";
            return tag === "textarea" ? el.value : el.innerHTML;
        },

        initialize: function () {
            this.attachFeedback(); // Comes from FeedbackMixin
        }

    });
    return EditableText;

});
