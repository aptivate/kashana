define([
    'underscore',
    'backbone',
    'jquery',
    'views/overview/filter-lead',
], function (_, BB, $, LeadView) {
	
	jasmine.getFixtures().fixturesPath = 'tests/html_fixtures';
	
	var setVisibility = LeadView.prototype.setVisibility,
        ctx = null;
	
	
	
    describe("Filter Lead Tests",  function() {
    	beforeEach(function() {
    		loadFixtures('filter_lead.html');
    		ctx = $("#qunit-fixture");
    	});
    	
        it('Check filter matches correct item', function () {
            var not_empty = ['node1', 'node2', 'node5', 'node6', 'node8'];
            
            var assertCount = 0;
            
            since("There are just 10 containers");
            expect($("div", ctx)).toHaveLength(10);
            assertCount++;

            setVisibility(1);
            
            since("Only 5 or them should be set to empty");
            expect($("div.empty", ctx)).toHaveLength(5);
        	assertCount++;
       
            // The right ones are marked as not empty
            $("div:not(.empty)", ctx).each(function (i, el) {
                expect($(el)).toHaveId(not_empty[i]);
                assertCount++;
            });
            
            since("Only one activity is selected");
            expect($(".selected-activity").length).toEqual(1);
            assertCount++;
            
            since("The right one was selected");
            expect($(".selected-activity").attr("id")).toEqual("act2");
            assertCount++;
            
            since("There should be 9 assertions.");
            expect(assertCount).toEqual(9);
        });

        it('Check filter none clears everything', function () {
        	since("There are just 10 containers");
            expect($("div", ctx)).toHaveLength(10);
            setVisibility(1);
            setVisibility();
            
            since( "No container is marked as empty");
            expect($("div.empty", ctx)).toHaveLength(0);
            
            since("No activity is marked as selected");
            expect($(".selected-activity")).toHaveLength(0);
        });

        it('Check new filter marks only new matches', function () {
            var not_empty = ['node1', 'node2', 'node7', 'node8', 'node9'];
            var assertCount = 0;

            since("There are just 10 containers");
            expect($("div", ctx)).toHaveLength(10);
            assertCount++;
            setVisibility(1);
            setVisibility(2);
            
            since("Only 5 or them should be set to empty");
            expect($("div.empty", ctx).length).toEqual(5);
            assertCount++;
            // The right ones are marked as not empty
            $("div:not(.empty)", ctx).each(function (i, el) {
                expect($(el)).toHaveId(not_empty[i]);
                assertCount++;
            });

            since("Only one activity is selected")
            expect($(".selected-activity")).toHaveLength(1);
            assertCount++;
            
            since("The right one was selected")
            expect($(".selected-activity")).toHaveId("act3");
            assertCount++;
            
            since("There should be 9 assertions.");
            expect(assertCount).toEqual(9);
        });
    });
});
