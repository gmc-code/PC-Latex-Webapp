document.addEventListener('DOMContentLoaded', function () {
    const numInputs = document.querySelectorAll('input[name="numq"]');

    numInputs.forEach(numInput => {
        const min = parseInt(numInput.min);
        const max = parseInt(numInput.max);

        numInput.addEventListener('input', function () {
            let val = parseInt(this.value);
            if (!isNaN(val)) {
                if (val < min) this.value = min;
                if (val > max) this.value = max;
            }
        });
    });
});
