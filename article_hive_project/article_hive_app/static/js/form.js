const form = document.getElementById('form');
form.addEventListener('submit', submitHandler);

function submitHandler (e) {
	e.preventDefault();
	// console.log('event activated')
	// console.log(e.target.value)

    const formData = new FormData(form);
	let msg = ''
	const firstname = formData.get('firstname');
	const email = formData.get('email');

    for (let [key, value] of formData.entries()) {
        console.log(`${key}: ${value}`);
		if (key == 'comment') {
			msg = `Thank You ${firstname} for reaching out to us!\nYour form has been processed successfully.\nWe value your contribution and we will keep working to improve your expeience.`;
			break;
		} else if (key == 'number') {
			msg = `Registration successful!\nUsername: ${firstname}\nUsername: ${email}`;
			break;
		} else {
			msg = `Welcome ${email}`;
		}
    }
	alert(msg);
    form.reset();

	// fetch(form.action, {method: 'POST', body: new FormData(form)})
	// .then(response=>response.json())
	// .then(data=>{
	//		if (data.message === 'success') {
	//			alert('Success!');
	// 			form.reset()
	//		}
	// })
	// check screenshot for server side json config
}
