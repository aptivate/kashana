define([
    'jquery',
    'views/base_view',
    'pen',
], function ($, BaseView, Pen){

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
                dateFormat: "yy-mm-dd",
            }).removeClass("addpicker");
        },

        addUpdate: function () {
            var attrs = {};
            this.$('[name="code"], [name="date"]').each(function (i, el) {
                var $el = $(el);
                attrs[$el.attr("name")] = $el.val();
            });
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
            data.today = year + '-' +
                         (month < 10 ? "0" + month : month) + '-' +
                         (date < 10 ? "0" + date : date);
            data.codes = Aptivate.data.statuscodes;
            return data;
        }
    });

    return StatusUpdateView;
});
