define([
        'backbone',
        'jquery',
        'views/base_view',
], function (Backbone, $, BaseView) {
    var ExportAnnualPlanView = BaseView.extend({
        tagName: "span",
        className: "export-annual-plan",
        template_selector: "#export-annual-plan",

        events: {
            "change select": "exportAnnualPlan"
        },

        exportAnnualPlan: function (e) {
            var value = $(e.target).val() || "",
                url;
            if (value) {
                url = Aptivate.data.export_annual_plan_url.replace("1900", value);
                window.open(url, 'export');
            }
            return false;
        },

        getTemplateData: function () {
            var periods = Aptivate.data.periods;

            var years = $(periods).map(function () {
                return this.start.split("-")[0];
            });

            return {
                years: $.unique(years).toArray(),
            };
        }
    });

    return ExportAnnualPlanView;
});
