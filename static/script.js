document.addEventListener('DOMContentLoaded', function () {
    const shortenForm = document.getElementById('shorten-form');
    const shortenedUrl = document.getElementById('shortened-url');
    const redirectForm = document.getElementById('redirect-form');
    const clearButton=document.getElementById('clear-button');
    // const clearButton=document.getElementById('clear-button');

    shortenForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(shortenForm);
        const longUrl = formData.get('long_url');

        // API request to your Flask server
        fetch('http://127.0.0.1:5000/shorten', {
            method: 'POST',
            body: JSON.stringify({ long_url: longUrl }),
            headers: { 'Content-Type': 'application/json' },
        })
            .then(response => response.text())
            .then(data => {
                shortenedUrl.textContent = 'Shortened URL: ' + data;
            });
    });

    redirectForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the form from submitting
        const formData = new FormData(redirectForm);
        const shortUrl = formData.get('short_url');
    
        // Send a GET request to your Flask server with short_url as a query parameter
        fetch(`http://127.0.0.1:5000/redirect?short_url=${shortUrl}`)
            .then(response => {
                if (response.ok) {
                    // Parse the response as JSON if needed
                    return response.json();
                } else {
                    return Promise.reject('Short URL not yet found');
                }
            })
            .then(data => {
                // Open the long URL in a new tab
                window.open(data.long_url, '_blank');
            })
            .catch(error => {
                alert(error);
            });
    });
     
    clearButton.addEventListener('click', function () {
        // Clear all the forms
        shortenForm.reset();
        redirectForm.reset();
        
        // Clear the displayed shortened URL
        shortenedUrl.textContent = '';
    });
});
