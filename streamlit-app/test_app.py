import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector

def main():
    st.title("Sensor Dataa SQL-tietokannasta")

    # 1️⃣ Yritetään yhdistää MySQL:ään
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="ubuntu",
            password="salasana",  # korvaa oikealla salasanalla
            database="streamlit"
        )
    except mysql.connector.Error as e:
        st.error(f"MySQL-yhteys epäonnistui: {e}")
        return

    # 2️⃣ Haetaan data taulusta
    try:
        df = pd.read_sql("SELECT timestamp, value FROM sendor_data", conn)
        conn.close()
    except Exception as e:
        st.error(f"Virhe datan lukemisessa: {e}")
        return

    # 3️⃣ Tarkistetaan, että DataFrame ei ole tyhjä
    if df.empty:
        st.warning("Taulu 'sendor_data' on tyhjä. Lisää ensin dataa MySQL:ään.")
        return

    # 4️⃣ Muutetaan timestamp Pandas datetimeksi
    try:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    except Exception as e:
        st.error(f"Virhe timestamp-sarakkeen muunnoksessa: {e}")
        return

    # 5️⃣ Näytetään taulukko
    st.write("### Sensor Data Table")
    st.dataframe(df)

    # 6️⃣ Piirretään graafi
    try:
        fig = px.line(df, x="timestamp", y="value", title="Sensor Data Over Time")
        st.plotly_chart(fig, width='stretch')  # korvataan vanha use_container_width
    except Exception as e:
        st.error(f"Virhe graafin piirrossa: {e}")

if __name__ == "__main__":
    main()
