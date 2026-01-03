import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul Dashboard
st.title("Dashboard Analisis Pengaruh Tren dan Influencer")
st.write("Studi Perilaku Belanja Remaja Putri di TikTok Shop")

# Upload file CSV
uploaded_file = st.file_uploader("Upload file CSV hasil kuesioner", type=["csv"])

if uploaded_file is not None:
    # Baca data
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview Data Responden")
    st.dataframe(df.head())

    # =========================
    # PENGAMBILAN DATA
    # =========================
    # Kolom Tren     : 5, 5.1, 5.2, 5.3, 5.4  → index 5–9
    # Kolom Influencer: 6, 6.1, 6.2, 6.3, 6.4 → index 10–14

    tren = df.iloc[:, 5:10].apply(pd.to_numeric, errors="coerce")
    influencer = df.iloc[:, 10:15].apply(pd.to_numeric, errors="coerce")

    # Hitung rata-rata
    avg_tren = tren.mean().mean()
    avg_influencer = influencer.mean().mean()

    # =========================
    # METRIK UTAMA
    # =========================
    st.subheader("Hasil Utama Analisis")

    col1, col2 = st.columns(2)
    col1.metric("Rata-rata Pengaruh Tren", round(avg_tren, 2))
    col2.metric("Rata-rata Pengaruh Influencer", round(avg_influencer, 2))

    # =========================
    # GRAFIK PERBANDINGAN
    # =========================
    st.subheader("Perbandingan Pengaruh Tren vs Influencer")

    fig, ax = plt.subplots()
    ax.bar(["Tren", "Influencer"], [avg_tren, avg_influencer])
    ax.set_ylabel("Nilai Rata-rata")
    ax.set_xlabel("Variabel")
    ax.set_title("Pengaruh terhadap Keputusan Belanja")

    st.pyplot(fig)

    # =========================
    # KESIMPULAN OTOMATIS
    # =========================
    st.subheader("Kesimpulan")

    if avg_tren > avg_influencer:
        st.success(
            "Berdasarkan hasil analisis dashboard, variabel **Tren** "
            "memiliki pengaruh yang lebih besar terhadap keputusan belanja "
            "remaja putri di TikTok Shop."
        )
    else:
        st.success(
            "Berdasarkan hasil analisis dashboard, variabel **Influencer** "
            "memiliki pengaruh yang lebih besar terhadap keputusan belanja "
            "remaja putri di TikTok Shop."
        )
