define([
   'backbone', 'jquery', 'models/collections', 'views/overview/container',
], function (BB, $, Collections, OverviewContainer) {
	describe("Overview Container Tests", function () {
		it("shouldn't have a max length of 1", function() {
			var model = {id: 1, name: 'test', results: [], level: 1, get: function (name) {return 1;}}
			overviewContainer = new OverviewContainer({model: model});
			overviewContainer.subviewCreators.model = model;
			overviewContainer.subviewCreators.collection = new Collections.Results();
			resultList = overviewContainer.subviewCreators.resultList();
			expect(resultList.maxLength).toBeUndefined();
		});
	});
});