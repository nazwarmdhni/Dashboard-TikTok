import streamlit as st
import pandas as pd
import statsmodels.api as sm
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Analisis Produk - TikTok Shop", layout="wide")

st.title("🛍️ Analisis Pengaruh per Kategori Produk")
st.markdown("Gunakan filter di samping untuk melihat apakah produk tertentu lebih dipengaruhi oleh **Tren** atau **Influencer**.")

# --- LOAD & PREPROCESSING DATA ---
@st.cache_data
def load_and_clean_data():
    # Membaca data
    df = pd.read_csv('data_kuesioner_likert_numerik.csv')
    
    # Menamai ulang kolom kategori produk agar mudah dipanggil (Kolom indeks ke-3)
    df.rename(columns={df.columns[3]: 'Kategori_Produk'}, inplace=True)
    
    # Menghitung Total Skor Variabel
    # X1 (Tren): Kolom 5-9 | X2 (Influencer): Kolom 10-14 | Y (Keputusan): Kolom 15-17
    df['Total_Tren'] = df.iloc[:, 5:10].sum(axis=1)
    df['Total_Influencer'] = df.iloc[:, 10:15].sum(axis=1)
    df['Total_Keputusan'] = df.iloc[:, 15:18].sum(axis=1)
    
    return df

df = load_and_clean_data()

# --- SIDEBAR FILTER ---
st.sidebar.header("Filter Analisis")
kategori = st.sidebar.selectbox(
    "Pilih Kategori Produk:",
    options=["Semua Produk"] + list(df['Kategori_Produk'].unique())
)

# Logika Filter Data
if kategori == "Semua Produk":
    df_filtered = df
else:
    df_filtered = df[df['Kategori_Produk'] == kategori]

# --- CEK APAKAH DATA CUKUP ---
if len(df_filtered) < 3:
    st.warning(f"Data untuk kategori {kategori} terlalu sedikit untuk dilakukan analisis regresi.")
else:
    # --- REGRESI LINEAR BERGANDA ---
    X = df_filtered[['Total_Tren', 'Total_Influencer']]
    Y = df_filtered['Total_Keputusan']
    X = sm.add_constant(X)
    
    model = sm.OLS(Y, X).fit()

    # --- TAMPILAN DASHBOARD ---
    st.subheader(f"Analisis untuk Kategori: {kategori}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Responden", f"{len(df_filtered)} orang")
    col2.metric("Pengaruh Tren (Beta)", f"{model.params[1]:.3f}")
    col3.metric("Pengaruh Influencer (Beta)", f"{model.params[2]:.3f}")

    # Visualisasi
    st.divider()
    c1, c2 = st.columns(2)
    
    with c1:
        fig_tren = px.scatter(df_filtered, x='Total_Tren', y='Total_Keputusan', 
                             trendline="ols", title=f"Tren vs Keputusan ({kategori})")
        st.plotly_chart(fig_tren, use_container_width=True)
        
    with c2:
        fig_inf = px.scatter(df_filtered, x='Total_Influencer', y='Total_Keputusan', 
                            trendline="ols", title=f"Influencer vs Keputusan ({kategori})")
        st.plotly_chart(fig_inf, use_container_width=True)

    # --- KESIMPULAN OTOMATIS ---
    st.success("### 💡 Temuan Utama")
    beta_tren = model.params[1]
    beta_inf = model.params[2]
    
    if beta_tren > beta_inf:
        st.write(f"Untuk kategori **{kategori}**, remaja putri lebih terdorong belanja karena **Tren yang sedang viral**. Strategi konten harus fokus pada apa yang sedang 'hype'.")
    else:
        st.write(f"Untuk kategori **{kategori}**, remaja putri lebih percaya pada **Review Influencer**. Strategi pemasaran sebaiknya fokus pada kolaborasi dengan kreator konten.")
