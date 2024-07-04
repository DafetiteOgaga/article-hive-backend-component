const form = document.getElementById('form');
form.addEventListener('submit', submitHandler);

let msg = ''
function submitHandler (e) {
	e.preventDefault();
	// console.log('event activated')
	// console.log(e.target.value)

    const formData = new FormData(form);
	const name = formData.get('name');
	const firstname = formData.get('firstname');
	const email = formData.get('email');
	const username = formData.get('username');

    for (let [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
		if (key == 'comment') {
			msg = `Dear ${firstname}, your comment has been updated and the author will be duly informed.\nThank you.`;
			break;
		} else if (key == 'contact') {
			msg = `Thank You ${name} for reaching out to us!\nYour comment is currently under review and we promise to take it with utmost importance.\nWe value your input and we will keep working to improve your experience.`;
			break;
		} else if (key == 'number') {
			msg = `Registration successful!\nUsername: ${firstname}\nUsername: ${email}`;
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
			} else if (data.message === 'error') {
				alert('Oopsy! Something went wrong.\nCheck your details again.');
				window.location.reload();
            }
			// form.reset()
		}
	})
	// check screenshot for server side json config
}
