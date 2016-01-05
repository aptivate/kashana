define(['views/base_view'], function (baseView) {
	
	jasmine.getFixtures().fixturesPath = 'tests/html_fixtures';
	
    describe("BaseView", function () {
    	beforeEach(function() {
    		loadFixtures('components/base_view.html');
    	});

        it("Test BaseView rendering of compiled template", function () {
            var test_model = new Backbone.Model({name: "Test"}),
                TestView = baseView.extend({
                    template_selector: "#milestone-table-heading",
                    el: "#qunit-fixture"
                }), tv;

            tv = new TestView({model: test_model});
            since("Correct selector");
            expect(tv.template_selector).toEqual("#milestone-table-heading");

            tv.render();
            since("Rendered element contains model's data");
            expect(tv.el.firstChild.innerHTML).toEqual("Test");
        });

        it("Test getTemplateData", function () {
            var test_model = new Backbone.Model({name: "Test"}),
                TestView = baseView.extend({
                    template_selector: "#milestone-table-heading",
                    el: "#qunit-fixture",
                    getTemplateData: function (data) {
                        data.name = "Changed test";
                        return data;
                    }
                }), tv;

            tv = new TestView({model: test_model});
            tv.render();
            since("Rendered element contains getTemplateData changes");
            expect(tv.el.firstChild.innerHTML).toEqual("Changed test");
        });
    });
});
