document.addEventListener('DOMContentLoaded', function() {
    const textElement = document.querySelector('.signup');
    const texts = [
        "Sign-up NOW to start making Posts!",
        "Get email notifications for posts, comments, replies and more!",
        "This Application was developed with Django, HTML, CSS and JS."
    ];
    let current = 0;
    let index = 0;
    const typingSpeed = 100; // speed of typing
    const pauseDuration = 2000; // pause duration before restarting

    function typeText() {
        if (index < texts[current].length) {
            textElement.textContent += texts[current].charAt(index);
            index++;
            setTimeout(typeText, typingSpeed);
        } else {
            setTimeout(resetAndTypeText, pauseDuration);
        }
    }

    function resetAndTypeText() {
        textElement.textContent = '';
        index = 0;
        current = (current + 1) % texts.length; // cycle through texts
        typeText();
    }

    try {
        typeText();
    } catch (e) {
        console.error("Error in typing animation: ", e);
    }
});
