import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard TikTok Shop", layout="centered")

st.title("Dashboard Analisis TikTok Shop")
st.subheader("Pengaruh Tren dan Influencer terhadap Keputusan Belanja Remaja Putri")

st.write("""
Dashboard ini bertujuan untuk menganalisis pengaruh **tren** dan **influencer**
terhadap keputusan belanja remaja putri di e-commerce **TikTok Shop**
dalam konteks **fashion, make up, dan skincare**.
""")

st.header("Upload Data Kuesioner")
uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("Data berhasil dimuat")

    st.header("Jumlah Responden")
    st.metric("Total Responden", len(df))

    st.header("Contoh Data Responden")
    st.dataframe(df.head())

    st.header("Analisis Pengaruh")

    avg_tren = df["Pengaruh Tren"].mean()
    avg_influencer = df["Pengaruh Influencer"].mean()

    col1, col2 = st.columns(2)
    col1.metric("Rata-rata Pengaruh Tren", round(avg_tren, 2))
    col2.metric("Rata-rata Pengaruh Influencer", round(avg_influencer, 2))

    st.header("Perbandingan Pengaruh")
    chart_data = pd.DataFrame({
        "Variabel": ["Tren", "Influencer"],
        "Rata-rata Skor": [avg_tren, avg_influencer]
    })

    st.bar_chart(chart_data.set_index("Variabel"))

    st.header("Kesimpulan Sementara")
    if avg_tren > avg_influencer:
        st.success("Tren lebih berpengaruh terhadap keputusan belanja.")
    elif avg_tren < avg_influencer:
        st.success("Influencer lebih berpengaruh terhadap keputusan belanja.")
    else:
        st.info("Pengaruh tren dan influencer seimbang.")
