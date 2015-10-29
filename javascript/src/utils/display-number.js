define(function () {
    // Function for nicely displaying numbers with thousand and decimal
    // separators.
    //
    // TODO: Does not handle e+ notation or rounding of decimals
    function displayNumber(value) {
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
            } else {
                parts.push("00");
            }
            return parts.join(".");
        } else {
            return value;
        }
    }

    return displayNumber;
});
