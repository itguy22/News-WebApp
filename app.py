from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import requests
import sqlite3
import os
import pandas as pd
from datetime import datetime

load_dotenv()

app = Flask(__name__)

df = pd.read_csv('./data/LGBT_Survey_DailyLife.csv')
def create_table():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS news_data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            url TEXT,
            publishedAt TEXT
        )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error {e} occurred while creating table")
    finally:
        conn.close()

@app.route('/news')
def news():
    create_table()

    # Connect to SQLite database and fetch data
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news_data ORDER BY publishedAt DESC LIMIT 10")  # Add ORDER BY and LIMIT to your SQL query
    data = cursor.fetchall()
    conn.close()

    articles = [{'id': id, 'title': title, 'description': description, 'url': url, 'publishedAt': publishedAt} for id, title, description, url, publishedAt in data]

    # Parse the publishedAt string into a datetime object
    for article in articles:
        article['publishedAt'] = datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")

    return render_template('news.html', articles=articles)  # Pass data to your news.html template


@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/data')
def data():
    df = pd.read_csv('/data/LGBT_Survey_DailyLife.csv')
    return df.to_json(orient='records')


@app.route("/")
def home():
    return render_template('landingPage.html', title='Landing Page')

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/joinus')
def joinus():
    return render_template('joinus.html')


@app.route('/update-data')
def update_data():
    news_api_key = os.getenv('NEWS_API_KEY')
    url = 'https://newsapi.org/v2/everything'
    parameters = {
        'q': 'transgender discrimination OR nonbinary discrimination',
        'pageSize': 100,
        'apiKey': news_api_key,
    }

    try:
        response = requests.get(url, params=parameters)
        response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        articles = response.json()['articles']
    except (requests.RequestException, ValueError, KeyError) as e:
        print(f"Error {e} occurred while fetching API data")
        return jsonify({"success": False, "message": str(e)})

    # Connect to SQLite database and store data
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        for article in articles:
            cursor.execute("""
                INSERT INTO news_data (title, description, url, publishedAt) 
                SELECT ?, ?, ?, ? 
                WHERE NOT EXISTS(SELECT 1 FROM news_data WHERE title=?)
                """,
                (article['title'], article['description'], article['url'], article['publishedAt'], article['title']))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error {e} occurred while inserting data")
        return jsonify({"success": False, "message": str(e)})
    finally:
        conn.close()

    return jsonify({"success": True})


if __name__ == '__main__':
    # Call update data function to get data when the ap starts
    with app.app_context():
        app.run(debug=True)
