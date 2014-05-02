define([
    'underscore', 'backbone', 'jquery', 'views/generic/list',
], function (_, BB, $, AddOneList) {

    var runtests = function () {
        var ids = ["1", "2", "3"],
            models = _.map(ids, function(n){return {id: n};}),
            MyListView = AddOneList.extend({
                itemView: BB.View.extend({
                    render: function(){
                        var content = this.model.get('id') || "empty";
                        this.$el.html(content);
                    },
                }),
            });

        module("Basic rendering");

        test("Elements in collection rendered", function() {
            var listView = new MyListView({
                collection: new BB.Collection(models)
            });
            expect(4);
            listView.render();
            listView.$el.children("div").each(function (i, el) {
                var contents = $(el).html();
                if (contents==="empty") {
                    ok(true, "blank element included");
                } else {
                    ok(_.contains(ids, contents, "ID rendered is from list"));
                }
            });
        });

        module("Max-size");

        test("No blank element if max size reached", function() {
            var listView = new MyListView({
                maxLength: 3,
                collection: new BB.Collection(models)
            });
            expect(4);
            listView.render();
            listView.$el.children("div").each(function (i, el) {
                var contents = $(el).html();
                if (contents==="empty") {
                    ok(false, "blank element should not be included");
                } else if (contents === "") {
                    ok(true, "Empty placeholder div, but no view");
                } else {
                    ok(_.contains(ids, contents, "ID rendered is from list"));
                }
            });
        });

        test("Blank element if max size not yet reached", function() {
            var listView = new MyListView({
                maxLength: 4,
                collection: new BB.Collection(models)
            });
            expect(4);
            listView.render();
            listView.$el.children("div").each(function (i, el) {
                var contents = $(el).html();
                if (contents==="empty") {
                    ok(true, "blank element should be included");
                } else if (contents === "") {
                    ok(fail, "No empty divs please");
                } else {
                    ok(_.contains(ids, contents, "ID rendered is from list"));
                }
            });
        });

        module("itemViewOptions");

        test("Test passing  itemViewOptions", function () {
            var listView = new MyListView({
                itemViewOptions: { tagName: 'span' },
                collection: new BB.Collection(models)
            });
            expect(4); // TODO
            listView.render();
            listView.$el.children("span").each(function () {
                ok(true, "it's a span");
            });
        });

    };

    return runtests;

});
