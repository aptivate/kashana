define([
        'backbone',
        'jquery',
        'views/base_view',
], function (Backbone, $, BaseView) {
    var ExportView = BaseView.extend({
        tagName: "p",
        className: "export-data-select",
        template_selector: "#export-data",

        events: {
            "change select": "exportPeriod"
        },

        exportPeriod: function (e) {
            var value = $(e.target).val() || "",
                url;
            if (value) {
                // 1900-01-01 is used for easier pattern matching
                url = Aptivate.data.export_url.replace("1900-01-01", value);
                window.open(url, 'export');
            }
            return false;
        },

        getTemplateData: function () {
            return {
                periods: Aptivate.data.periods
            };
        }
    });

    return ExportView;
});
