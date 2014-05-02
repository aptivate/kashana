define([
    'underscore',
    'jquery',
    'views/overview/utils/container-mixin',
], function (_, $, Mixin) {
    var getDateLimit = Mixin.getDateLimit,
        intersects = Mixin.intersects,
        ctx = $("#qunit-fixture");

    var runtests = function () {
        // INTERSECTS
        module("intersects");
        test("Check closed intervals intersect correctly", function () {
            ok(intersects("2014-02-01", "2014-02-15",
                          "2014-02-13", "2014-02-28"), "Overlaps");
            ok(intersects("2014-02-01", "2014-02-15",
                          "2014-02-15", "2014-02-28"), "Overlaps a day");
            ok(intersects("2014-02-01", "2014-02-15",
                          "2014-02-02", "2014-02-14"), "Contained interval also matches");
            ok(!intersects("2014-02-01", "2014-02-15",
                           "2014-02-16", "2014-02-24"), "Disjunct intervals don't match");
        });

        test("Check open intervals intersect correctly", function () {
            ok(intersects("", "2014-02-15",
                          "2014-02-13", "2014-02-28"), "Matches open start");
            ok(intersects("2014-02-01", "2014-02-15",
                          "2014-02-15", Mixin.BiggestDate), "Matches open end");
            ok(intersects("", Mixin.BiggestDate,
                          "2014-02-13", "2014-02-28"), "Undefined/open matches all");
            ok(!intersects("", "2014-02-15",
                           "2014-02-16", "2014-02-24"), "Disjunct intervals don't match");
        });

        // GETDATELIMIT
        module("getDateLimit");
        test("Check there is no minDate on empty start date", function () {
            var options = getDateLimit($("#filter-time-end"));
            ok(options === undefined, "No limit was returned");
        });

        test("Check there is minDate when start date is set", function () {
            var limit = "2014-03-02",
                options;
            $("#filter-time-start").val(limit);
            options = getDateLimit($("#filter-time-end"));
            equal(options.minDate, limit, "minDate was returned with correct date");
        });

        test("Check there is no maxDate on empty end date", function () {
            var options = getDateLimit($("#filter-time-start"));
            ok(options === undefined, "No limit was returned");
        });

        test("Check there is maxDate when end date is set", function () {
            var limit = "2014-03-02",
                options;
            $("#filter-time-end").val(limit);
            options = getDateLimit($("#filter-time-start"));
            equal(options.maxDate, limit, "maxDate was returned with correct date");
        });

        // SETVISIBILITY
        module("setVisibility");
        test("Check bounded filter matches correct items", function () {
            equal($("div", ctx).length, 11, "There are just 10 containers");
            equal($(".empty, .hide", ctx).length, 0, "No element is marked as empty or hidden");

            Mixin.setVisibility("2014-01-05", "2014-01-20");  // Matches acts: 1, 3 and 4
            equal($(".hide", ctx).length, 1, "One item does not match");
            equal($(".hide", ctx).attr("id"), "node6", "The right one is hidden");
            equal($(".empty", ctx).length, 1, "Correct number are marked as empty");
        });

        test("Check unbound start filter matches correct items", function () {
            equal($("div", ctx).length, 11, "There are just 10 containers");
            equal($(".empty, .hide", ctx).length, 0, "No element is marked as empty or hidden");

            Mixin.setVisibility("", "2014-01-20");  // Matches acts: 1, 3 and 4
            equal($(".hide", ctx).length, 1, "One item does not match");
            equal($(".hide", ctx).attr("id"), "node6", "The right one is hidden");
            equal($(".empty", ctx).length, 1, "Correct number are marked as empty");
        });

        test("Check unbound end filter matches correct items", function () {
            equal($("div", ctx).length, 11, "There are just 10 containers");
            equal($(".empty, .hide", ctx).length, 0, "No element is marked as empty or hidden");

            Mixin.setVisibility("2014-03-05", "");  // Matches acts: 1, 2 and 3
            equal($(".hide", ctx).length, 1, "One item does not match");
            equal($(".hide", ctx).attr("id"), "node10", "The right one is hidden");
            equal($(".empty", ctx).length, 0, "Correct number are marked as empty");
        });

        test("Check completely unbound match items", function () {
            equal($("div", ctx).length, 11, "There are just 10 containers");
            equal($(".empty, .hide", ctx).length, 0, "No element is marked as empty or hidden");

            Mixin.setVisibility("", "");  // Matches all
            equal($(".empty, .hide", ctx).length, 0, "No element is marked as empty or hidden");
        });
    };

    return runtests;
});
