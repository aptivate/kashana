define([
    'underscore',
    'jquery',
    'views/overview/utils/container-mixin',
], function (_, $, Mixin) {
	
    var getDateLimit = Mixin.getDateLimit,
        intersects = Mixin.intersects,
        ctx = null;

    jasmine.getFixtures().fixturesPath = 'tests/html_fixtures';
	
    
    // INTERSECTS
    describe("intersects", function () {
	    it("Check closed intervals intersect correctly", function () {
	        since("Overlaps");
	    	expect(intersects("2014-02-01", "2014-02-15",
	    			"2014-02-13", "2014-02-28")).toEqual(true);
	    	
	    	since("Overlaps a day");
	        expect(intersects("2014-02-01", "2014-02-15",
	                      "2014-02-15", "2014-02-28")).toEqual(true);
	        
	        since("Contained interval also matches");
	        expect(intersects("2014-02-01", "2014-02-15",
	                      "2014-02-02", "2014-02-14")).toEqual(true);
	        
	        since("Disjunct intervals don't match");
	        expect(intersects("2014-02-01", "2014-02-15",
	                       "2014-02-16", "2014-02-24")).toEqual(false);
	    });
	
	    it("Check open intervals intersect correctly", function () {
	        since("Matches open start")
	    	expect(intersects("", "2014-02-15",
	                      "2014-02-13", "2014-02-28")).toEqual(true);
	        
	        since("Matches open end");
	        expect(intersects("2014-02-01", "2014-02-15",
	                      "2014-02-15", Mixin.BiggestDate)).toEqual(true);
	        
	        since("Undefined/open matches all");
	        expect(intersects("", Mixin.BiggestDate,
	                      "2014-02-13", "2014-02-28")).toEqual(true);
	        
	        since("Disjunct intervals don't match");
	        expect(intersects("", "2014-02-15",
	                       "2014-02-16", "2014-02-24")).toEqual(false);
	    });
    });

    // GETDATELIMIT
    describe("getDateLimit", function () {
    	beforeEach(function() {
    		loadFixtures('filter_dates.html');
    		ctx = $("#qunit-fixture");
    	});
    	
	    it("Check there is no minDate on empty start date", function () {
	        var options = getDateLimit($("#filter-time-end"));
	        since("No limit was returned");
	        expect(options).toBeUndefined();
	    });
	
	    it("Check there is minDate when start date is set", function () {
	        var limit = "2014-03-02",
	            options;
	        $("#filter-time-start").val(limit);
	        options = getDateLimit($("#filter-time-end"));
	        
	        since("minDate was returned with correct date");
	        expect(options.minDate).toEqual(limit);
	    });
	
	    it("Check there is no maxDate on empty end date", function () {
	        var options = getDateLimit($("#filter-time-start"));
	        since("No limit was returned");
	        expect(options).toBeUndefined();
	    });
	
	    it("Check there is maxDate when end date is set", function () {
	        var limit = "2014-03-02",
	            options;
	        $("#filter-time-end").val(limit);
	        options = getDateLimit($("#filter-time-start"));
	        since("maxDate was returned with correct date");
	        expect(options.maxDate).toEqual(limit);
	    });
    });
    // SETVISIBILITY
    describe("setVisibility", function () {
    	beforeEach(function() {
    		loadFixtures('filter_dates.html');
    		ctx = $("#qunit-fixture");
    	});
    	
	    it("Check bounded filter matches correct items", function () {
	    	since("There are just 10 containers");
	        expect($("div", ctx)).toHaveLength(11);
	        
	        since("No element is marked as empty or hidden");
	        expect($(".empty, .hide", ctx)).toHaveLength(0);
	
	        Mixin.setVisibility("2014-01-05", "2014-01-20");  // Matches acts: 1, 3 and 4
	        since("One item does not match");
	        expect($(".hide", ctx)).toHaveLength(1);
	        
	        since("The right one is hidden");
	        expect($(".hide", ctx)).toHaveId("node6");
	        
	        since("Correct number are marked as empty");
	        expect($(".empty", ctx)).toHaveLength(1);
	    });
	
	    it("Check unbound start filter matches correct items", function () {
	        since("There are just 10 containers");
	    	expect($("div", ctx)).toHaveLength(11);
	    	
	    	since("No element is marked as empty or hidden");
	        expect($(".empty, .hide", ctx)).toHaveLength(0);
	
	        Mixin.setVisibility("", "2014-01-20");  // Matches acts: 1, 3 and 4
	        since("One item does not match");
	        expect($(".hide", ctx)).toHaveLength(1);
	        
	        since("The right one is hidden");
	        expect($(".hide", ctx)).toHaveId("node6");
	        
	        since("Correct number are marked as empty");
	        expect($(".empty", ctx)).toHaveLength(1);
	    });
	
	    it("Check unbound end filter matches correct items", function () {
	        since("There are just 10 containers");
	    	expect($("div", ctx)).toHaveLength(11);
	    	
	    	since("No element is marked as empty or hidden");
	        expect($(".empty, .hide", ctx)).toHaveLength(0);
	
	        Mixin.setVisibility("2014-03-05", "");  // Matches acts: 1, 2 and 3
	        since("One item does not match");
	        expect($(".hide", ctx)).toHaveLength(1);
	        
	        since("The right one is hidden");
	        expect($(".hide", ctx)).toHaveId("node10");
	        
	        since("Correct number are marked as empty");
	        expect($(".empty", ctx)).toHaveLength(0);
	    });
	
	    it("Check completely unbound match items", function () {
	        since("There are just 10 containers");
	    	expect($("div", ctx)).toHaveLength(11);
	    	
	    	since("No element is marked as empty or hidden");
	        expect($(".empty, .hide", ctx)).toHaveLength(0);
	
	        Mixin.setVisibility("", "");  // Matches all
	        since("No element is marked as empty or hidden");
	        expect($(".empty, .hide", ctx)).toHaveLength(0);
	    });
    });
});
