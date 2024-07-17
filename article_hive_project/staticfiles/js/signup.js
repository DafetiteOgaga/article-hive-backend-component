// JavaScript file: js/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const textElement = document.querySelector('.signup');
    const text = "Sign-up NOW to start making Posts!";
    let index = 0;
    const typingSpeed = 100; //speed

    function typeText() {
        if (index < text.length) {
            textElement.textContent += text.charAt(index);
            index++;
            setTimeout(typeText, typingSpeed);
        } else {
            setTimeout(resetAndTypeText, 2000);  // Pauses the cursor before restarting
        }
    }

    function resetAndTypeText() {
        textElement.textContent = '';
        index = 0;
        typeText();
    }

    typeText();
});
