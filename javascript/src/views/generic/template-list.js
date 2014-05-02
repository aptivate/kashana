define([
    'underscore',
    'views/base_view'
], function (_, BaseView ) {
    var TemplateList = BaseView.extend({
        template_selector: "#list-view",

        // Expected options
        // 'collection' -- a collecttion of the list-item models
        // 'itemView' -- a view to use to render the items
        initialize: function (options) {
            Backbone.Subviews.add(this);
            _.extend(this, _.pick(options, 'itemView', 'collection'));
            this.listenTo(this.collection, 'add', this.render);
            this.listenTo(this.collection, 'reset', this.render);
        },

        // What list items do we want to render?
        // by default, everything in the collection.
        listItems: function () {
            return this.collection;
        },
        
        // what data per-item do we want in the items collection?
        // by default, the model's json
        itemTemplateData: function (item) {
            return item.toJSON();
        },

        getTemplateData: function (data) {
            var templateData = data || {};
            templateData.items = this.listItems().map(function (item) {
                return this.itemTemplateData(item);
            }, this);
            return templateData;
        },

        // Define unique subview ids for Backbone.subviews to use as its cache keys
        getSubviewId: function ($placeholder) {
            return $placeholder.data('subview-id');
        },

        // assume every model has an id (i.e. not isNew())
        // and that data-subview-id is set to that id
        getItemFor: function (placeholder) {
            var itemId = placeholder.attr('data-subview-id'),
                item = this.collection.get(itemId);
            if (itemId === undefined) {throw "Placeholder element must defined data-subview-id";}
            if (item === undefined) {throw  "Can't find item for placeholder, id: " + itemId;}
            return item;
        },

        subviewCreators: {
            itemView: function (placeholder) {
                return new this.itemView({
                    model: this.getItemFor(placeholder),
                });
            },
        },

    });
    return TemplateList;
});
