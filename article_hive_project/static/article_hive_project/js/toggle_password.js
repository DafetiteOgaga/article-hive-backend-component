// scripts.js

function togglePasswordVisibility(inputId) {
    const passwordInput = document.getElementById(inputId);
    const icon = passwordInput.nextElementSibling.querySelector('i');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}


// function togglePasswordVisibility(inputId) {
// 	console.log('togglePasswordVisibility called ...');
//     const passwordInput = document.getElementById(inputId);
// 	console.log("ID found ... : " + inputId);
//     const icon = passwordInput.nextElementSibling.querySelector('i');

//     if (passwordInput.type === 'password') {
// 		console.log("turning password to text (forward)")
//         passwordInput.type = 'text';
//         icon.classList.remove('fa-eye');
//         icon.classList.add('fa-eye-slash');
//     } else {
// 		console.log("turning text to password (reverse)")
//         passwordInput.type = 'password';
//         icon.classList.remove('fa-eye-slash');
//         icon.classList.add('fa-eye');
//     }
// }

// document.addEventListener('DOMContentLoaded', function() {
//     const eyeIcons = document.querySelectorAll('.eye-icon');
// 	console.log("load document ...")
//     eyeIcons.forEach(icon => {
// 		console.log("adding click listener to icon...")
//         icon.addEventListener('click', function(event) {
//             event.preventDefault(); // Prevent default behavior
//             event.stopPropagation(); // Stop the event from propagating
// 			console.log("icon clicked ...")
//             const inputId = this.previousElementSibling.id;
// 			console.log("before toggle ...")
//             togglePasswordVisibility(inputId);
// 			console.log("after toggle ...")
//         });
//     });
// });