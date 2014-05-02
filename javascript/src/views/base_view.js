define([
    'underscore',
    'handlebars',
    'backbone',
    'views/permission-mixin',
    'backbone_subviews',  // So inherited views can use it
], function (_, Handlebars, Backbone, PermissionMixin) {
    var BaseView = Backbone.View.extend(PermissionMixin).extend({

        constructor: function (options) {
            // add 'template_selector' option to instances (if provided) but
            // let subclasses override 'initialize' without blathering this
            // behaviour
            Backbone.View.apply(this, arguments);
            this.options = options;
            _.extend(this, _.pick(options, 'template_selector'));
        },

        getTemplate: function () {
            // Templates are precompiled with gulp (gulp templates) and stored
            // on Aptivate.data.templates
            var name = this.template_selector.slice(1);
            this.viewTpl = Aptivate.data.templates[name];
            return this.viewTpl;
        },

        render: function () {
            var template = this.getTemplate(),
                modelJson = this.model ? this.model.toJSON(): {},
                data = this.getTemplateData ? this.getTemplateData(modelJson) : modelJson;

            // Add global values
            data.editable = this.is_editable;

            this.$el.html(template(data));
            return this;
        }
    });
    return BaseView;
});
