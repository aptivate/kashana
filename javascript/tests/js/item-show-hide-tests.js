define([
		 'jquery', 'models/models', 'views/result/overview_item'
], function($, models, OverviewItem) {
	jasmine.getFixtures().fixturesPath = 'tests/html_fixtures';
	
	var overviewItem, 
		ctx;
	
	describe('Toggling the arrows for showing and hiding items', function () {
		beforeEach(function (done) {
			loadFixtures('items_to_show_hide.html');
			ctx = $("#qunit-fixture");
			
			overviewItem = new OverviewItem({model: new models.Result()});
			done();
		});
		
		it('showing third level sets elements on child results to show if previously shown', function () {
			event = {
				target: $('.result-overview.level-3 .toggle-triangle', ctx)[0],
			    delgateTarget: $('.result-overview.level-3', ctx)[0],
				stopPropagation: function() {},
			};

			overviewItem.toggleDetails(event);
			overviewItem.toggleDetails(event);
			
			expect($('.result-overview-table.level-4 .toggle-triangle.show').length).toEqual(1);
		});
		
		it('showing second level sets elements on child results to show if previously shown', function () {
			event = {
				target: $('.result-overview.level-2 .toggle-triangle', ctx)[0],
			    delgateTarget: $('.result-overview.level-2', ctx)[0],
				stopPropagation: function() {},
			};

			overviewItem.toggleDetails(event);
			overviewItem.toggleDetails(event);
			
			expect($('.result-overview-table.level-3 .toggle-triangle.show').length).toEqual(1);
			expect($('.result-overview-table.level-4 .toggle-triangle.show').length).toEqual(1);
		});
		
		it('showing first level sets elements on child results to show if previously shown', function () {
			event = {
				target: $('.result-overview.level-1 .toggle-triangle', ctx)[0],
			    delgateTarget: $('.result-overview.level-1', ctx)[0],
				stopPropagation: function() {},
			};

			overviewItem.toggleDetails(event);
			overviewItem.toggleDetails(event);
			
			expect($('.result-overview-table.level-2 .toggle-triangle.show').length).toEqual(1);
			expect($('.result-overview-table.level-3 .toggle-triangle.show').length).toEqual(1);
			expect($('.result-overview-table.level-4 .toggle-triangle.show').length).toEqual(1);
		});
	});
});