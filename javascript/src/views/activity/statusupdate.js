define([
    'jquery',
    'views/base_view',
    'utils/clean-date',
    'pen',
], function ($, BaseView, cleanDate, Pen){

    var StatusUpdateView = BaseView.extend({
        template_selector: '#activity-statusupdate',

        events: {
            "click .add": "addUpdate",
            "click .cancel": "cancelUpdate",
            "mouseover .addeditor": "addEditor",
            "focus .addpicker": "addPicker"
        },

        addEditor: function (e) {
            new Pen({
                editor: e.target,
                class: "pen-editor",
                list: ['bold', 'italic', 'createlink'],
                textarea: '<textarea name="description"></textarea>'
            });
            $(e.target).removeClass("addeditor");
        },

        addPicker: function (e) {
            // Add date picker on first focus
            $(e.target).datepicker({
                dateFormat: "dd/mm/yy",
            }).removeClass("addpicker");
        },

        addUpdate: function () {
            var attrs = {};
            this.$('[name="code"], [name="date"]').each(function (i, el) {
                var $el = $(el);
                attrs[$el.attr("name")] = $el.val();
            });
            if (attrs.date) {
                attrs.date = cleanDate(attrs.date);
            }
            if (attrs.code) {
                attrs.code = parseInt(attrs.code, 10);
            }
            attrs.description = this.$(".description").html();
            attrs.activity = this.model.get("id");
            this.collection.create(attrs, {wait: true});
            this.render();
        },

        cancelUpdate: function () {
            this.$('[name="description"], [name="date"]').val("");
            this.$('[name="code"]')[0].selectedIndex = 0;
        },

        getTemplateData: function (data) {
            var today = new Date(),
                year = today.getFullYear(),
                month = today.getMonth() + 1,
                date = today.getDate();
            data.today = [
                (date < 10 ? "0" + date : date),
                (month < 10 ? "0" + month : month),
                year
            ].join("/");
            data.codes = Aptivate.data.statuscodes;
            return data;
        }
    });

    return StatusUpdateView;
});
