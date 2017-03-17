define([
    'jquery',
    'backbone',
    'pages/overview-page',
    'pages/result-page',
    'pages/monitor-page',
], function ($, Backbone, OverviewPage, ResultPage, MonitorPage) {
    function integer(string_value) {
        return parseInt(string_value, 10);
    }

    function PageLoader(element) {
        var self = this;

        this.$element = $(element);

        // call back to use when page is loaded and rendered
        this.showView = function(view){
            view.render();
            self.$element.html(view.el);
        };

        // unload current page and load new one
        this.showPage = function (page) {
            // Remove any editor menus lying around
            $(".pen-editor-menu").remove();

            this.$element.html('<h2 class="loading-indicator">Loading...</h2>');
            if (this.currentPage){
                this.currentPage.unload();
            }
            this.currentPage = page;
            this.currentPage.load(this.showView);
        };

    }

    var Router = Backbone.Router.extend({
        routes: {
            "": "home",
            "dashboard/:organization_slug/:logframe_slug/": "showOverview",
            "design/:logframe_id/result/:result_id/": "showResult",
            "monitor/:logframe_id/result/:result_id/": "showMonitor",
            "*other": "defaultRouter"
        },

        appView:  new PageLoader('#current-page'),

        home: function () {
            // TODO: Non-local dependency: can't this be this.router.navigate...?
            Aptivate.status.router.navigate(
                "dashboard/",
                { trigger: true, replace: true });
        },

        showOverview: function () {
            this.appView.showPage(
                new OverviewPage({ logframe: Aptivate.logframe })
            );
        },

        showResult: function (logframeId, resultId) {
            this.appView.showPage(
                new ResultPage({ resultId: integer(resultId) })
            );
        },

        showMonitor: function (logframeId, resultId) {
            this.appView.showPage(
                new MonitorPage({ resultId: integer(resultId) })
            );
        },

        defaultRoute: function (other) {
            console.log('Invalid. You attempted to reach:' + other);
        }
    });

    return Router;
});
