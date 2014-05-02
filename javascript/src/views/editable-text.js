define([
    'underscore',
    'jquery',
    'views/input_view',
    'pen',
], function (_, $, Editable, Pen) {
    var EditableText = Editable.extend({

        //TODO: There is almost certainly a better way to arrange
        //the hierarchy of Editabletext and Inputview so I don't have
        //to remove events here. But its home time on Friday.
        events: {
            "click .editable": "changeElement",
            "change .savable":  "commitEdit",
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
                class: "editable-textarea"
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

        postChangeElement: function () {
            var self = this;
            $(document).on("click", ".pen-menu, .pen-editor", function (e) {
                e.stopPropagation();
            }).on("click", ".body", function (e) {
                // Need to fix target first to point at editor
                // (if editor wasn't handled by blur listener)
                var $el = $(".editable-textarea");
                if ($el.length) {
                    e.target = $el[0];
                    self.commitEdit.call(self, e);
                }
                e.stopPropagation();
            });
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
