define([
    'jquery',
], function ($) {
    function toggleDelete(prop_value, button_selector) {
        $(this).toggleClass('pure-button-hidden')
               .parent()
                    .find('.field-clear-hidden-input input')
                        .prop('checked', prop_value)
                    .end()
                    .find(button_selector)
                        .toggleClass('pure-button-hidden')
                    .end()
                    .find('.field-clear-initial')
                        .children().toggleClass('deleted');
    }
    // Handlers
    $('.field-clear-check-button').click(function(e) {
        toggleDelete.call(this, true, '.field-clear-cancel');
    });
    $('.field-clear-cancel').click(function(e) {
        toggleDelete.call(this, false, '.field-clear-check-button');
    });
});
