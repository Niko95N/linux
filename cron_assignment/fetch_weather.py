#!/usr/bin/env python3
import requests
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Helsinki"

URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()


response = requests.get(URL)
data = response.json()

temp = data['main']['temp']
clouds = data['clouds']['all']
timestamp = datetime.now()

cursor.execute(
    'INSERT INTO weather_data (city, temperature, clouds, timestamp) VALUES (%s, %s, %s, %s)',
    (CITY, temp, clouds, timestamp)
)

conn.commit()
cursor.close()
conn.close()

print(f"Data tallennettu: {CITY} {temp}°C, clouds {clouds}%, {timestamp}")
