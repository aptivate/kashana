define([
    'underscore', 'backbone', 'jquery', 'views/generic/list',
], function (_, BB, $, AddOneList) {
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

        describe("Basic rendering", function() {

        it("Elements in collection rendered", function() {
            var listView = new MyListView({
                collection: new BB.Collection(models)
            });

            listView.render();
            
            var assertionCount = 0
            listView.$el.children("div").each(function (i, el) {
                var contents = $(el).html();
                if (contents==="empty") {
                	since("blank element included");
                	expect(true).toBe(true);
                	assertionCount++;
                } else {
                    expect(_.contains(ids, contents, "ID rendered is from list")).toBe(true);
                    assertionCount++;
                }
            });
            expect(assertionCount).toEqual(4);
        })});

        describe("Max-size", function() {

        it("No blank element if max size reached", function() {
            var listView = new MyListView({
                maxLength: 3,
                collection: new BB.Collection(models)
            });
            listView.render();
            
            var assertionCount = 0;
            listView.$el.children("div").each(function (i, el) {
                var contents = $(el).html();
                if (contents==="empty") {
                	since("blank element should not be included");
                    expect(false).toBe(true);
                } else if (contents === "") {
                	since("Empty placeholder div, but no view");
                    expect(true).toBe(true);
                    assertionCount++;
                } else {
                    expect(_.contains(ids, contents, "ID rendered is from list")).toBe(true);
                    assertionCount++;
                }
            });
            expect(assertionCount).toEqual(4);
        });

        it("Blank element if max size not yet reached", function() {
            var listView = new MyListView({
                maxLength: 4,
                collection: new BB.Collection(models)
            });
            listView.render();
            
            var assertionCount = 0;
            listView.$el.children("div").each(function (i, el) {
                var contents = $(el).html();
                if (contents==="empty") {
                    expect(true).toBe(true);
                    assertionCount++;
                } else if (contents === "") {
                    expect(false).toBe(true);
                } else {
                    expect(_.contains(ids, contents, "ID rendered is from list")).toBe(true);
                    assertionCount++;
                }
            });
            expect(assertionCount).toEqual(4);
        })});

        describe("itemViewOptions", function() {

        it("Test passing itemViewOptions", function () {
            var listView = new MyListView({
                itemViewOptions: { tagName: 'span' },
                collection: new BB.Collection(models)
            });
            listView.render();
            
            // Jasmine has no default way to count the number of assertions, 
            // So I'm adding something manually.
            var assertionCount = 0;
            listView.$el.children("span").each(function () {
            	since("it's a span")
                expect(true).toBe(true);
                assertionCount++;
            });
            expect(assertionCount).toEqual(4);
        })});
});