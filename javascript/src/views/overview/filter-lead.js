define([
        'backbone',
        'jquery',
        'views/base_view',
], function (Backbone, $, BaseView) {
    var LeadView = BaseView.extend({
        tagName: "span",
        id: "filter-lead",
        template_selector: "#lead-select",

        events: {
            "change .filter-lead": "filterLead",
        },

        filterLead: function (e) {
            var id = e.target.value;
            this.setVisibility(id);
        },

        setVisibility: function (id) {
            // Don't use jQuery remove because it removes handlers
            var $d = $(".result-tree > .result-overview").detach();

            // Always reset state first
            $d.find(".result-overview, .activity-item")
                .removeClass("empty");
            $d.find(".selected-activity")
                .removeClass("selected-activity");

            // Make a selection if there is one
            if (id) {

                $d.find(".result-overview, .activity-item")
                    .addClass("empty");
                $d.find('.activity-item [data-lead="'+id+'"]')
                    .addClass("selected-activity")
                    .parents(".result-overview, .activity-item")
                    .removeClass("empty");
            }
            $d.appendTo(".result-tree");
        },

        getTemplateData: function () {
            var lead_list = [{
                id: "",
                name: "any"
            }].concat(Aptivate.data.users.slice());

            return {
                option_list: lead_list
            };
        },

        initialize: function () {
            this.listenTo(Aptivate.logframe.activities, "change:lead", function () {
                this.$(".filter-lead").change();
            });
        }
    });

    return LeadView;
});
