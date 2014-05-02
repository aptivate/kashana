define(['views/base_view'], function (baseView) {

    var run = function () {

        module("Test infrastructure");

        test("hello test", function () {
            var test_model = new Backbone.Model({name: "Test"}),
                TestView = baseView.extend({
                    template_selector: "#handle-template",
                    el: "#qunit-fixture"
                }), tv;

            ok( 1 == "1", "Passed!");

            tv = new TestView({model: test_model});
            equal(tv.template_selector, "#handle-template", "Correct selector");
            equal(tv.render().el.innerHTML, "Test!");
        });

        module("Other tests");

        test("Other test", function() {
            ok(true, "ok");
        });
    };

    return run;

});
