import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

st.sidebar.title("Valikko")
st.sidebar.markdown('<a href="http://195.148.21.250/chat" target="_self" style="text-decoration:none; color:orange;">💬Avaa Chat</a>',
    unsafe_allow_html=True)
st.sidebar.markdown('<a href="http://195.148.21.250" target="_self" style="text-decoration:none; color:orange;">🏠Avaa kotisivu</a>',
    unsafe_allow_html=True)

def main():
    st.markdown("<--- Sivupaneeli")
    st.title("Sensor Data ja Säädata")

    # Yhteys MySQL:ään
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME")
        )
    except mysql.connector.Error as e:
        st.error(f"MySQL-yhteys epäonnistui: {e}")
        return

    try:
        sensor_df = pd.read_sql("SELECT timestamp, value FROM sendor_data", conn)

        if sensor_df.empty:
            st.warning("Taulu 'sendor_data' on tyhjä. Lisää ensin dataa MySQL:ään.")
        else:
            sensor_df['timestamp'] = pd.to_datetime(sensor_df['timestamp'])
            st.write("### Sensor Data Table")
            st.dataframe(sensor_df)

            fig = px.line(sensor_df, x="timestamp", y="value", title="Sensor Data Over Time")
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Virhe sensoridatan lukemisessa: {e}")

    try:
        weather_df = pd.read_sql(
            "SELECT city, temperature, clouds, timestamp FROM weather_data ORDER BY timestamp DESC LIMIT 10",
            conn
        )

        if not weather_df.empty:
            city = weather_df['city'][0]
            temp = weather_df['temperature'][0]
            clouds = weather_df['clouds'][0]
            timestamp = weather_df['timestamp'][0]

            weather_df.rename(columns={
    "city": "Kaupunki",
    "temperature": "Lämpötila (°C)",
    "clouds": "Pilvisyys (%)",
    "timestamp": "Aikaleima"
}, inplace=True)

            st.write("### Viimeisin säädata")
            st.dataframe(weather_df)

    except Exception as e:
        st.error(f"Virhe säädatan lukemisessa: {e}")

    conn.close()

if __name__ == "__main__":
    main()
