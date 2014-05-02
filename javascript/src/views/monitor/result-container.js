define([
    'backbone',
    'views/base_view',
    'views/editable/rating',
    'views/generic/template-list',
    'views/monitor/indicator-container',
], function (Backbone, BaseView, EditableRating, StaticList, IndicatorContainer) {
    var ResultView = BaseView.extend({
        tagName: 'div',
        template_selector: "#monitor-result-container",

        initialize: function () {
            Backbone.Subviews.add(this);
        },

        subviewCreators: {
            indicatorList: function (){
                return new StaticList({
                    tagName: 'div',
                    collection: this.model.indicators,
                    itemView: IndicatorContainer,
                });
            },
            resultRating: function () {
                return new EditableRating({
                    model: this.model,
                    options: Aptivate.data.ratings
                });
            },
        }

    });

    return ResultView;
});
