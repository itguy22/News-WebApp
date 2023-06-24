from flask import Flask, render_template, jsonify
import requests
import sqlite3

app = Flask(__name__)

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

@app.route('/')
def home():
    # ensure table exists before trying to fetch data
    create_table()

    # Connect to SQLite database and fetch data
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM news_data")
        data = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error {e} occurred while fetching data")
        data = []
    finally:
        conn.close()

    return render_template('home.html', data=data)

@app.route('/update-data')
def update_data():
    url = 'https://newsapi.org/v2/everything'
    parameters = {
        'q': 'transgender discrimination OR nonbinary discrimination',
        'pageSize': 100,
        'apiKey': '78d50591ba5b42c6a22c77fe2aa4d1bc',
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
            cursor.execute("INSERT INTO news_data (title, description, url, publishedAt) VALUES (?, ?, ?, ?)",
                (article['title'], article['description'], article['url'], article['publishedAt']))
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
        update_data()
    app.run(debug=True)
