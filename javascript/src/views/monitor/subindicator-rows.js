define([
    'backbone',
    'views/base_view',
], function (Backbone, BaseView) {
    var IndicatorContainerView = BaseView.extend({
        tagName: 'tbody',
        template_selector: "#monitor-subindicator-rows",

        initialize: function () {
            Backbone.Subviews.add(this);
        },

        subviewCreators: {
        }

    });

    return IndicatorContainerView;
});
