import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard TikTok Shop", layout="centered")

st.title("📊 Dashboard Pengaruh Tren dan Influencer")
st.subheader("Keputusan Belanja Remaja Putri di TikTok Shop")

st.write("""
Dashboard ini dibuat untuk menganalisis pengaruh **tren** dan **influencer**
terhadap keputusan belanja remaja putri di e-commerce **TikTok Shop**
dengan konteks **fashion, make up, dan skincare**.
""")

st.header("📁 Upload Data Kuesioner")

uploaded_file = st.file_uploader(
    "Upload file CSV hasil kuesioner",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("✅ Data berhasil dimuat!")

    st.header("📄 Preview Data Responden")
    st.dataframe(df)

    st.header("👩 Jumlah Responden")
    st.metric("Total Responden", len(df))

    st.header("📊 Rata-rata Skor Pengaruh")

    col_tren = "Pengaruh Tren"
    col_influencer = "Pengaruh Influencer"

    if col_tren in df.columns and col_influencer in df.columns:
        avg_tren = df[col_tren].mean()
        avg_influencer = df[col_influencer].mean()

        st.write("Rata-rata Pengaruh Tren:", round(avg_tren, 2))
        st.write("Rata-rata Pengaruh Influencer:", round(avg_influencer, 2))

        st.header("📈 Perbandingan Pengaruh")
        chart_data = pd.DataFrame({
            "Variabel": ["Tren", "Influencer"],
            "Rata-rata Skor": [avg_tren, avg_influencer]
        })

        st.bar_chart(chart_data.set_index("Variabel"))

        st.header("📝 Kesimpulan Sementara")
        if avg_tren > avg_influencer:
            st.success("📌 Tren memiliki pengaruh lebih besar terhadap keputusan belanja.")
        elif avg_tren < avg_influencer:
            st.success("📌 Influencer memiliki pengaruh lebih besar terhadap keputusan belanja.")
        else:
            st.info("📌 Tren dan influencer memiliki pengaruh yang seimbang.")
    else:
        st.warning("⚠️ Kolom 'Pengaruh Tren' atau 'Pengaruh Influencer' tidak ditemukan.")
