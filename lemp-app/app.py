from flask import Flask
import mysql.connector
import os
from dotenv import load_dotenv

# Lataa ympäristömuuttujat

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT NOW();")  # hae serverin kellonaika
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    server_time = result[0]

    return f"""
    <h1 style="font-size: 50px;">Terve!</h1>
    <p>Tämä on minun lemp-appilla toteutettu sivuni!</p>
    <p>Server time from SQL: {server_time}</p>
    <p>Kello on tuossa yläpuolella ja päivittyy päivittämällä sivun ^</p>
    <p style="font-size: 30px;"> Katso  data-analyysini <a href="http://195.148.21.250/data-analysis">täältä</a> </p>
    """
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
