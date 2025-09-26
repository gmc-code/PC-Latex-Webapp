document.addEventListener('DOMContentLoaded', function () {
    const inputNames = ['vmargin', 'hmargin'];

    inputNames.forEach(name => {
        const input = document.querySelector(`input[name="${name}"]`);
        if (input) {
            const min = parseFloat(input.min);
            const max = parseFloat(input.max);

            // Show red border if out of range while typing
            input.addEventListener('input', function () {
                let val = parseFloat(this.value);
                if (!isNaN(val) && (val < min || val > max)) {
                    this.style.borderColor = 'red';
                } else {
                    this.style.borderColor = '';
                }
            });

            // Clamp value when user leaves the field
            input.addEventListener('blur', function () {
                let val = parseFloat(this.value);
                if (!isNaN(val)) {
                    if (val < min) this.value = min;
                    if (val > max) this.value = max;
                }
                this.style.borderColor = ''; // Reset border after clamping
            });
        }
    });
});


