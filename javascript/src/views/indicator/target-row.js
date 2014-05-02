define([
    'backbone',
    'views/static-list',
    'views/input_view',
], function (Backbone, StaticListView, Editable) {

    // View for a target-data row in the milestone table, comprising a
    // subindicator in the first column and then the targets belonging to the
    // owning indicator; associated wiht the subindicator, and arranged in
    // columns according to the given collection of milestones, which are taken
    // to be in order.
    var TargetRowView = StaticListView.extend({
        tagName: "tr",

        itemView: Editable.extend({
            tagName: "td",
            template_selector: "#target-value-cell",
        }),

        // Expected options:
        // 'indicator' -- Indicator model 
        // 'collection' -- Target value models (belonging to the indicator)
        // 'collumns' -- the milestone values that define table columns
        // 'model' -- subindictor
        initialize: function (options) {
            _.extend(this,
                _.pick(options,
                    'collection',
                    'collumns',
                    'indicator',
                    'model')
            );
            this.subindicator = this.model || new Backbone.Model(),

            this.listenTo(this.collection, 'reset', this.render);
            this.listenTo(this.indicator, 'sync', this.render);
            this.listenTo(this.subindicator, 'sync', this.render);
        },

        subIndicatorView: Editable.extend({
            tagName: 'th',
            template_selector: "#editable-name",
        }),

        // Add views for target measurements for the given:  
        //  - indicator, 
        //  - milestone (column), and
        //  - subindicator (row)
        addAll: function () {
            this.collumns.each(function (milestone) {
                var opts = {
                        milestone: milestone.id,
                        indicator: this.indicator.get('id'),
                        subindicator: this.subindicator.get('id'),
                    },
                    target = this.collection.findWhere(opts) ||
                             this.collection.add(opts);
                this.addItem(target);
            }, this);
        },

        render: function () {
            if (!this.indicator.isNew()){
                this.$el.html('');
                new this.subIndicatorView({
                    model: this.subindicator
                }).render().$el.appendTo(this.$el);
                if (!this.subindicator.isNew()) {
                    this.addAll();
                }
            }
            return this;
        },

    });

    return TargetRowView;
    
});
