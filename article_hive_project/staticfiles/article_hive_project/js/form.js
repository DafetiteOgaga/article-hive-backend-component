const form = document.getElementById('form');
const password = document.getElementById('password1');
const password2 = document.getElementById('password2');
const new_password1 = document.getElementById('new_password1');
const new_password2 = document.getElementById('new_password2');
const passwordMatchMessage = document.getElementById('password-match-message');
const submitButton = document.getElementById('submit-button');
form.addEventListener('submit', submitHandler);
password.addEventListener('input', checkPasswordMatch);
password2.addEventListener('input', checkPasswordMatch);
new_password1.addEventListener('input', checkPasswordMatch);
new_password2.addEventListener('input', checkPasswordMatch);

// let msg = ''

function checkPasswordMatch() {
	passwordMatchMessage.textContent = '';
    if (password.value === '' && password2.value === '') {
        passwordMatchMessage.textContent = '';
    } else {
        if (password.value === password2.value) {
			if (password2.value.length < 8) {
				passwordMatchMessage.textContent = 'Password must be atleast 8 characters.';
			} else {
				passwordMatchMessage.textContent = 'Passwords match.';
				passwordMatchMessage.style.color = 'green';
			}
        } else {
            passwordMatchMessage.textContent = 'Passwords do not match.';
        }
        passwordMatchMessage.style.height = 'auto';
        passwordMatchMessage.style.overflow = 'visible';
    }

	if (new_password1.value === '' && new_password2.value === '') {
        passwordMatchMessage.textContent = '';
    } else {
        if (new_password1.value === new_password2.value) {
			if (new_password2.value.length < 8) {
				passwordMatchMessage.textContent = 'Password must be atleast 8 characters.';
			} else {
				passwordMatchMessage.textContent = 'Passwords match.';
				passwordMatchMessage.style.color = 'green';
			}
        } else {
            passwordMatchMessage.textContent = 'Passwords do not match.';
        }
        passwordMatchMessage.style.height = 'auto';
        passwordMatchMessage.style.overflow = 'visible';
    }
}

function submitHandler (e) {
	e.preventDefault();

    const formData = new FormData(form);
	const name = formData.get('name');
	const first_name = formData.get('first_name');
	const email = formData.get('email');
	const username = formData.get('username');
	let msg = ''

    for (let [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
		// if (key == 'comment') {
		// 	msg = `Dear ${first_name}, your comment has been updated and the author will be duly informed.\nThank you.`;
		// 	break;
		// } else 
		if (key == 'contact') {
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
			// console.log('###################');
			// console.log('Raw response:', data);
			// console.log('###################');
			if (data.message === 'success') {
				alert(msg);
				form.reset()
			} else if (data.message === 'error') {
				// fix for contact us and author response
				alert('Oopsy! Something went wrong.\nCheck your login details again or register if you are not a member yet.');
				window.location.reload();
			} else if (data.message === 'not registered') {
				alert('Oopsy! Not a Member yet.\nRegister for free and sign in.\nThank you.');
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
