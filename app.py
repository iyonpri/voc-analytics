import streamlit as st
import pandas as pd
import plotly.express as px

# --- KONFIGURASI GOOGLE SHEETS ---
# Ganti ID di bawah dengan ID Spreadsheet Anda
SHEET_ID = "1T4yqz7u-Wxu26SxlySmTCJpq58SGn5BHAozcZNjLwII"
DATA_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=data"
CATS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=categories"

# Fungsi untuk menyimpan ke Google Sheets (via Form/Apps Script atau manual csv update)
# Untuk kemudahan akses publik, kita akan menggunakan metode upload & download CSV 
# atau integrasi library gspread. Namun untuk langkah awal ini, kita fokus pada tampilan publik.

st.set_page_config(page_title="VoC TRACTION", layout="wide")

def get_sentiment(text):
    t = str(text).lower()
    pos = ['😍', '🥰', '👍', 'best', 'mantap', 'keren', 'puas', 'gercep', 'untung', 'bagus']
    neg = ['hancur', 'buruk', 'parah', 'kecewa', 'penipu', 'nyesel', 'lelet', 'jelek', 'rugi', 'pindah', 'cabut']
    score = sum(3 for w in pos if w in t) - sum(4 for w in neg if w in t)
    return "Positive" if score >= 2 else ("Negative" if score <= -2 else "Neutral")

# --- SIDEBAR ---
with st.sidebar:
    st.title("VoC TRACTION")
    st.caption("TELKOMSEL ANALYTICS")
    st.divider()
    
    try:
        cats_df = pd.read_csv(CATS_URL)
        product_options = ["ALL"] + cats_df['name'].tolist()
        active_cat = st.radio("Pilih Produk", product_options)
    except:
        st.error("Gagal memuat kategori. Pastikan Link Google Sheets benar.")

# --- MAIN AREA ---
col_main, col_summary = st.columns([2.5, 1], gap="large")

with col_main:
    st.title(f"Produk: {active_cat}")
    
    # Fitur Upload
    uploaded_file = st.file_uploader("📂 Import CSV Baru", type="csv")
    if uploaded_file and active_cat != "ALL":
        df_new = pd.read_csv(uploaded_file)
        df_new = df_new.iloc[:, [0]] # Ambil kolom pertama
        df_new.columns = ['comment']
        df_new['product'] = active_cat
        df_new['sentiment'] = df_new['comment'].apply(get_sentiment)
        
        # Di sini Anda bisa menambahkan logika menyimpan balik ke Google Sheets
        st.success(f"Berhasil memproses {len(df_new)} data. (Simulasi Serverless)")
        st.dataframe(df_new)

    # Load Data ulasan
    try:
        db = pd.read_csv(DATA_URL)
        filtered_df = db if active_cat == "ALL" else db[db['product'] == active_cat]
        
        if not filtered_df.empty:
            for _, row in filtered_df.iloc[::-1].iterrows():
                with st.container(border=True):
                    c1, c2 = st.columns([5, 1])
                    c1.write(f"**\"{row['comment']}\"**")
                    s = row['sentiment']
                    color = "green" if s == "Positive" else "red" if s == "Negative" else "gray"
                    c2.markdown(f"**:{color}[{s.upper()}]**")
    except:
        st.info("Belum ada data di database.")

# --- SUMMARY ---
with col_summary:
    st.subheader("Analytics Center")
    if 'filtered_df' in locals() and not filtered_df.empty:
        counts = filtered_df['sentiment'].value_counts()
        fig = px.pie(values=counts.values, names=counts.index, hole=0.7,
                     color=counts.index, color_discrete_map={'Positive':'#22c55e','Negative':'#ef4444','Neutral':'#64748b'})
        fig.update_layout(showlegend=False, height=250)
        st.plotly_chart(fig, use_container_width=True)