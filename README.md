# fullstack-challenge
1. Set Up Your Virtual Environment
   a.Open the Command Prompt
   b. Navigate to your project folder on the desktop using the cd command: cd C:\Users\YourUsername\Desktop\challenge
   c. Create a virtual environment using the following command: python -m venv venv_name
   d. Activate the virtual environment:venv_name\Scripts\activate
2. Install Flask
   a. pip install Flask
3. Running Your Application
   a.In the Command Prompt, ensure your virtual environment is still activated.
   b.Run your Flask application with the following command in the terminal: python app.py
   c. Your application should be running locally. You'll see output indicating that your Flask application is running on a local server, typically at http://localhost:5000
   d. Open a web browser and go to http://localhost:5000 to interact with your URL shortener service
4. Update the URL in script.js file
   a. In shortenForm.addEventListener and redirectForm.addEventListener functions of script.js file, if your local server is different to "http://127.0.0.1:5000", replace the "http://127.0.0.1:5000" in these functions with your localhost URL
