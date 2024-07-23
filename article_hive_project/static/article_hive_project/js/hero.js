try {
	document.addEventListener('DOMContentLoaded', function() {
		const images = [
			'./static/images/Adult-Book-Club.png',
			'./static/images/GMA_Main_BookClubMontage_March_v01_ks_1710354921581_hpMain_16x9_1600.jpg',
			'./static/images/Group-of-open-books-photographed-from-top-down.png',
			'./static/images/how-to-host-a-virtual-book-club2-1585775401.jpg',
			'./static/images/shutterstock_240069319.png'
		];

		let currentIndex = 0;
		const heroElement = document.getElementsByClassName('hero')[0];

		if (heroElement) {
			function changeBackgroundImage() {
				heroElement.style.background = `url(${images[currentIndex]}) no-repeat center center`;
				heroElement.style.backgroundSize = 'cover';
				currentIndex = (currentIndex + 1) % images.length;
			}

			setInterval(changeBackgroundImage, 4500);

			changeBackgroundImage();
		}
	});
} catch (e) {}