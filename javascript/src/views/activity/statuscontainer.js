define([
    'backbone',
    'views/base_view',
    'views/activity/statusupdate',
    'views/generic/template-list',
    'views/activity/statushistory',
], function (Backbone, BaseView, StatusUpdate, ListView, StatusHistory){

    var StatusContainerView = BaseView.extend({
        template_selector: '#activity-statuscontainer',

        initialize: function () {
            Backbone.Subviews.add(this);
        },

        subviewCreators: {
            "statusUpdate": function () {
                return new StatusUpdate({
                    model: this.model,
                    collection: this.model.statusupdates
                });
            },
            "statusHistory": function () {
                return new ListView({
                    tagName: "table",
                    className: "status-updates-table",
                    collection: this.model.statusupdates,
                    itemView: StatusHistory
                });
            }
        }

    });

    return StatusContainerView;
});
