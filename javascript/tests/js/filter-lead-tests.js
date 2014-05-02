define([
    'underscore',
    'backbone',
    'jquery',
    'views/overview/filter-lead',
], function (_, BB, $, LeadView) {
    var runtests = function () {
        var setVisibility = LeadView.prototype.setVisibility,
            ctx = $("#qunit-fixture");

        test('Check filter matches correct item', function () {
            var not_empty = ['node1', 'node2', 'node5', 'node6', 'node8'];
            expect(9);

            equal($("div", ctx).length, 10, "There are just 10 containers");

            setVisibility(1);
            equal($("div.empty", ctx).length, 5, "Only 5 or them should be set to empty");
            // The right ones are marked as not empty
            $("div:not(.empty)", ctx).each(function (i, el) {
                equal($(el).attr("id"), not_empty[i]);
            });

            equal($(".selected-activity").length, 1, "Only one activity is selected");
            equal($(".selected-activity").attr("id"), "act2", "The right one was selected");
        });

        test('Check filter none clears everything', function () {
            equal($("div", ctx).length, 10, "There are just 10 containers");
            setVisibility(1);
            setVisibility();

            equal($("div.empty", ctx).length, 0, "No container is marked as empty");
            equal($(".selected-activity").length, 0, "No activity is marked as selected");
        });

        test('Check new filter marks only new matches', function () {
            var not_empty = ['node1', 'node2', 'node7', 'node8', 'node9'];
            expect(9);

            equal($("div", ctx).length, 10, "There are just 10 containers");
            setVisibility(1);
            setVisibility(2);

            equal($("div.empty", ctx).length, 5, "Only 5 or them should be set to empty");
            // The right ones are marked as not empty
            $("div:not(.empty)", ctx).each(function (i, el) {
                equal($(el).attr("id"), not_empty[i]);
            });

            equal($(".selected-activity").length, 1, "Only one activity is selected");
            equal($(".selected-activity").attr("id"), "act3", "The right one was selected");
        });
    };

    return runtests;
});
