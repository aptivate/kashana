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
            equal(tv.el.firstChild.innerHTML, "Test");
        });

    };

    return run;

});
