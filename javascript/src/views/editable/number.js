define([
    'views/base_view',
    'views/editable/input',
    'views/display-number',
], function (BaseView, EditableInput, displayNumber) {
    var EditableNumber = EditableInput.extend({
        displayValue: displayNumber,

        getElementValue: function (el) {
            var value = el.value.split(".");
            value.length = value.length > 1 ? 2 : 1;
            value[1] = value[1] || "00";
            value[1] = value[1].slice(0, 2);
            return value.join(".");
        }
    });

    return EditableNumber;
});
