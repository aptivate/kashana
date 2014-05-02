define([
        'backbone',
        'jquery',
], function (Backbone, $) {
    // This mixin was created for easier testing
    var ViewMixin = {
        BiggestDate: "9999-12-31",

        // Listener helpers
        getDateLimit: function ($el) {
            var ids = ["filter-time-end", "filter-time-start"],
                ops = ["maxDate", "minDate"],
                index = $el.attr("id") === "filter-time-end" ? 1 : 0,
                value, options;

            value = $.trim($("#" + ids[index]).val());
            if (value) {
                options = {};
                options[ops[index]] = value;
            }
            return options;
        },

        intersects: function (p1s, p1e, p2s, p2e) {
            // Does period p1 intersect period p2?
            return (p1s === p2s) || (p1s > p2s ? p1s <= p2e : p2s <= p1e);
        },

        setVisibility: function (start, raw_end) {
            // Don't use jQuery remove because it removes handlers
            var self = this,
                end = raw_end || this.BiggestDate,
                $d = $(".result-tree > .result-overview").detach();

            // Always reset state first
            $d.find(".empty, .hide")
                    .removeClass("empty hide");

            // Make a selection if there is one
            if (start || end !== this.BiggestDate) {
                $d.find(".result-overview")
                        .addClass("empty")
                    .end()
                    .find(".activity-item")
                        .addClass("hide");
                $d.find('.activity-item')
                        .find('.result-overview-table.show-full-ui').each(function (i, activity) {
                    var $el = $(activity),
                        el_start = $el.data("start"),
                        el_end = $el.data("end") || self.BiggestDate;

                    if (self.intersects(el_start, el_end, start, end)) {
                        $el.parents(".result-overview, .activity-item")
                            .removeClass("empty hide");
                    }
                  });
            }
            $d.appendTo(".result-tree");
        }
    };

    return ViewMixin;
});
