define(['views/base_view'], function (baseView) {

    var run = function () {

        module("BaseView");

        test("Test BaseView rendering of compiled template", function () {
            var test_model = new Backbone.Model({name: "Test"}),
                TestView = baseView.extend({
                    template_selector: "#milestone-table-heading",
                    el: "#qunit-fixture"
                }), tv;

            tv = new TestView({model: test_model});
            equal(tv.template_selector, "#milestone-table-heading", "Correct selector");

            tv.render();
            equal(tv.el.firstChild.innerHTML, "Test",
                  "Rendered element contains model's data");
        });

        test("Test getTemplateData", function () {
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
            equal(tv.el.firstChild.innerHTML, "Changed test",
                  "Rendered element contains getTemplateData changes");
        });

    };

    return run;

});
