define([
    'backbone',
    'views/base_view',
    'views/input_view',
    'views/editable-text',
    'views/editable/date',
    'views/editable/select',
    'views/generic/list',
    'views/activity/budgetline',
    'views/activity/taline',
    'views/display-number',
    'views/activity/statuscontainer',
], function (
    Backbone, BaseView, Editable, EditableText, EditableDate,
    Selectable, ListView, BudgetLineView, TALineView, displayNumber,
    StatusContainerView) {

    var ActivityContainer = BaseView.extend({
        tagName: "div",
        className: "activity-item",
        template_selector: "#activity-container",

        events: {
            "click .show-full-ui .overview-minmax .toggle-triangle": "toggleDetails",
            "click .status-minmax .toggle-triangle": "toggleStatus"
        },

        toggleDetails: function (e) {
            this.$(e.target).parents("table")
                            .find(".activity-details")
                            .add(e.target) // Change also on toggle
                            .toggleClass("show");
            e.stopPropagation();
        },

        toggleStatus: function (e) {
            this.$(e.target).parents('li')
                            .toggleClass('hide-status-history');
        },

        showFullUI: function () {
            var id = this.model.get('id');
            if (id) {
                this.$("table").addClass("show-full-ui");
            }
        },

        updateTotal: function (collection, total_selector) {
            var total = 0;
            collection.each(function (el) {
                var value = el.get("amount");
                total += value ? parseFloat(value) : 0;
            });
            this.$(total_selector).html(displayNumber(total.toString()));
        },

        updateNonTATotal: function () {
            this.updateTotal(this.model.budgetlines, ".budget-lines-total");
        },

        updateTATotal: function () {
            this.updateTotal(this.model.talines, ".ta-lines-total");
        },

        // Init
        initialize: function () {
            var model_id = this.model.get("id");
            this.model.talines = Aptivate.logframe.talines.subcollection({
                filter: function (taline) {
                    return taline.get("activity") === model_id;
                }
            });
            this.model.budgetlines = Aptivate.logframe.budgetlines.subcollection({
                filter: function (budgetline) {
                    return budgetline.get("activity") === model_id;
                }
            });
            this.model.statusupdates = Aptivate.logframe.statusupdates.subcollection({
                filter: function (statusUpdate) {
                    return statusUpdate.get("activity") === model_id;
                }
            });
            Backbone.Subviews.add(this);
            this.listenTo(this.model, "sync", this.showFullUI);
            this.listenTo(this.model.budgetlines, "add change sync", this.updateNonTATotal);
            this.listenTo(this.model.talines, "add change sync", this.updateTATotal);

            // Re-render on lead change
            this.listenTo(this.model, "change:lead", this.renderOpenDetails);
        },

        onSubviewsRendered: function () {
            this.updateNonTATotal();
            this.updateTATotal();
        },

        renderOpenDetails: function () {
            this.render();
            this.$(".activity-details").addClass("show");
        },

        subviewCreators: {
            activityName: function () {
                return new Editable({
                    model: this.model,
                    template_selector: "#editable-title",
                    attributes: { class: "ribbon ribbon-result" },
                });
            },
            activityStartDate: function () {
                return new EditableDate({
                    model: this.model,
                    field_name: 'start_date',
                });
            },
            activityEndDate: function () {
                return new EditableDate({
                    model: this.model,
                    field_name: 'end_date',
                });
            },
            activityDescription: function () {
                return new EditableText({
                    model: this.model,
                    template_selector: "#editable-description"
                });
            },
            activityDeliverables: function () {
                return new EditableText({
                    model: this.model,
                    template_selector: "#editable-deliverables"
                });
            },
            activityLead: function () {
                return new Selectable({
                    model: this.model,
                    field_name: 'lead',
                    options: Aptivate.data.users,
                    options_map: {
                        value: "id",
                        text: "name"
                    },
                    template_selector: "#editable-field"
                });
            },
            activityStatusUpdates: function () {
                return new StatusContainerView({
                    model: this.model,
                });
            },
            activityTALines: function () {
                return new ListView({
                    tagName: "table",
                    className: "ta-lines-table",
                    collection: this.model.talines,
                    newModelOptions: { activity: this.model.get('id') },
                    itemView: TALineView
                });
            },
            activityBudgetLines: function () {
                return new ListView({
                    tagName: "table",
                    className: "budget-lines-table",
                    collection: this.model.budgetlines,
                    newModelOptions: { activity: this.model.get('id') },
                    itemView: BudgetLineView
                });
            }
        }
    });

    return ActivityContainer;
});
