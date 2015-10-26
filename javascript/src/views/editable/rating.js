define([
    'jquery',
    'underscore',
    'backbone',
    'views/input_view',
], function ($, _, Backbone, Editable) {
    /***************************************
     * Rating picker
     ***************************************/
    var RatingDialog = Backbone.View.extend({
        events: {
            "click .rating-item":  "commitEdit",
            "keyup .editable-rag": "remove",
        },

        createRatingElement: function (choice, selected) {
            var cls = choice.color,
                $el = $("<div>", {
                    class: "rating-item clearfix",
                    name: "rating",
                    "data-value": choice.id
                    });

            if (choice.id === selected) {
                cls += " selected";
            }
            $("<div>", {
                class: "rating-value " + cls,
                title: choice.name,
                name: "rating",
                "data-value": choice.id,
                text: " "
            }).appendTo($el);
            $("<div>", {
                class: "rating-label",
                name: "rating",
                "data-value": choice.id,
                text: choice.name
            }).appendTo($el);

            return $el;
        },

        inputElement: function () {
            var sel = $('<div>', {
                    class: "editable-rag"
                }),
                selected = this.model.get("rating") || 0,
                choices = this.options.options || [],
                self = this;

            $.each(choices, function (i, choice) {
                var $el = self.createRatingElement(choice, selected);
                $el.appendTo(sel);
            });
            return sel;
        },

        commitEdit: function (e) {
            this.options.parent.commitEdit(e);
            this.remove();
        },

        attachHandlers: function ($el) {
            $el.on("click", ".rating-item", $.proxy(this.commitEdit, this))
               .on("keyup", ".editable-rag", $.proxy(this.remove, this));
        },

        positionDialog: function ($el) {
            var parent = this.options.parent,
                offset = parent.$el.offset();

            $el.css({
                left: offset.left + "px",
                top: (offset.top - 40) + "px"
            });
        },

        constructor: function (options) {
            Backbone.View.apply(this, arguments);
            this.options = options;
        },

        initialize: function () {
            var self = this;

            // Replacement for blur to recognize when user starts using
            // a different part of the interface or cancel with Esc
            $("body").on("click", function () {
                self.remove();
            }).on("keyup", function (e) {
                if (e.keyCode === 27) { // Escape
                    self.remove();
                }
            });
        },

        render: function () {
            this.$el = this.inputElement();
            this.attachHandlers(this.$el);
            this.positionDialog(this.$el);
        }
    }),

    /***************************************
     * Rating editable
     ***************************************/
    Rating = Editable.extend({
        className: "result-rating",
        template_selector: "#editable-rating",

        events: {
            "click .editable": "switchElement",
            "blur .editable":  "commitEdit",
        },

        getElementValue: function (el) {
            return $(el).data("value") || "";
        },

        preRender: function () {
            // Remove rating dialog
            this.dialogView.remove();
        },

        switchElement: function (e) {
            // Needed so that click handler on body is not triggered when
            // clicking inside of the rating interface
                e.stopPropagation();
            this.changeElement(e);
        },

        changeElement: function () {
            this.dialogView = new RatingDialog({
                parent: this,
                options: this.options.options,
                model: this.model
            });
            this.dialogView.render();
            $("body").append(this.dialogView.$el);
        },

        getTemplateData: function (data) {
            var rating_id = data.rating || 0,
                rating, new_data = data;
            if (rating_id) {
                rating = _.find(this.options.options, function (option) {
                    return option.id === rating_id;
                });
                if (rating) {
                    new_data = rating;
                }
            }
            return new_data;
        },

        // Process Rating values as Integers (so values match those returned by API).
        commitEdit: function (e) {
            var element = e.target,
                name = element.getAttribute("name"),
                old_value = this.model.get(name) || "",  // Cast undefined to ""
                value = parseInt(this.getElementValue(element), 10);

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

    return Rating;
});
