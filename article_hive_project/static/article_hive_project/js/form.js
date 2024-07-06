const form = document.getElementById('form');
const password = document.getElementById('password1');
const password2 = document.getElementById('password2');
const passwordMatchMessage = document.getElementById('password-match-message');
const submitButton = document.getElementById('submit-button');
form.addEventListener('submit', submitHandler);
password.addEventListener('input', checkPasswordMatch);
password2.addEventListener('input', checkPasswordMatch);

// let msg = ''

function checkPasswordMatch() {
	// submitButton.disabled = true;
	// passwordMatchMessage.style.fontStyle = 'italic';
	// passwordMatchMessage.style.color = 'red';
	passwordMatchMessage.textContent = '';
	// passwordMatchMessage.style.height = '0';
	// passwordMatchMessage.style.overflow = 'hidden';
    if (password.value === '' && password2.value === '') {
        passwordMatchMessage.textContent = '';
        // passwordMatchMessage.style.height = '0';
        // passwordMatchMessage.style.overflow = 'hidden';
		// submitButton.disabled = true;
    } else {
        if (password.value === password2.value) {
			if (password2.value.length < 8) {
				passwordMatchMessage.textContent = 'Password must be atleast 8 characters.';
				// passwordMatchMessage.style.color = 'red';
				// submitButton.disabled = true;
				// passwordMatchMessage.style.fontStyle = 'italic';
				// passwordMatchMessage.style.color = 'red';
			} else {
				passwordMatchMessage.textContent = 'Passwords match.';
				passwordMatchMessage.style.color = 'green';
				// passwordMatchMessage.style.fontStyle = 'italic';
				// submitButton.disabled = false;
			}
        } else {
            passwordMatchMessage.textContent = 'Passwords do not match.';
            // passwordMatchMessage.style.color = 'red';
			// submitButton.disabled = true;
			// passwordMatchMessage.style.fontStyle = 'italic';
			// passwordMatchMessage.style.color = 'red';
        }
        passwordMatchMessage.style.height = 'auto';
        passwordMatchMessage.style.overflow = 'visible';
    }
}

function submitHandler (e) {
	e.preventDefault();
	// console.log('event activated')
	// console.log(e.target.value)

    const formData = new FormData(form);
	const name = formData.get('name');
	const first_name = formData.get('first_name');
	const email = formData.get('email');
	const username = formData.get('username');
	let msg = ''

    for (let [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
		if (key == 'comment') {
			msg = `Dear ${first_name}, your comment has been updated and the author will be duly informed.\nThank you.`;
			break;
		} else if (key == 'contact') {
			msg = `Thank You ${name} for reaching out to us!\nYour comment is currently under review and we promise to take it with utmost importance.\nWe value your input and we will keep working to improve your experience.`;
			// form.reset();
			break;
		} else if (key == 'phone') {
			const password = formData.get('password1');
			const password2 = formData.get('password2');
			if (password !== password2) {
				console.log('Passwords do not match')
                alert('Passwords do not match.');
                return;
			}
			console.log('Passwords ok')
			msg = `Registration successful!\nUsername: ${first_name}\nUsername: ${email}`;
			break;
		} else {
			msg = `Welcome ${username}`;
		}
    }
	// alert(msg);
    // form.reset();

	fetch(form.action, {
		method: 'POST',
		body: new FormData(form),
		redirect: "follow"
	})
	.then(response=> {
		if (response.redirected) {
			window.location.href = response.url;
		} else {
			return response.json()
		}
	})
	.then(data=>{
		if (data) {
			console.log('###################');
			console.log('Raw response:', data);
			console.log('###################');
			if (data.message === 'success') {
				alert(msg);
				form.reset()
			} else if (data.message === 'error') {
				alert('Oopsy! Something went wrong.\nCheck your details again.');
				window.location.reload();
            } else if (data.message === 'incorrect password') {
				alert('Your passwords does not match.\nCheck your details and try again.');
				window.location.reload();
            } else if (data.message === 'form invalid') {
				let errorMessage = '';
				for (const [key, value] of Object.entries(data.errors)) {
					errorMessage += `${key}: ${value}\n`;
				}
				alert(errorMessage);
				window.location.reload();
			}
			// form.reset()
		}
	})
	// check screenshot for server side json config
}
