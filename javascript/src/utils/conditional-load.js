define([
    'jquery',
], function ($) {
    // Load data from Aptivate.data if it exists or server otherwise
    function conditionalLoadData(collection, data_field, fetch_options) {
        var promise;

        if (Aptivate.data[data_field]) {
            collection.reset(Aptivate.data[data_field]);
            delete Aptivate.data[data_field];

            // Return resolved promise
            promise = $.Deferred();
            promise = promise.resolve();
        } else {
            promise = collection.fetch(fetch_options);
        }
        return promise;
    }
    return conditionalLoadData;
});
