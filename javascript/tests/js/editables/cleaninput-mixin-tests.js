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

    describe("processNode", function() {

	    it("Test processNode works on text node", function () {
	        var text = 'Node has text',
	            node = document.createTextNode(text),
	            result;
	
	        result = Mixin.processNode(node, keep);
	
	        expect(result.nodeValue).toBe(text);
	    });
	
	    it("Test processNode works on tags to keep", function () {
	        var text = 'Node has text',
	            $el = $('<p class="class1" onclick="true">'+text+'</p>'),
	            result;
	
	        expect($el).toHaveClass("class1");
	        expect($el[0].onclick).toBeTruthy();
	
	        result = Mixin.processNode($el[0], keep);
	
	        expect(result.innerHTML).toBe(text);
	        expect(result.nodeName.toLowerCase()).toEqual("p");
	        expect(result.className).toBeFalsy();
	    });
	
	    it("Test processNode works filters non-keepable tags", function () {
	        var text = 'Node has text',
	            $el = $('<div class="class1" onclick="true">'+text+'</div>'),
	            result;
	        
	        since("Has a class");
	        expect($el).toHaveClass("class1");
	        
	        since("Has an onclick handler");
	        expect($el[0].onclick).toBeTruthy();
	
	        result = Mixin.processNode($el[0], keep);
	
	        since("Is now a document fragment");
	        expect(result.nodeType).toBe(11);
	        
	        since("Fragment has only one child node");
	        expect(result.childNodes.length).toBe(1);
	        
	        since("Has the right content");
	        expect(result.firstChild.nodeValue).toBe(text);
	        
	        since("Removed class");
	        expect($(result)).not.toHaveClass("class1");
	        
	        since("onclick handler is gone");
	        expect(result.onclick).toBeFalsy();
	    });
	
	    it("Test processNode keeps unkeepable tag if marked wrapper", function () {
	        var text = 'Node has text',
	            $el = $('<div class="class1" onclick="true">'+text+'</div>'),
	            result;
	        
	        since("Has class");
	        expect($el).toHaveClass("class1");
	        
	        since("Has onclick handler");
	        expect($el[0].onclick).toBeTruthy();
	
	        result = Mixin.processNode($el[0], keep, true);
	
	        since("Still div that is otherwise not allowed");
	        expect(result.nodeName.toLowerCase()).toEqual("div");
	        
	        since("Removed class");
	        expect($(result)).not.toHaveClass("class1");
	        
	        since("Removed onclick handler");
	        expect(result.onclick).toBeFalsy();
	        
	        since("Has only one child");
	        expect(result.childNodes.length).toBe(1);
	        
	        since("...which has the correct value");
	        expect(result.firstChild.nodeValue).toBe(text);
	    });
	
	    it("Test links keep href value", function () {
	        var $el = $('<a href="http://aptivate.org">Aptivate</a>'),
	            result;
	        
	        since("Link has the correct href value");
	        expect($el.attr("href")).toEqual("http://aptivate.org");
	
	        result = Mixin.processNode($el[0], keep);
	
	        since("Link still points to the same source");
	        expect($(result).attr("href")).toEqual("http://aptivate.org");
	    });
    });


    describe("cleanInput", function () {
    	it("Test removing of classes and other attributes", function () {
	        var dirty = 'Some <span>like</span> it <b class="strong">hot</b> and some <em data-bla="5">not</em>.',
	            clean = 'Some like it <b>hot</b> and some <em>not</em>.';
	        
	        since("Classes and attributes were removed");
	        expect(Mixin.cleanInput(dirty)).toEqual(clean);
    	});
    });
});
