define([
        'jquery',
        'models/models',
        'models/collections',
        'views/overview/container',
        'utils/conditional-load',
], function ($, models, collections, OverviewContainer, load) {

    function OverviewPage(options) {

        this.load = function (showView) {
            // Load missing data
            var self = this,
                promises = [
                    load(Aptivate.logframe.results, "results"),
                    load(Aptivate.logframe.activities, "activities"),
                    load(Aptivate.logframe.budgetlines, "budgetlines"),
                    load(Aptivate.logframe.talines, "talines"),
                    load(Aptivate.logframe.statusupdates, "statusupdates")
                ];

            $.when.apply(this, promises).then(function () {
                self.overviewContainer = new OverviewContainer({
                    model: options.logframe
                });
                showView(self.overviewContainer);
            });
        };

        this.unload = function () {
            // Possible race condition here if remove() is called before the
            // promises above have completed, overviewcontainer won't yet exist.
            this.overviewContainer.remove();
        };
    }

    return OverviewPage;
});
