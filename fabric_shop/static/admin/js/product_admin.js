document.addEventListener('DOMContentLoaded', function () {
    const hasVariantsCheckbox = document.querySelector('#id_has_variants');

    const fieldsToToggle = [
        { selector: '.form-row.field-quantity', field: '#id_quantity' },
        { selector: '.form-row.field-price', field: '#id_price' },
        { selector: '.form-row.field-color', field: '#id_color' },
        { selector: '.form-row.field-size', field: '#id_size' },
        { selector: '.form-row.field-image', field: '#id_image' },
        { selector: '.form-row.field-unit_of_measurement', field: '#id_unit_of_measurement' }
    ];

    function toggleFields() {
        fieldsToToggle.forEach(({ selector, field }) => {
            const fieldRow = document.querySelector(selector);
            const inputField = document.querySelector(field);
            if (fieldRow && inputField) {
                if (hasVariantsCheckbox.checked) {
                    fieldRow.style.display = 'none';
                    inputField.removeAttribute('required');
                } else {
                    fieldRow.style.display = '';
                    inputField.setAttribute('required', 'required');
                }
            }
        });
    }

    function toggleInline() {
        const inlineWrapper = document.querySelector('.inline-related');
        if (hasVariantsCheckbox.checked && inlineWrapper) {
            inlineWrapper.style.display = 'block';
        } else if (inlineWrapper) {
            inlineWrapper.style.display = 'none';
        }
    }

    if (hasVariantsCheckbox) {
        hasVariantsCheckbox.addEventListener('change', function() {
            toggleFields();
            toggleInline();
        });
        toggleFields();  // initial state
        toggleInline();  // initial state
    }
});
