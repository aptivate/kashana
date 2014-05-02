define([
    'views/input_view',
], function (Editable) {
    var Selectable = Editable.extend({
        template_selector: "#editable-field",

        events: {
            "click .editable": "changeElement",
            "blur .savable":  "commitEdit",
            "change .savable":  "commitEdit",
            "keyup .savable": "cancelOnEscape",
            "keypress .savable": "updateOnEnter",
        },

        // which fields from choice objects (options)
        // to use as value and text? Overwrite by passing
        // options_map when creating Selectable.
        defaultMap: {
            value: 'id',
            text: 'name'
        },

        inputElement: function (name, value) {
            var sel = $('<select>', {
                    value: value,
                    name: name,
                    class: "editable-input"
                }),
                choices = this.options.options || [],
                map = this.options.options_map || this.defaultMap;
            $(choices).each(function (i, choice) {
                $("<option>", {
                    value: choice[map.value],
                    text: choice[map.text],
                    selected: value &&
                        value.toString() === choice[map.value].toString()
                }).appendTo(sel);
            });
            return sel;
        },

        getDisplayValue: function (value) {
            var displayValue = "",
                choices = this.options.options || [],
                map = this.options.options_map || this.defaultMap;
            $(choices).each(function (i, choice) {
                if (value &&
                        choice[map.value].toString() === value.toString()) {
                    displayValue = choice[map.text];
                    return false;
                }
            });
            return displayValue;
        },

        getTemplateData: function (data) {
            var field_name = this.options.field_name,
                new_data = {
                    field_name: field_name,
                    name: this.options.name || "",
                    value: this.getDisplayValue(data[field_name])
                };
            return new_data;
        },

    });

    return Selectable;
});
