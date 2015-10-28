define(function () {
    // Function for nicely displaying dates passed as either ISO date
    // strings (YYYY-MM-DD) or Date objects
    //
    // Returns original value otherwise (NEVER return error)
    function displayDate(value) {
        var bits;
        if (value && value.toISOString) { // Date object
            value = value.toISOString();
        }
        if (typeof(value) === "string") {
            bits = value.split("T")[0].split("-");
            if (bits.length === 3) {
                value = [bits[2], bits[1], bits[0]].join("/");
            }
        }
        return value;
    }

    return displayDate;
});
