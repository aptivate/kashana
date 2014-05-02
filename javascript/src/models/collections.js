define([
    'underscore', 'backbone', 'models/models', 'backbone_collectionsubset',
], function (_, Backbone, models) {
    var logframeUrl = '/api/logframes/' + Aptivate.data.logframe.id,

        Collections = {
            Results: Backbone.Collection.extend({
                model: models.Result,
                url: logframeUrl + '/results',
            }),

            // OVERVIEW PAGE
            Activities: Backbone.Collection.extend({
                model: models.Activity,
                url: logframeUrl + '/activities',
            }),

            BudgetLines: Backbone.Collection.extend({
                model: models.BudgetLine,
                url: logframeUrl + '/budgetlines',
            }),

            TALines: Backbone.Collection.extend({
                model: models.TALine,
                url: logframeUrl + '/talines',
            }),

            TATypes: Backbone.Collection.extend({
                model: models.TAType,
                url: logframeUrl + '/tatypes',
            }),

            // RESULT PAGE
            Assumptions: Backbone.Collection.extend({
                model: models.Assumption,
                url: logframeUrl + '/assumptions',
            }),

            RiskRatings: Backbone.Collection.extend({
                model: models.RiskRating,
                url: logframeUrl + '/riskratings',
            }),

            Indicators: Backbone.Collection.extend({
                model: models.Indicator,
                url: logframeUrl + '/indicators',
            }),

            SubIndicators: Backbone.Collection.extend({
                model: models.SubIndicator,
                url: logframeUrl + '/subindicators',
            }),

            Milestones: Backbone.Collection.extend({
                model: models.Milestone,
                url: logframeUrl + '/milestones',
                comparator: function(milestone) {
                    return new Date(milestone.get('date')).getTime();
                }
            }),

            Targets: Backbone.Collection.extend({
                model: models.Target,
                url: logframeUrl + '/targets',
            }),

            StatusCodes: Backbone.Collection.extend({
                model: models.StatusCode,
                url: logframeUrl + '/statuscodes',
            }),

            StatusUpdates: Backbone.Collection.extend({
                model: models.StatusUpdate,
                url: logframeUrl + '/statusupdates',
                comparator: function(col) {
                    return new Date(col.get('date')).getTime();
                }
            }),

            Columns: Backbone.Collection.extend({
                model: models.Column,
                url: logframeUrl + '/columns',
                /*** Comparator removed to fix #5511 ***/
            }),

            Actuals: Backbone.Collection.extend({
                model: models.Actual,
                url: logframeUrl + '/actuals',
            }),
    };

    return Collections;
});
