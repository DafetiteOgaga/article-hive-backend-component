// JavaScript file: js/scripts.js text

document.addEventListener('DOMContentLoaded', function() {
    const textElement = document.querySelector('.signup');
    const text1 = "Sign-up NOW to start making Posts!";
    const text2 = "Get email notifications for posts, comments, replies and more!";
    let current = true;
    const getText = () => {
        return current ? text1 : text2;
    }
    let index = 0;
    const typingSpeed = 100; //speed

    function typeText() {
        const text = getText()
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
        current = !current
        typeText();
    }

    typeText();
});
