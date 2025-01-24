document.addEventListener('DOMContentLoaded', function () {
    const startBtn = document.getElementById('Generate');

    startBtn.addEventListener('click', function (event) {
        // Prevent default form submission temporarily to allow progress bar animation
        event.preventDefault();

        // Show the progress bar and start the animation immediately
        startProgress();

        // Delay the form submission to allow the progress bar animation to start
        setTimeout(function() {
            // Submit the form after the progress bar starts animating
            document.querySelector("form").submit();
        }, 10); // Short delay to ensure progress bar starts animating before submission
    });
});

function startProgress() {
    const progressBar = document.getElementById('progress-bar');
    const progress = document.querySelector('.progress');

    // Reset width to 0% before showing the progress bar (to prevent initial progress display)
    progress.style.width = '0%';

    // Immediately make the progress bar visible and trigger animation
    progressBar.style.visibility = 'visible';
    progressBar.style.opacity = 1;

    // Start the progress bar animation (this can be adjusted for your case)
    let width = 0;
    const interval = setInterval(function() {
        if (width >= 100) {
            clearInterval(interval);
            // After the progress reaches 100%, trigger the fade-out effect
            fadeOutAndHide(progressBar);
        } else {
            width += 1; // Increment the width (you can adjust the speed here)
            progress.style.width = `${width}%`;  // Ensure percentage is appended correctly
        }
    }, 60); // Update progress in ms (adjust timing for speed)
}

function fadeOutAndHide(element) {
    const progress = document.querySelector('.progress');

    // Start fading out the element (opacity to 0)
    let opacity = 1;
    const fadeInterval = setInterval(() => {
        if (opacity <= 0) {
            clearInterval(fadeInterval);
            // Once faded out, reset the progress bar width to 0% and hide the element
            progress.style.width = '0%';
            element.style.visibility = 'hidden';
            element.style.opacity = 0; // Ensure element is fully hidden
        } else {
            opacity -= 0.05; // Reduce opacity in 20 steps
            element.style.opacity = opacity;
        }
    }, 25); // Fade out in ms (adjust interval for speed)
}
