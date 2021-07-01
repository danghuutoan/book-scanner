handleBookDelete = (book_id) => {
    fetch("/books/" + book_id, {
		method: "DELETE",
		body: {},
	}).then((response) => {
		console.log(response);
		window.location.replace("/books");
	});
}
