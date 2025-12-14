from flask import Flask, jsonify
import os
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'changeme')
DB_NAME = os.getenv('DB_NAME', 'appdb')

@app.get('/cicd/api/health')
def health():
    return jsonify(message={'status': 'Toimii!'})

@app.get('/cicd/api/time')
def time():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cur = conn.cursor()
    cur.execute("SELECT NOW() + INTERVAL 2 HOUR")
    row = cur.fetchone()
    cur.close(); conn.close()
    return jsonify(message={'time': str(row[0])})

@app.get('/cicd/api/')
def index():
    """Simple endpoint that greets from DB."""
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cur = conn.cursor()
    cur.execute("SELECT 'Hello from MySQL via Testi!'")
    row = cur.fetchone()
    cur.close(); conn.close()
    return jsonify(message={'greeting': row[0]})
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8000, debug=True)
