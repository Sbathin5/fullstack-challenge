from urllib.parse import urlparse
import random
import string
from flask import Flask, render_template, request, redirect, g
import sqlite3
from flask import jsonify
from urllib.parse import unquote

app = Flask(__name__)

# Define the characters to use for the short key
characters = string.ascii_letters + string.digits


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('url_mapping.db')
    return db


def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # Check if the table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='url_mapping'")
        table_exists = cursor.fetchone()

        if not table_exists:
            with app.open_resource('schema.sql', mode='r') as f:
                cursor.executescript(f.read())
            db.commit()
        else:
            print("Table 'url_mapping' already exists.")


def generate_short_key(key_length=6):
    # Generate a random short key of a specified length
    short_key = ''.join(random.choice(characters) for _ in range(key_length))
    return short_key


def shorten_url(long_url):
    db = get_db()
    cursor = db.cursor()

    # Check if the long URL is already in the database
    cursor.execute(
        'SELECT shortened_url FROM url_mapping WHERE long_url = ?', (long_url,))
    row = cursor.fetchone()
    if row:
        # If it's already in the database, return the existing shortened URL
        return row[0]

    # Extract the base URL from the long URL
    parsed_url = urlparse(long_url)
    base_url = parsed_url.netloc

    # Generate a unique short key and store it in the database
    short_key = generate_short_key()
    # Construct the full shortened URL
    shortened_url = f"http://{base_url}/{short_key}"
    cursor.execute(
        'INSERT INTO url_mapping (shortened_url, long_url) VALUES (?, ?)', (shortened_url, long_url))
    db.commit()

    return shortened_url


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten():
    try:
        long_url = request.json['long_url']
        shortened_url = shorten_url(long_url)
        return shortened_url
    except KeyError:
        return "Invalid request", 400


@app.route('/redirect', methods=['GET'])
def redirect_to_original():
    short_url = request.args.get('short_url')

    print("this is url", short_url)
    db = get_db()
    cursor = db.cursor()

    # Retrieve the original URL from the database
    cursor.execute(
        'SELECT long_url FROM url_mapping WHERE shortened_url = ?', (short_url,))
    row = cursor.fetchone()
    if row:
        original_url = row[0]
        return jsonify({'long_url': original_url})
    else:
        return "Short URL not found", 404


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
