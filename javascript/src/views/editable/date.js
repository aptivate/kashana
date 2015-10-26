define([
    'views/input_view',
    'utils/display-date',
    'utils/clean-date',
], function (Editable, displayDate, cleanDate) {
    var EditableDate = Editable.extend({

        template_selector: "#editable-date",

        events: {
            "click .editable": "changeElement",
            "change .savable":  "commitEdit",
            "keyup .savable": "cancelOnEscape",
            "keypress .savable": "updateOnEnter",
        },

        inputElement: function (name, value) {
            var options = this.getOptions(),
                inp = $('<input>', {
                    value: displayDate(value),
                    name: name,
                    placeholder: "DD/MM/YYYY",
                    class: "editable-input"
                });
            inp.datepicker(options);
            return inp;
        },

        getOptions: function () {
            var related,
                options = {
                    dateFormat: "dd/mm/yy"
                };

            if (_.has(this.options, 'related')) {
                related = _.pairs(this.options.related);
            }

            _.each(related, function (e) {
                var value = this.get(e[1]),
                    opt = e[0];
                if (value) {
                    options[opt] = displayDate(value);
                }
            }, this.model);

            return options;
        },

        cleanInput: cleanDate,

        getTemplateData: function (data) {
            var name = this.options.field_name,
                new_data = {
                    name: name,
                    value: displayDate(data[name]) || ""
                };
            return new_data;
        },

    });

    return EditableDate;
});
