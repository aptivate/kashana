define([
    "views/input_view",
    "views/result/container",
], function (Editable, ResultView) {
    describe("Waffle Tests", function() {
        beforeEach(function() {
            waffle = {
                switch_is_active: function(name) {
                }
            };
        });

        it("ResultView resultContribution subview null when impact weighting disabled", function() {
            spyOn(waffle, "switch_is_active").and.returnValue(false);

            var resultView = new ResultView({model: {}});
            var contribution = resultView.subviewCreators.resultContribution();

            expect(waffle.switch_is_active).toHaveBeenCalledWith("enable impact weighting");
            expect(contribution).toEqual(null);
        });

        it("ResultView resultContribution subview created when impact weighting enabled", function() {
            spyOn(waffle, "switch_is_active").and.returnValue(true);

            spyOn(Editable.prototype, "initialize").and.stub();
            var resultView = new ResultView({model: {}});
            var contribution = resultView.subviewCreators.resultContribution();

            expect(waffle.switch_is_active).toHaveBeenCalledWith("enable impact weighting");
            expect(contribution).toEqual(jasmine.any(Editable));
        });

    });
});
