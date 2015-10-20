define([
    'jquery',
    'backbone',
    'views/base_view',
], function ($, Backbone, BaseView) {
    var delete_warning = "Do you really want to delete '%(object_name)%'?\n" +
        "It will also delete all its attached data (activities, indicators, subindicators...).",

    DeleteResult = BaseView.extend({
        template_selector: "#delete-result",

        events: {
            "click #delete-result": "removeResult",
        },

        initialize: function (options) {
            var warning = options.delete_warning || delete_warning;

            this.object_name = options.object_name || "object";
            this.delete_warning = warning.replace("%(object_name)%", this.object_name);
        },

        removeResult: function () {
            var do_delete = window.confirm(this.delete_warning),
                result_id;

            if (do_delete) {
                // Delete and then redirect to dashboard
                result_id = document.location.href.split("/result/")[1];
                if (result_id.slice(result_id.length - 1) === "/") {
                    result_id = parseInt(result_id.slice(0, result_id.length - 1), 10);
                }
                Aptivate.logframe.results.get(result_id)
                                         .destroy()
                                         .done(function () {
                                             Aptivate.status.router.navigate(
                                                 $("#nav-dashboard").attr("href"), {trigger: true});
                                         });
            }

        }
    });
    return DeleteResult;
});
