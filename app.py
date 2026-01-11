import streamlit as st
import pandas as pd
import statsmodels.api as sm
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Dashboard Analisis TikTok Shop", layout="wide")

st.title("📊 Dashboard Keputusan Belanja Remaja Putri")
st.markdown("Analisis variabel yang paling memengaruhi keputusan belanja di TikTok Shop.")

# --- LOAD & CLEAN DATA ---
@st.cache_data
def load_data():
    # Membaca data kuesioner kamu
    df = pd.read_csv('data_kuesioner_likert_numerik.csv')
    
    # Penamaan ulang kolom agar mudah dikelola
    df.rename(columns={df.columns[3]: 'Kategori_Produk'}, inplace=True)
    
    # Menghitung Total Skor Berdasarkan Kolom di CSV
    # Tren: Kolom indeks 5-9 | Influencer: Kolom indeks 10-14 | Keputusan: Kolom indeks 15-17
    df['Total_Tren'] = df.iloc[:, 5:10].sum(axis=1)
    df['Total_Influencer'] = df.iloc[:, 10:15].sum(axis=1)
    df['Total_Keputusan'] = df.iloc[:, 15:18].sum(axis=1)
    
    return df

df = load_data()

# --- SIDEBAR FILTER ---
st.sidebar.header("Filter Analisis")
kategori = st.sidebar.selectbox(
    "Pilih Kategori Produk:",
    options=["Semua Produk"] + list(df['Kategori_Produk'].unique())
)

# Filter Data Berdasarkan Pilihan
if kategori == "Semua Produk":
    df_filtered = df
else:
    df_filtered = df[df['Kategori_Produk'] == kategori]

# --- LAYOUT DASHBOARD ---
col_left, col_right = st.columns([1, 1])

with col_left:
    # 1. PIE CHART - Distribusi Produk
    st.subheader("📍 Proporsi Kategori Produk")
    # Jika memfilter "Semua Produk", tampilkan pie chart kategori. 
    # Jika sudah pilih satu kategori, tampilkan pie chart perbandingan Tren vs Influencer di persepsi responden
    fig_pie = px.pie(df, names='Kategori_Produk', hole=0.4, title="Sebaran Responden per Kategori")
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    # 2. ANALISIS REGRESI & BAR CHART
    st.subheader(f"📈 Hasil Analisis: {kategori}")
    
    if len(df_filtered) > 2:
        # Perhitungan Regresi Linear Berganda
        X = df_filtered[['Total_Tren', 'Total_Influencer']]
        Y = df_filtered['Total_Keputusan']
        X = sm.add_constant(X)
        model = sm.OLS(Y, X).fit()
        
        # Menyiapkan data untuk Bar Chart
        df_hasil = pd.DataFrame({
            'Variabel': ['Tren (X1)', 'Influencer (X2)'],
            'Kekuatan Pengaruh': [model.params[1], model.params[2]]
        })
        
        # Pembuatan Bar Chart
        fig_bar = px.bar(
            df_hasil, 
            x='Variabel', 
            y='Kekuatan Pengaruh',
            color='Variabel',
            text_auto='.3f',
            title="Tingkat Pengaruh (Koefisien Beta)",
            color_discrete_map={'Tren (X1)': '#00D1FF', 'Influencer (X2)': '#FF4B4B'}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.error("Data tidak mencukupi untuk analisis.")

# --- KESIMPULAN SEDERHANA ---
st.divider()
if len(df_filtered) > 2:
    beta_t = model.params[1]
    beta_i = model.params[2]
    pemenang = "Tren" if beta_t > beta_i else "Influencer"
    
    st.success(f"### 💡 Kesimpulan Utama")
    st.write(f"Untuk kategori **{kategori}**, faktor yang paling dominan memengaruhi keputusan belanja adalah **{pemenang}**.")
    st.write(f"Artinya, jika kamu ingin meningkatkan penjualan {kategori}, fokuslah pada strategi yang berkaitan dengan {pemenang}.")
