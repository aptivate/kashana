define([
    'views/base_view',
    'views/generic/list',
    'views/generic/template-list',
    'views/input_view',
    'views/indicator/target-row',
], function (BaseView, ListView, StaticListView, Editable, TargetRowView) {

    var MilestoneTableView = BaseView.extend({

        tagName: 'table',
        template_selector: "#milestone-table",
        className: 'scrollable',

        initialize: function () {
            Backbone.Subviews.add(this);
        },

        subviewCreators: {
            milestoneRow: function () {
                return new StaticListView({
                    collection: Aptivate.logframe.milestones,
                    tagName: 'tr',
                    template_selector: "#milestone-table-heading-row",
                    attributes: { class: 'milestone-heading-row' },
                    itemView: Editable.extend({
                        tagName: "th",
                        template_selector: "#milestone-table-heading",
                    }),
                });
            },
            subindicatorRows: function () {
                var indicator = this.model;

                if (!indicator.targets) {
                    // TODO: move the targets into the Indicator declaration
                    indicator.targets = Aptivate.logframe.targets.subcollection({
                        filter: function (target) {
                            var sub_id = target.get("subindicator");
                            return !!(indicator.subindicators.get(sub_id));
                        }
                    });
                }
                // Next line is required because next-to-be-added indicator does
                // not have an ID yet so its related subcollections need to be
                // recreated correctly once it does (once it has been added)
                indicator.on("change:id", indicator.initialize);

                return new ListView({
                    itemView: TargetRowView.extend({
                        indicator: indicator,
                        collection: indicator.targets,
                        collumns: Aptivate.logframe.milestones,
                    }),
                    collection: indicator.subindicators,
                    newModelOptions: function () {
                        // defer looking for the owning indicator's id because
                        // it might have been new when this view was created.
                        return { indicator: indicator.get('id') };
                    },
                    tagName: 'tbody',
                });
            },
        },

    });

    return MilestoneTableView;
});

