try {
    const newPassword1 = document.getElementById('id_new_password1');
    const newPassword2 = document.getElementById('id_new_password2');

    newPassword1.addEventListener('input', checkPasswordMatch);
    newPassword2.addEventListener('input', checkPasswordMatch);

    const passwordMatchMessage = document.getElementById('password-match-message');

    function checkPasswordMatch() {
        passwordMatchMessage.textContent = '';
        if (newPassword1.value === '' && newPassword2.value === '') {
            passwordMatchMessage.textContent = '';
        } else {
            if (newPassword1.value === newPassword2.value) {
                if (newPassword2.value.length < 8) {
                    passwordMatchMessage.textContent = 'Password must be at least 8 characters long.';
                } else if (!(/\d/.test(newPassword2.value))) {
                    passwordMatchMessage.textContent = 'Password contain at least one number.';
                } else if (!(/[a-z]/.test(newPassword2.value))) {
                    passwordMatchMessage.textContent = 'Password must contain at least one lowercase letter.';
                } else if (!(/[A-Z]/.test(newPassword2.value))) {
                    passwordMatchMessage.textContent = 'Password must contain at least one uppercase letter.';
                } else {
                    passwordMatchMessage.textContent = 'Passwords match and meet strength requirements.';
                    passwordMatchMessage.style.color = '#001f3f';
                }
            } else {
                passwordMatchMessage.textContent = 'Passwords do not match.';
                passwordMatchMessage.style.color = 'red';
            }
            passwordMatchMessage.style.height = 'auto';
            passwordMatchMessage.style.overflow = 'visible';
        }
    }
} catch (e) {}