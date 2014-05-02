define([
    'underscore',
    'views/editable/rating',
    'models/models',
    'models/collections',
    'views/generic/template-list',
    'views/monitor/header-row',
    'views/monitor/actual-container'
], function (_, EditableRating, models,
    collections, StaticListView, HeaderRowView, ActualContainer) {

    // View for a data-entry row in the Monitoring data-entry table
    // Subindicator in the first column, then baseline target then 
    // next indicator target, then the Actual values for the given 
    // subindicator.
    var DataEntryRow = StaticListView.extend({
        tagName: 'tr',
        template_selector: '#monitor-data-entry-row',
        unknownValue: '(unknown)',

        itemView: ActualContainer,

        // Expected options:
        // 'indicator' -- Indicator model
        // 'actuals' -- Actual value models (belonging to the indicator)
        // 'columns' -- the Columns belonging to the indicator
        // 'model' -- the subindicator
        initialize: function (options) {
            Backbone.Subviews.add(this);
            // we use extend so those previously set by extend should
            // not be overwritten?
            _.extend(this,
                _.pick(options,
                    'actuals',
                    'columns',
                    'indicator',
                    'model')
            );
            this.subindicator = this.model;
            this.listenTo(this.columns, 'add', this.render);
        },

        getMilestoneId: function (selectMilestone) {
            var milestone = selectMilestone(Aptivate.logframe.milestones);
            if (milestone) {
                return milestone.get('id');
            } else {
                window.alert("Set up milestones first");
            }
        },

        // we assume the baseline is the first milestone
        getBaselineTargetValue: function () {
            var target =  this.indicator.targets.findWhere({
                milestone: this.getMilestoneId(
                   HeaderRowView.prototype.firstMilestone),
                subindicator: this.subindicator.get('id')
            });
            return target ? target.get('value') : this.unknownValue;
        },

        getNextTargetValue: function () {
            var target = this.indicator.targets.findWhere({
                milestone: this.getMilestoneId(
                   HeaderRowView.prototype.nextMilestone),
                subindicator: this.subindicator.get('id')
            });
            return target ? target.get('value') : this.unknownValue;
        },

        listItems: function () {
            return this.columns.slice(-4); // TODO: use settings
        },

        itemTemplateData: function (col) {
            return {
                row: this.subindicator.get('id'),
                col: col.get('id'),
            };
        },

        getTemplateData: function () {
            var data = StaticListView.prototype.getTemplateData.apply(this, arguments);
            return _.extend(data || {}, {
                baseline: this.getBaselineTargetValue(),
                milestone: this.getNextTargetValue(),
                row: this.subindicator.get('id'),
            });
        },

        // what should Backbone.subviews use as keys in its cache?
        getSubviewId: function ($placeholder) {
            var id = $placeholder.data('row') + '-' + $placeholder.data('col');
            return id;
        },

        // get the Actual from our collection for h
        getItemFor: function ($placeholder) {
            var actualOpts = {
                    indicator: this.indicator.get('id'),
                    column: $placeholder.data('col'),
                    subindicator: $placeholder.data('row'),
                };
            return this.actuals.findWhere(actualOpts) ||
                   this.actuals.add(actualOpts);
        },

        subviewCreators: _.extend({},
            StaticListView.prototype.subviewCreators,
            {
                resultRating: function () {
                    return new EditableRating({
                        model: this.model,
                        options: Aptivate.data.ratings
                    });
                }
            }
        ),

    });

    return DataEntryRow;
});
