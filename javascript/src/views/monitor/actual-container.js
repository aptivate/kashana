define([
    'backbone',
    'views/base_view',
    'views/editable/input',
    'views/editable-text'
], function (Backbone, BaseView, Editable, EditableText) {
    var ResultView = BaseView.extend({
        template_selector: "#monitor-actual-container",

        initialize: function () {
            Backbone.Subviews.add(this);
        },

        subviewCreators: {
            valueView: function (){
                return new Editable({
                    attributes: { class: "value" },
                    model: this.model,
                    field_name: 'value',
                });
            },
            evidenceView: function () {
                return new EditableText({
                    attributes: { class: "evidence" },
                    template_selector: "#monitor-actual-evidence",
                    model: this.model,
                    field_name: 'evidence',
                });
            },
        }

    });

    return ResultView;
});
