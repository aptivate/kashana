define([
        'backbone',
        'jquery',
        'views/base_view',
        'views/generic/list',
        'views/overview/filter-lead',
        'views/overview/utils/container-mixin',
        'views/result/overview_item',
        'views/overview/export-data',
        'views/overview/annual-plan',
        'views/overview/quarter-plan',
], function (Backbone, $, BaseView, ListView, LeadView, ContainerMixin,
             OverviewItem, ExportView, ExportAnnualPlanView,
             ExportQuarterPlanView) {
    var OverviewContainer = BaseView.extend(ContainerMixin).extend({
        template_selector: "#overview-container",

        events: {
            "focus .date.addpicker": "createPicker",
            "focus .date": "limitPicker",
            "click #filter-clear": "clearSelection",
            "change .date": "filterTime",
        },

        // Listeners
        createPicker: function (e) {
            // Add date picker on first focus
            $(e.target).datepicker({
                dateFormat: "yy-mm-dd",
            }).removeClass("addpicker");
        },

        clearSelection: function () {
            $("#filter-time .date, #filter-by-lead")
                .val("")
                .change();
        },

        filterTime: function () {
            var start = $("#filter-time-start").val(),
                end = $("#filter-time-end").val() || this.BiggestDate;

            this.setVisibility(start, end);
        },

        limitPicker: function (e) {
            var $el = $(e.target),
                limit = this.getDateLimit($el);
            if (limit) {
                $el.datepicker("option", limit);
            }
        },

        // INIT
        initialize: function () {
            this.collection = Aptivate.logframe.results.subcollection({
                filter: function (result) {
                    return result.get("parent") === null;
                }
            });
            Backbone.Subviews.add(this);

            this.listenTo(Aptivate.logframe.activities, "change:start_date", function () {
                this.$("#filter-time-start").change();
            });
            this.listenTo(Aptivate.logframe.activities, "change:end_date", function () {
                this.$("#filter-time-end").change();
            });
        },
        subviewCreators: {
            "leadSelect": function () {
                return new LeadView({
                    // Required by BaseView, but not used
                    model: new Backbone.Model()
                });
            },
            "resultList": function () {
                return new ListView({
                    className: "result-tree",
                    maxLength: 1,
                    itemView: OverviewItem,
                    collection: this.collection,
                    newModelOptions: {
                        log_frame: this.model.get('id'),
                        level: this.model.get('level')
                    }
                });
            },
            "exportData": function () {
                return new ExportView({
                    // Required by BaseView, but not used
                    model: new Backbone.Model()
                });
            },
            "exportAnnualPlan": function () {
                return new ExportAnnualPlanView({
                    // Required by BaseView, but not used
                    model: new Backbone.Model()
                });
            },
            "exportQuarterPlan": function () {
                return new ExportQuarterPlanView({
                    // Required by BaseView, but not used
                    model: new Backbone.Model()
                });
            }
        }
    });

    return OverviewContainer;
});
