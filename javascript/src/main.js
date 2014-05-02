require(['require.config'], function () {

    require(['app', 'router'
            ], function (app, Router) {
        Aptivate.status.router = new Router();

        // Intercept dashboard tab click and handle it in app
        $("#nav-dashboard").on("click", function (e) {
            e.preventDefault();

            Aptivate.status.router.navigate(
                $(e.target).attr("href"), {trigger: true});
        });

        Backbone.history.start({
            pushState: true,
            root: "/"
        });
    });

});
