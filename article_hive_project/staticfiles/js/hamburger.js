try {
	document.addEventListener('DOMContentLoaded', function() {
		const menuToggle = document.getElementById('menu-toggle');
		const mainContent = document.getElementById('main-content');
		const menu = document.querySelector('.menu');
		const hero = document.getElementById('bounce-out');
		const click_anime = document.getElementById('click-anime');
		const right_anime = document.getElementById('right-anime');
		const left_anime = document.getElementById('left-anime');
		const top_drop = document.getElementById('top-drop');
		const down_drop = document.getElementById('down-drop');
		// const hero = document.getElementsByClassName('hero');
		// console.log('hero:', hero);

		menuToggle.addEventListener('change', function() {
			if (menuToggle.checked) {
				// console.log('menuToggle.checked:', menuToggle.checked);
				mainContent.classList.add('blur');
				if (hero) {
					hero.removeAttribute('id');
				}
				if (click_anime) {
					click_anime.removeAttribute('id');
				}
				if (right_anime) {
					right_anime.removeAttribute('id');
				}
				if (left_anime) {
					left_anime.removeAttribute('id');
				}
				if (top_drop) {
					top_drop.removeAttribute('id');
				}
				if (down_drop) {
					down_drop.removeAttribute('id');
				}
			} else {
				// console.log('menuToggle.checked:', menuToggle.checked);
				mainContent.classList.remove('blur');
				// hero.setAttribute('id', 'bounce-out')
			}
		});

		document.addEventListener('click', function(event) {
			const isClickInside = menu.contains(event.target);
			const isToggleClick = menuToggle.contains(event.target);

			if (!isClickInside && !isToggleClick && menuToggle.checked) {
				menuToggle.checked = false;
			}
		});
	});
} catch {}

document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const menu = document.querySelector('.menu');
    const menuIcon = document.querySelector('.menu-icon');

    document.addEventListener('click', function(event) {
        const isClickInsideMenu = menu.contains(event.target);
        const isClickOnToggle = menuToggle.contains(event.target);
        const isClickOnMenuIcon = menuIcon.contains(event.target);
        
        // Close the menu if the click is outside the menu, toggle button, and menu icon
        if (!isClickInsideMenu && !isClickOnToggle && !isClickOnMenuIcon) {
            menuToggle.checked = false;
        }
    });

    menuToggle.addEventListener('click', function(event) {
        // Allow the menu to toggle when clicking on the checkbox itself
        if (menuToggle.checked) {
            menuToggle.checked = true;
        } else {
            menuToggle.checked = false;
        }
    });
});
