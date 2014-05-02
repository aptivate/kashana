define(function () {
    return {
        // Miliseconds to wait before removing feedback class
        removeDelay: 2000,

        loadingFeedback: function (selector, class_name, keepClass) {
            return function () {
                var $el = this.$(selector);
                if (this.saveFlag) {
                    $el.addClass(class_name)
                        .parents(".in-progress").removeClass("in-progress");
                    this.saveFlag = false;

                    if (!keepClass) {
                        setTimeout(function () {
                            $el.removeClass(class_name);
                        }, this.removeDelay);
                    }
                }
            };
        },

        attachFeedback: function (sel) {
            var selector = sel || ".editable";

            // Used for distinguishing fields that triggered the change
            this.saveFlag = false;
            this.listenTo(this.model, "request", function () {
                if (this.saveFlag) {
                    this.$el.addClass("in-progress");
                }
            });
            this.listenTo(this.model, "error",
                          this.loadingFeedback(selector, "error", true));
            this.listenTo(this.model, "sync",
                          this.loadingFeedback(selector, "success"));
        }
    };
});
