define(function () {
    function displayValue(value) {
        var parts;
        if (value) {
            parts = value.toString().split(".");
            parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            if (parts.length > 1) {
                parts.length = 2;
                parts[1] = parts[1].slice(0, 2);
                if (parts[1].length === 1) {
                    parts[1] += "0";
                }
            }
            return parts.join(".");
        } else {
            return value;
        }
    }

    return displayValue;
});
