/**********************************************************************
 *
 * Remote submit - submit form found elsewhere on page
 *
 * Usage: buttons need to link to form they want to submit by having an
 *        attribute 'data-form' that contains a CSS2 selector pointing
 *        to the form.
 *
 * Algorithm:
 * - attach to elements with class 'remote-submit' and add click
 *   handler
 * - when pressed:
 *    - find form
 *    - make a hidden duplicate of the button and add it to the form
 *    - trigger submit by "clicking" on the button
 *
 * Should work in: FF, Chrome, Safari, IE8+
 *
 * Depends on: lib.js or jQuery
 *
 **********************************************************************/
define([
    'jquery',
], function ($) {
    function remoteSubmit() {
        var form = null,
            btn = null;

        if (this.hasAttribute("data-form")) {
            form = $(this.getAttribute("data-form"));
            if (form.length) {
                form = form[0];
                btn = this.cloneNode(true);
                btn.style.display = "none";
                form.appendChild(btn);
                btn.click();
            }
        }
    };

    $(".remote-submit").on("click", remoteSubmit)
                       .addClass("show");
});
