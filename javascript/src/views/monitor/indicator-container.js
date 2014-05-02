define([
    'backbone',
    'views/base_view',
    'views/generic/template-list',
    'views/monitor/header-row',
    'views/monitor/subindicator-rows',
    'views/monitor/column-heading',
    'views/monitor/data-entry-row'
], function (
    Backbone,
    BaseView,
    StaticListView,
    HeaderRowView,
    SubindicatorRowsView,
    ColumnHeadingView,
    DataEntryRowView
) {
    var IndicatorContainerView = BaseView.extend({
        tagName: 'div',
        className: 'monitor-indicator-table',
        template_selector: "#monitor-indicator-container",

        initialize: function () {
            Backbone.Subviews.add(this);
        },

        subviewCreators: {
            headerRow: function () {
                return new HeaderRowView({
                    // Modified ListView that also has a model
                    model: this.model,
                    itemView: ColumnHeadingView,
                    newModelOptions: { indicator: this.model.get('id') },
                    collection: this.model.columns,
                });
            },
            subindicatorRows: function () {
                return new StaticListView({
                    tagName: 'tbody',
                    collection: this.model.subindicators,
                    itemView: DataEntryRowView.extend({
                        indicator: this.model,
                        columns: this.model.columns,
                        actuals: this.model.actuals
                    })
                });
            }
        }

    });

    return IndicatorContainerView;
});
