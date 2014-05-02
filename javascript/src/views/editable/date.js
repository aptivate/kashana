define([
    'views/input_view',
], function (Editable) {
    function formatDate(date) {
        return date;
    }

    var EditableDate = Editable.extend({

        template_selector: "#editable-date",
    
        events: {
            "click .editable": "changeElement",
            "change .savable":  "commitEdit",
            "keyup .savable": "cancelOnEscape",
            "keypress .savable": "updateOnEnter",
        },

        inputElement: function (name, value) {
            var inp = $('<input>', {
                value: formatDate(value),
                name: name,
                placeholder: "YYYY-MM-DD",
                class: "editable-input"
            })
            .datepicker({
                dateFormat: "yy-mm-dd",
            });
            return inp;
        },

        getTemplateData: function (data) {
            var name = this.options.field_name,
                new_data = {
                    name: name,
                    value: formatDate(data[name]) || ""
                };
            return new_data;
        },

    });

    return EditableDate;
});
