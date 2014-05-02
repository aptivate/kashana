define([
    'underscore',
    'backbone'
], function (_, Backbone) {
    var StaticListView = Backbone.View.extend({
        tagName: 'ul',

        initialize: function (options) {
            // Expected options:
            // 'collection' -- a collecttion of the list item models
            // 'itemView' -- a view to use to render the items
            _.extend(this, _.pick(options, 'itemView', 'collection'));

            this.listenTo(this.collection, 'add', this.addItem);
            this.listenTo(this.collection, 'reset', this.render);
        },

        addItem: function (item) {
            // TODO: re-use existing sub-views if possible?
            var view = new this.itemView({ model: item });
            this.$el.append(view.render().el);
        },

        addAll: function () {
            this.collection.each(this.addItem, this);
        },

        render: function () {
            this.$el.html('');
            this.addAll();
            return this;
        },

    });
    return StaticListView;
});
