define(function () {
    // Function cleaning dates from dd/mm/yyyy to ISO representation.
    //
    // Returns original value otherwise (NEVER return error)
    function cleanDate(d) {
        var bits,
            date = d;
        if (typeof(d) === "string") {
            bits = d.split("/");
            if (bits.length === 3) {
                date = [bits[2], bits[1], bits[0]].join("-");
            }
        }
        return date;
    }

    return cleanDate;
});
