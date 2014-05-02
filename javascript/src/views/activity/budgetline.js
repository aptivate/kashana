define([
    'views/base_view',
    'views/editable/input',
    'views/editable/number',
], function (BaseView, EditableInput, EditableNumber) {
    var BudgetLineView = BaseView.extend({
        tagName: "tr",
        template_selector: "#activity-budgetline",

        // Init
        initialize: function () {
            Backbone.Subviews.add(this);
        },

        subviewCreators: {
            "blName": function () {
                return new EditableInput({
                    field_name: 'name',
                    model: this.model,
                });
            },
            "blAmount": function () {
                return new EditableNumber({
                    field_name: 'amount',
                    model: this.model,
                });
            }
        }
    });

    return BudgetLineView;
});
