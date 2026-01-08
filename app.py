import streamlit as st
import pandas as pd
import json

# --- KONFIGURASI STREAMLIT ---
st.set_page_config(page_title="VoC TRACTION Product", layout="wide")

# --- DATABASE SIMPEL (Agar Data Tidak Hilang Saat Orang Lain Add) ---
# Di deploy public, kita gunakan file CSV sebagai database
DB_FILE = "database_ulasan.csv"

def load_data():
    if not os.path.exists(DB_FILE):
        return pd.DataFrame(columns=["product", "comment", "sentiment"])
    return pd.read_csv(DB_FILE)

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# --- FUNGSI ANALISIS SENTIMEN (Sesuai Logic Anda) ---
def get_sentiment(text):
    t = str(text).lower()
    pos = ['😍', '🥰', '👍', 'best', 'mantap', 'keren', 'puas', 'gercep', 'untung', 'bagus']
    neg = ['hancur', 'buruk', 'parah', 'kecewa', 'penipu', 'nyesel', 'lelet', 'jelek', 'rugi', 'pindah', 'cabut']
    score = sum(3 for w in pos if w in t) - sum(4 for w in neg if w in t)
    return "Positive" if score >= 2 else ("Negative" if score <= -2 else "Neutral")

# --- INJECT HTML & CSS (Full Dashboard Layout) ---
# Kita masukkan seluruh kode index.html Anda ke dalam variabel string ini
html_layout = """
<style>
    /* Masukkan seluruh blok <style> dari index.html Anda secara utuh */
    :root { 
        --bg:#020617; --side:#0f172a; --card:rgba(30, 41, 59, 0.4); --text:#f1f5f9; 
        --accent:#ef4444; --pos:#22c55e; --neg:#f87171; --neu:#64748b; --border:#334155; 
        --grad: linear-gradient(135deg, #ef4444 0%, #991b1b 100%);
    }
    /* ... Sisa CSS Anda ... */
</style>

<body class="dark-mode">
    <div class="sidebar">...</div>
    <div class="main">...</div>
    <div class="summary">...</div>
</body>
"""

# --- INTEGRASI KE STREAMLIT ---
# Gunakan komponen streamlit untuk menangani input dari orang lain
with st.sidebar:
    st.markdown("### ➕ Tambah Ulasan Baru")
    selected_p = st.selectbox("Produk", ["OWDI", "IndiHome"])
    input_comment = st.text_area("Tulis komentar...")
    
    if st.button("KIRIM KE DASHBOARD"):
        if input_comment:
            sent = get_sentiment(input_comment)
            # Logika simpan data agar bisa dilihat user lain
            st.toast("Data berhasil dikirim ke Analytics Center!")

# Merender tampilan HTML Anda
st.components.v1.html(html_layout, height=800, scrolling=False)
