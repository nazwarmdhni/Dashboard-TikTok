import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard Analisis Perilaku Belanja Remaja Putri di TikTok Shop")

st.write("""
Dashboard ini dibuat untuk mengetahui variabel mana yang lebih berpengaruh
antara **Tren** dan **Influencer** terhadap **Keputusan Belanja**
remaja putri di e-commerce TikTok Shop.
""")

uploaded_file = st.file_uploader("Upload file CSV hasil kuesioner", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview Data Kuesioner")
    st.dataframe(df.head())

    # ===============================
    # AMBIL KOLOM BERDASARKAN URUTAN
    # ===============================
    kolom_tren = df.iloc[:, 5]
    kolom_influencer = df.iloc[:, 6]
    kolom_keputusan = df.iloc[:, 7]

    # ===============================
    # HITUNG RATA-RATA
    # ===============================
    avg_tren = kolom_tren.mean()
    avg_influencer = kolom_influencer.mean()

    col1, col2 = st.columns(2)
    col1.metric("Rata-rata Pengaruh Tren", round(avg_tren, 2))
    col2.metric("Rata-rata Pengaruh Influencer", round(avg_influencer, 2))

    # ===============================
    # VISUALISASI
    # ===============================
    fig, ax = plt.subplots()
    ax.bar(
        ["Tren", "Influencer"],
        [avg_tren, avg_influencer]
    )
    ax.set_ylabel("Nilai Rata-rata")
    ax.set_title("Perbandingan Pengaruh Tren dan Influencer")

    st.pyplot(fig)

    # ===============================
    # KESIMPULAN OTOMATIS
    # ===============================
    st.subheader("Kesimpulan")

    if avg_tren > avg_influencer:
        st.success("📌 Tren memiliki pengaruh yang lebih besar terhadap keputusan belanja remaja putri di TikTok Shop.")
    elif avg_influencer > avg_tren:
        st.success("📌 Influencer memiliki pengaruh yang lebih besar terhadap keputusan belanja remaja putri di TikTok Shop.")
    else:
        st.info("📌 Pengaruh tren dan influencer memiliki tingkat pengaruh yang sama.")

