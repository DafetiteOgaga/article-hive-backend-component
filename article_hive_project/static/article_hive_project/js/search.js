try {
	document.addEventListener('DOMContentLoaded', function() {
		const searchInput = document.getElementById('search-input');
		
		searchInput.addEventListener('input', function() {
		const query = this.value;
		if (query.length > 2) {
			fetch(`/autocomplete/?q=${query}`)
			.then(response => response.json())
			.then(data => {
				// Update your UI with autocomplete suggestions
				console.log(data);
			});
		}
		});
	});
} catch (e) {}