define([
    'backbone',
    'views/editable/date',
    'views/base_view',
], function (Backbone, EditableDate, BaseView) {
    var MonitorColumnHeadingView = BaseView.extend({
        tagName: 'th',
        attributes: { class: 'actual' },
        template_selector: '#monitor-heading',

        initialize: function () {
            Backbone.Subviews.add(this);
        },

        subviewCreators: {
            dateEditor: function () {
                return new EditableDate({
                    model: this.model,
                    field_name: 'date'
                });
            }
        }
    });

    return MonitorColumnHeadingView;
});
