define([
    'underscore',
    'backbone',
    'views/generic/template-list'
], function (_, Backbone, TemplateList) {

    // Expected options:
    var addOneListOptions = [
            'itemView',        // a collecttion of the list item models
            'collection',      // a view to use to render the items
            'newModelOptions', // extra options to pass when adding new models
            'maxLength',       // when the list has this many items stop showing the unsaved one
            'itemViewOptions'  // extra options to pass when creating item views
        ];

    var AddOneListView = TemplateList.extend({

        template_selector: "#addone-list-view",

        initialize: function (options) {
            Backbone.Subviews.add(this);
            _.extend(this, _.pick(options, addOneListOptions));
            _.bindAll(this, 'emptyItemSaved');
            this.listenTo(this.collection, 'add', this.itemAdded);
            this.listenTo(this.collection, 'reset', this.listReset);
        },

        // if we get a reset, the unsaved item might be removed from the collection
        // pop it back in (the add triggers a render)
        listReset: function() {
            if (!this.collection.contains(this.unsavedItem)) {
                this.collection.add(this.unsavedItem);
            }
        },

        // Don't re-draw on add if we're adding the unsaved item
        itemAdded: function (model, collection, options) {
            if (!options.addoneUnsaved){
                this.render();
            }
        },

        // assume either every model has an id specified by data-subview-id
        // or data-subview-id="new" and we're using a new unsaved item
        getItemFor: function (itemId) {
            if (itemId !== "new") {
                return this.collection.get({id: itemId});
            } else {
                return this.addEmptyItem();
            }
        },

        // If you need to pass arguments to Model instantiation set
        // newModelOptions which can be a function that returns the
        // options, e.g:
        //
        // newModelOptions: function (){
        //      return { parent: this.options.parent.get('id') };
        // }
        addEmptyItem: function() {
            if (this.unsavedItem === undefined || !this.unsavedItem.isNew()) {
                var modelOptions = _.result(this, 'newModelOptions') || {};
                this.unsavedItem = this.collection.add(
                    modelOptions,
                    {addoneUnsaved: true}
                );
                this.unsavedItem.on('sync', this.emptyItemSaved);
            } else if (!this.collection.contains(this.unsavedItem)) {
                this.collection.unshift(this.unsavedItem, {addoneUnsaved: true});
            }
            return this.unsavedItem;
        },

        // The formerly unsaved item was just saved.
        // It's now cached erroneously as 'new', so we remove that;
        // then render to get a new unsaved item displayed.
        emptyItemSaved: function(itemJustSaved) {
            itemJustSaved.off('sync', this.emptyItemSaved);
            delete this.subviews.new;
            this.render();
        },

        // Only include non-new items in the rendered list -- the template
        // can ask for the new one explicitly.
        // TODO: this could be controlled by an option in future.
        listItems: function () {
            return this.collection.filter(function (item) {
                return !item.isNew();
            });
        },

        subviewCreators: {
            itemView: function (placeholder) {
                var itemId = placeholder.attr('data-subview-id'),
                    viewOptions;
                if (itemId === "new" &&
                        this.collection.length >= this.maxLength){
                    return null; // Don't show empty item
                }
                viewOptions = _.extend({}, this.itemViewOptions, {
                    model: this.getItemFor(itemId)
                });
                return new this.itemView(viewOptions);
            },
        },

    });

    return AddOneListView;
});
