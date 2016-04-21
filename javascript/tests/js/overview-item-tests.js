define([
   'backbone', 'jquery', 'models/collections', 'views/result/overview_item',
], function (BB, $, Collections, OverviewItem) {
	describe("Overview Item Tests", function () {
		it("shouldn't have a max length of 1", function() {
			Aptivate.data.conf = {open_result_level: 1};
			var model = {id: 1, name: 'test', results: [], level: 1, get: function (name) {return 1;}}
			overviewItem = new OverviewItem({model: model});
			
			resultList = overviewItem.resultOverviewView({}, {}, 1);
			expect(resultList.maxLength).toBeUndefined();
		});
	});
});