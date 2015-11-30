define([
    'jquery',
    'backbone',
    'views/editable/feedback-mixin',
], function ($, BB, Mixin) {
    var ctx = $("#qunit-fixture");
    Mixin.removeDelay = 200;
    Mixin.$el = ctx;
    Mixin.$ = $;
    
    jasmine.getFixtures().fixturesPath = 'tests/html_fixtures';
    
    function callFeedback(feedback, ctx, done) {
    	feedback.call(Mixin);
    	since("Target element now has the class");
        expect($(".editable", ctx)).toHaveClass("works");
		done();
    }
    
    function triggerModel(view, m, ctx, trigger, elementClass, done) {
    	view.saveFlag = true;
        m.trigger(trigger);
        since("Target element now has the class");
    	expect($(".editable", ctx)).toHaveClass(elementClass);
        since("saveFlag attribute was resetted.");
        expect(view.saveFlag).toEqual(false);
        done();
    }
    
    describe("Test feedback mixin", function() {
    	beforeEach(function(done) {
    		loadFixtures('editables/feedback_mixin.html');
    		ctx = $("#qunit-fixture");
    		done();
    	});
    	
	    it("Test loadingFeedback works", function (done) {
	        var assertionCounter = 0;
	        
	        Mixin.saveFlag = true;
	        feedback = Mixin.loadingFeedback(".editable", "works");
	        since("Target element does not have class yet");
	        expect($(".editable", ctx)).not.toHaveClass("works");
		    assertionCounter++;
		    
		    callFeedback(feedback, ctx, done);
    		assertionCounter++;
    		
	        since("Target element again does not have the class");
	        expect($(".editable", ctx)).not.toHaveClass("works");
	        assertionCounter++;

			expect(assertionCounter).toEqual(3);
	    });
	
	    it("Test loadingFeedback keeps class when instructed", function (done) {
	        var assertionCounter = 0;
	        Mixin.saveFlag = true;
	        feedback = Mixin.loadingFeedback(".editable", "works", true);
	        since("Target element does not have class yet");
	        expect($(".editable", ctx)).not.toHaveClass("works");
	        assertionCounter++;
	        
	        callFeedback(feedback, ctx, done);
	        assertionCounter++;
	        
	       	since("Target element still has the class");
	        expect($(".editable", ctx)).toHaveClass("works");
	        assertionCounter++;
	        
	        expect(assertionCounter).toEqual(3);
	    });
	
	    it("Test attachFeedback attached model listeners", function (done) {
	        var Model = BB.Model.extend({}),
	            m = new Model,
	            ViewClass = BB.View.extend(Mixin).extend({
	                initialize: function () {
	                    this.attachFeedback();
	                }
	            }),
	            view = new ViewClass({
	                model: m
	            });
	
	        since("Target element does not have class yet");
	        expect($(".editable", ctx)).not.toHaveClass("success");
	        
	    	triggerModel(view, m, ctx, "sync", "success", done)	    	
	    });
	
	    it("Test attachFeedback attached success listener loses class", function (done) {
	        var Model = BB.Model.extend({}),
	            m = new Model,
	            ViewClass = BB.View.extend(Mixin).extend({
	                initialize: function () {
	                    this.attachFeedback();
	                }
	            }),
	            view = new ViewClass({
	                model: m
	            });
	        var assertionCounter = 0;
	        
	        since("Target element does not have class yet");
	        expect($(".editable", ctx)).not.toHaveClass("success");
	    	assertionCounter++;
	    
	        triggerModel(view, m, ctx, "sync", "success", done);
	        assertionCounter+=2;
	        
	        since("Target element lost the class");
	        expect($(".editable", ctx)).not.toHaveClass("success");
	        assertionCounter++;
	            
	        expect(assertionCounter).toEqual(4);
	    });
	
	    it("Test attachFeedback attached error listener keeps class", function (done) {
	        var Model = BB.Model.extend({}),
	            m = new Model,
	            ViewClass = BB.View.extend(Mixin).extend({
	                initialize: function () {
	                    this.attachFeedback();
	                }
	            }),
	            view = new ViewClass({
	                model: m
	            });
	        var assertionCounter = 0;
	        
	        since("Target element does not have class yet");
	        expect($(".editable", ctx)).not.toHaveClass("error");
	    	assertionCounter++;
	
	        triggerModel(view, m, ctx, "error", "error", done)
	        assertionCounter += 2;
	        
	        since("Target element kept the class");
	        expect($(".editable", ctx)).toHaveClass("error");
	        assertionCounter++;
	        
	        expect(assertionCounter).toEqual(4);
	    });
    });
});
