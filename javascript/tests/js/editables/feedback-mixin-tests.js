define([
    'jquery',
    'backbone',
    'views/editable/feedback-mixin',
], function ($, BB, Mixin) {
    var ctx = $("#qunit-fixture");
    Mixin.removeDelay = 200;
    Mixin.$el = ctx;
    Mixin.$ = $;

    return function () {
        asyncTest("Test loadingFeedback works", function () {
            expect(3);
            Mixin.saveFlag = true;
            feedback = Mixin.loadingFeedback(".editable", "works");

            ok(!$(".editable", ctx).hasClass("works"), "Target element does not have class yet");
            feedback.call(Mixin);
            ok($(".editable", ctx).hasClass("works"), "Target element now has the class");
            setTimeout(function () {
                ok(!$(".editable", ctx).hasClass("works"), "Target element again does not have the class");
                start();
            }, Mixin.removeDelay + 10);
        });

        asyncTest("Test loadingFeedback keeps class when instructed", function () {
            expect(3);
            Mixin.saveFlag = true;
            feedback = Mixin.loadingFeedback(".editable", "works", true);

            ok(!$(".editable", ctx).hasClass("works"), "Target element does not have class yet");
            feedback.call(Mixin);
            ok($(".editable", ctx).hasClass("works"), "Target element now has the class");
            setTimeout(function () {
                ok($(".editable", ctx).hasClass("works"), "Target element still has the class");
                start();
            }, Mixin.removeDelay + 10);
        });

        test("Test attachFeedback attached model listeners", function () {
            var Model = BB.Model.extend({}),
                m = new Model,
                ViewClass = BB.View.extend(Mixin).extend({
                    initialize: function () {
                        this.attachFeedback();
                    }
                }),
                view = new ViewClass({
                    model: m
                });

            ok(!$(".editable", ctx).hasClass("success"), "Target element does not have class yet");

            view.saveFlag = true;
            m.trigger("sync");
            ok($(".editable", ctx).hasClass("success"), "Target element now has the class");
            ok(!view.saveFlag, "saveFlag attribute was resetted.")
        });

        asyncTest("Test attachFeedback attached success listener loses class", function () {
            var Model = BB.Model.extend({}),
                m = new Model,
                ViewClass = BB.View.extend(Mixin).extend({
                    initialize: function () {
                        this.attachFeedback();
                    }
                }),
                view = new ViewClass({
                    model: m
                });
            expect(4);

            ok(!$(".editable", ctx).hasClass("success"), "Target element does not have class yet");

            view.saveFlag = true;
            m.trigger("sync");
            ok($(".editable", ctx).hasClass("success"), "Target element now has the class");
            ok(!view.saveFlag, "saveFlag attribute was resetted.")
            setTimeout(function () {
                ok(!$(".editable", ctx).hasClass("success"), "Target element lost the class");
                start();
            }, Mixin.removeDelay + 10);
        });

        asyncTest("Test attachFeedback attached error listener keeps class", function () {
            var Model = BB.Model.extend({}),
                m = new Model,
                ViewClass = BB.View.extend(Mixin).extend({
                    initialize: function () {
                        this.attachFeedback();
                    }
                }),
                view = new ViewClass({
                    model: m
                });
            expect(4);

            ok(!$(".editable", ctx).hasClass("error"), "Target element does not have class yet");

            view.saveFlag = true;
            m.trigger("error");
            ok($(".editable", ctx).hasClass("error"), "Target element now has the class");
            ok(!view.saveFlag, "saveFlag attribute was resetted.")
            setTimeout(function () {
                ok($(".editable", ctx).hasClass("error"), "Target element kept the class");
                start();
            }, Mixin.removeDelay + 10);
        });
    };
});
