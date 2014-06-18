define([
    'jquery',
    'views/editable/cleaninput-mixin',
], function ($, Mixin) {
    function createSet(list) {
        var set = {};
        $.each(list, function (i, el) {
            set[el] = true;
        });
        return set;
    }

    var keep = createSet(Mixin.keep_tags);

    return function () {
        module("processNode");

        test("Test processNode works on text node", function () {
            var text = 'Node has text',
                node = document.createTextNode(text),
                result;

            result = Mixin.processNode(node, keep);

            ok(result.nodeValue === text);
        });

        test("Test processNode works on tags to keep", function () {
            var text = 'Node has text',
                $el = $('<p class="class1" onclick="true">'+text+'</p>'),
                result;

            ok($el.hasClass("class1"));
            ok(!!$el[0].onclick);

            result = Mixin.processNode($el[0], keep);

            ok(result.innerHTML === text);
            equal(result.nodeName.toLowerCase(), "p");
            ok(!result.className);
        });

        test("Test processNode works filters non-keepable tags", function () {
            var text = 'Node has text',
                $el = $('<div class="class1" onclick="true">'+text+'</div>'),
                result;

            ok($el.hasClass("class1"), "Has a class");
            ok(!!$el[0].onclick, "Has an onclick handler");

            result = Mixin.processNode($el[0], keep);

            ok(result.nodeType === 11, "Is now a document fragment");
            ok(result.childNodes.length === 1, "Fragment has only one child node");
            ok(result.firstChild.nodeValue === text, "Has the right content");
            ok(!$(result).hasClass("class1"), "Removed class");
            ok(!result.onclick, "onclick handler is gone");
        });

        test("Test processNode keeps unkeepable tag if marked wrapper", function () {
            var text = 'Node has text',
                $el = $('<div class="class1" onclick="true">'+text+'</div>'),
                result;

            ok($el.hasClass("class1"), "Has class");
            ok(!!$el[0].onclick, "Has onclick handler");

            result = Mixin.processNode($el[0], keep, true);

            equal(result.nodeName.toLowerCase(), "div",
                "Still div that is otherwise not allowed");
            ok(!$(result).hasClass("class1"), "Removed class");
            ok(!result.onclick, "Removed onclick handler");
            ok(result.childNodes.length === 1, "Has only one child");
            ok(result.firstChild.nodeValue === text,
                "...which has the correct value");
        });

        test("Test links keep href value", function () {
            var $el = $('<a href="http://aptivate.org">Aptivate</a>'),
                result;

            equal($el.attr("href"), "http://aptivate.org", "Link has the correct href value");

            result = Mixin.processNode($el[0], keep);

            equal($(result).attr("href"), "http://aptivate.org", "Link still points to the same source");
        });


        module("cleanInput");

        test("Test removing of classes and other attributes", function () {
            var dirty = 'Some <span>like</span> it <b class="strong">hot</b> and some <em data-bla="5">not</em>.',
                clean = 'Some like it <b>hot</b> and some <em>not</em>.';

            equal(Mixin.cleanInput(dirty), clean, "Classes and attributes were removed");
        });
    };
});
