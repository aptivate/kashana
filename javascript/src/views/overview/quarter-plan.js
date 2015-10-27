define([
        'backbone',
        'jquery',
        'views/base_view',
], function (Backbone, $, BaseView) {
    var ExportQuarterPlanView = BaseView.extend({
        tagName: "span",
        className: "export-quarter-plan",
        template_selector: "#export-quarter-plan",

        events: {
            "change select": "exportQuarterPlan"
        },

        exportQuarterPlan: function (e) {
            var value = $(e.target).val() || "",
                url;
            if (value) {
                url = Aptivate.data.export_quarter_plan_url.replace("01-1900", value);
                window.open(url, 'export');
            }
            return false;
        },

        getTemplateData: function () {
            var data_periods = Aptivate.data.periods;

            var periods = $(data_periods).map(function () {
                var bits = this.start.split("-");
                return {
                    name: this.name,
                    start: bits[1] + "-" + bits[0]
                };
            });

            return {
                periods: periods
            };
        }
    });

    return ExportQuarterPlanView;
});
