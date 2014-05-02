define([
    'views/base_view',
    'views/input_view',
    'views/editable-text',
    'views/indicator/milestone-table',
], function (BaseView, Editable, EditableText, MilestoneTableView) {

    var IndicatorView = BaseView.extend({

        tagName: 'div',
        template_selector: '#indicator-container',

        initialize: function () {
            Backbone.Subviews.add(this);
        },

        subviewCreators: {
            indicatorName: function () {
                return new Editable({
                    model: this.model,
                    template_selector: "#editable-title",
                    attributes: { class: "ribbon ribbon-indicator" }
                });
            },
            indicatorDescription: function () {
                return new EditableText({
                    model: this.model,
                    attributes: { class: "inner" },
                    template_selector: "#editable-description",
                });
            },
            indicatorSource: function () {
                return new EditableText({
                    model: this.model,
                    template_selector: "#indicator-source"
                });
            },
            targetsTable: function () {
                return new MilestoneTableView({
                    model: this.model,
                });
            },
        },

    });
    return IndicatorView;

});
