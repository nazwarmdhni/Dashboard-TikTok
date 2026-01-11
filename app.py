import streamlit as st
import pandas as pd
import statsmodels.api as sm
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Dashboard TA - TikTok Shop", layout="wide")

st.title("📱 Dashboard Analisis Keputusan Belanja TikTok Shop")
st.markdown("Analisis Pengaruh **Tren** dan **Influencer** terhadap **Keputusan Belanja** Remaja Putri.")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    # Membaca file yang kamu unggah
    df = pd.read_csv('data_kuesioner_likert_numerik.csv')
    
    # Menghitung Total Skor untuk Regresi (Metode Likert)
    # Kolom 5-9: Tren | Kolom 10-14: Influencer | Kolom 15-17: Keputusan
    df['Total_Tren'] = df.iloc[:, 5:10].sum(axis=1)
    df['Total_Influencer'] = df.iloc[:, 10:15].sum(axis=1)
    df['Total_Keputusan'] = df.iloc[:, 15:18].sum(axis=1)
    
    return df

try:
    df = load_data()

    # --- BAGIAN 1: STATISTIK DESKRIPTIF ---
    st.subheader("📊 Gambaran Umum Responden")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_produk = px.pie(df, names=df.columns[3], title="Kategori Produk Terpopuler")
        st.plotly_chart(fig_produk)
        
    with col2:
        fig_frekuensi = px.histogram(df, x=df.columns[4], title="Frekuensi Belanja")
        st.plotly_chart(fig_frekuensi)

    # --- BAGIAN 2: REGRESI LINEAR BERGANDA ---
    st.divider()
    st.subheader("🤖 Analisis Regresi Linear Berganda")

    # Menyiapkan variabel
    X = df[['Total_Tren', 'Total_Influencer']]
    Y = df['Total_Keputusan']
    X = sm.add_constant(X) # Menambahkan intercept

    model = sm.OLS(Y, X).fit()

    # Menampilkan Hasil
    c1, c2, c3 = st.columns(3)
    c1.metric("Akurasi Model (R-Squared)", f"{model.rsquared:.3f}")
    c2.metric("Pengaruh Tren (Beta)", f"{model.params[1]:.3f}")
    c3.metric("Pengaruh Influencer (Beta)", f"{model.params[2]:.3f}")

    # --- BAGIAN 3: KESIMPULAN INTERAKTIF ---
    st.info("### 📌 Kesimpulan Mentor")
    
    p_tren = model.pvalues[1]
    p_influencer = model.pvalues[2]
    
    # Logika menentukan mana yang lebih berpengaruh
    if model.params[1] > model.params[2]:
        pemenang = "Tren"
        alasan = "lebih kuat pengaruhnya dibanding Influencer."
    else:
        pemenang = "Influencer"
        alasan = "lebih kuat pengaruhnya dibanding Tren."

    st.write(f"Berdasarkan data kuesioner kamu, variabel **{pemenang}** memiliki nilai koefisien yang lebih tinggi, artinya {alasan}")

except Exception as e:
    st.error(f"Gagal memuat data. Pastikan file 'data_kuesioner_likert_numerik.csv' ada di folder yang sama. Error: {e}")
