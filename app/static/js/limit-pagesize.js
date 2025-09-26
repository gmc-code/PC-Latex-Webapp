document.addEventListener('DOMContentLoaded', function () {
    const inputNames = ['paperheight', 'paperwidth'];

    inputNames.forEach(name => {
        const input = document.querySelector(`input[name="${name}"]`);
        if (input) {
            const min = parseFloat(input.min);
            const max = parseFloat(input.max);

            input.addEventListener('input', function () {
                let val = parseFloat(this.value);
                if (!isNaN(val)) {
                    if (val < min) this.value = min;
                    if (val > max) this.value = max;
                }
            });
        }
    });
});
