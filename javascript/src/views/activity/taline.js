define([
    'views/base_view',
    'views/editable/input',
    'views/editable/date',
    'views/editable/select',
    'views/editable/number',
], function (BaseView, EditableInput, EditableDate, Selectable, EditableNumber) {
    var BudgetLineView = BaseView.extend({
        tagName: "tr",
        template_selector: "#activity-taline",

        initialize: function () {
            Backbone.Subviews.add(this);
        },

        subviewCreators: {
            "taType": function () {
                return new Selectable({
                    model: this.model,
                    field_name: 'type',
                    options: Aptivate.data.tatypes,
                });
            },
            "taName": function () {
                return new EditableInput({
                    field_name: 'name',
                    model: this.model,
                });
            },
            "taBand": function () {
                return new Selectable({
                    model: this.model,
                    field_name: 'band',
                    options: [
                        {id: 'low'},
                        {id: 'medium'},
                        {id: 'high'}
                    ],
                    options_map: {
                        value: 'id',
                        text:  'id'
                    },
                });
            },
            "taStart": function () {
                return new EditableDate({
                    model: this.model,
                    field_name: 'start_date',
                });
            },
            "taEnd": function () {
                return new EditableDate({
                    model: this.model,
                    field_name: 'end_date',
                });
            },
            "taDays": function () {
                return new EditableInput({
                    field_name: 'no_days',
                    model: this.model,
                });
            },
            "taAmount": function (){
                return new EditableNumber({
                    field_name: 'amount',
                    model: this.model,
                });
            }
        }
    });

    return BudgetLineView;
});
