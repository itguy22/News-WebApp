News Analysis and Visualization App
This app collects and displays news data about gender discrimination and gender violence, focusing on news regarding transgender and nonbinary individuals. It uses the News API to gather news articles, which are then stored in a SQLite database. The app provides a simple web interface for viewing the articles.

Prerequisites
To run this app, you need to have Python installed on your machine. We recommend using Python 3.9 or later. You can download Python from the official website: https://www.python.org/downloads/

Installation
First, clone this repository to your local machine using git:

git clone https://github.com/yourusername/yourrepository.git
Replace yourusername and yourrepository with your actual GitHub username and repository name.

Next, navigate to the project directory:

cd yourrepository
It's recommended to create a virtual environment to isolate the dependencies of this project from your other Python projects. You can create a virtual environment using the following commands:

python3 -m venv env
Activate the virtual environment:

On Unix/macOS:

source env/bin/activate
On Windows:

.\env\Scripts\activate
After activating the virtual environment, install the required Python packages:

pip install -r requirements.txt
Running the app
You can start the app with the following command:

flask run
The app will be accessible at http://localhost:5000

API Key
The News API requires an API key, which you need to provide. You can do this by setting the NEWSAPI_KEY environment variable before running the app:

export NEWSAPI_KEY=your_api_key
flask run
Replace your_api_key with your actual News API key. On Windows, use set instead of export.
