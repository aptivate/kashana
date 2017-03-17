define([
    'jquery',
    'backbone',
    'views/base_view',
    'views/generic/list',
    'views/input_view',
    'views/editable-text',
    'views/editable/select',
    'views/indicator/container',
    'views/result/delete-result',
], function ($, Backbone, BaseView, ListView,
        Editable, EditableText, Selectable, IndicatorView, DeleteResult) {
    var ResultView = BaseView.extend({
        // View
        tagName: 'div',
        template_selector: "#result-container",

        initialize: function () {
            Backbone.Subviews.add(this);
        },

        subviewCreators: {
            resultName: function () {
                return new Editable({
                    model: this.model,
                    template_selector: "#editable-title",
                    attributes: { class: "ribbon ribbon-result" },
                });
            },
            resultDescription: function () {
                return new EditableText({
                    model: this.model,
                    template_selector: "#editable-description",
                    attributes: { class: "description" }
                });
            },
            resultContribution: function () {
                if (waffle.switch_is_active("enable impact weighting")) {
                    return new Editable({
                        model: this.model,
                        template_selector: "#result-contribution-weighting",
                        attributes: { class: "impact-weighting" }
                    });
                }

                return null;
            },
            assumptionList: function () {
                var resultId = this.model.get("id");
                return new ListView({
                    tagName: 'ul',
                    itemView: EditableText.extend({
                        tagName: "li",
                        template_selector: "#assumption-detail",
                    }),
                    newModelOptions: { result: this.model.get('id') },
                    collection: Aptivate.logframe.assumptions.subcollection({
                        filter: function (assumption) {
                            return assumption.get("result") === resultId;
                        }
                    }),
                    attributes: {class: "assumption-list"}
                });
            },
            indicatorList: function () {
                var resultId = this.model.get("id");
                return new ListView({
                    itemView: IndicatorView,
                    newModelOptions: { result: this.model.get('id') },
                    collection: Aptivate.logframe.indicators.subcollection({
                        filter: function (indicator) {
                            return indicator.get("result") === resultId;
                        }
                    }),
                });
            },
            resultRiskRating: function () {
                if (waffle.switch_is_active("enable risk rating")) {
                    return new Selectable({
                        className: "risk-rating",
                        model: this.model,
                        field_name: 'risk_rating',
                        options: Aptivate.data.riskratings,
                        template_selector: "#result-risk-rating"
                    });
                }

                return null;
            },
            deleteResult: function () {
                var object_name = this.model.get('name') || "object";

                return new DeleteResult({
                    model: this.model,
                    className: "delete-button",
                    object_name: object_name
                });
            }
        }

    });

    return ResultView;
});
