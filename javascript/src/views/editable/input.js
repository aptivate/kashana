define([
    'views/input_view',
], function (Editable) {

    var EditableInput = Editable.extend({

        template_selector: "#editable-field",

        displayValue: function (value) {
            return value;
        },

        getTemplateData: function (data) {
            var name = this.options.field_name || this.field_name,
                new_data = {
                    field_name: name,
                    name: name,
                    value: this.displayValue(data[name])
                };
            return new_data;
        },

    });

    return EditableInput;
});
