define([
    'underscore', 'backbone',
], function (_, Backbone) {
    var logframeUrl = '/api/logframes/' + Aptivate.data.logframe.id,

        Models = {
            Logframe : Backbone.Model.extend({
                urlRoot: '/api/logframes',
            }),

            Result: Backbone.Model.extend({
                defaults: {
                    order: 0
                },
                urlRoot: logframeUrl + '/results',

                initialize: function () {
                    var thisResult = this;
                    this.indicators = Aptivate.logframe.indicators.subcollection({
                        filter: function (indicator) {
                            return indicator.get('result') === thisResult.get('id');
                        }
                    });
                },
            }),

            Activity: Backbone.Model.extend({
                defaults: {
                    order: 0
                },
                urlRoot: logframeUrl + '/activities',
            }),

            BudgetLine: Backbone.Model.extend({
                defaults: {
                    value: 0
                },
                urlRoot: logframeUrl + '/budgetlines',
            }),

            TALine: Backbone.Model.extend({
                urlRoot: logframeUrl + '/talines',
            }),

            TAType: Backbone.Model.extend({
                urlRoot: logframeUrl + '/tatypes',
            }),

            Assumption: Backbone.Model.extend({
                urlRoot: logframeUrl + '/assumptions',
            }),

            RiskRating: Backbone.Model.extend({
                urlRoot: logframeUrl + '/riskratings',
            }),

            Indicator: Backbone.Model.extend({
                urlRoot: logframeUrl + '/indicators',

                initialize: function () {
                    var indicatorId = this.get('id'),
                        indicatorFilter = function (object) {
                            return object.get('indicator') === indicatorId;
                        };
                    this.columns = Aptivate.logframe.columns.subcollection({
                        filter: indicatorFilter
                    });
                    this.subindicators = Aptivate.logframe.subindicators.subcollection({
                        filter: indicatorFilter
                    });
                    this.actuals = Aptivate.logframe.actuals.subcollection({
                        filter: indicatorFilter
                    });
                    this.targets = Aptivate.logframe.targets.subcollection({
                        filter: indicatorFilter
                    });
                }
            }),

            SubIndicator: Backbone.Model.extend({
                urlRoot: logframeUrl + '/subindicators',
            }),

            Milestone: Backbone.Model.extend({
                urlRoot: logframeUrl + '/milestones',
            }),

            Target: Backbone.Model.extend({
                urlRoot: logframeUrl + '/targets',
            }),

            StatusCode: Backbone.Model.extend({
                urlRoot: logframeUrl + '/statuscodes',
            }),

            StatusUpdate: Backbone.Model.extend({
                urlRoot: logframeUrl + '/statusupdates',
            }),

            Column: Backbone.Model.extend({
                urlRoot: logframeUrl + '/columns',
            }),

            Actual: Backbone.Model.extend({
                urlRoot: logframeUrl + '/actuals',
            }),
        };

    return Models;
});
