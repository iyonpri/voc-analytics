import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="VoC TRACTION Product", layout="wide")

# --- CUSTOM CSS (Identik dengan HTML Anda) ---
st.markdown("""
    <style>
    /* Global Background & Font */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #020617);
        color: #f1f5f9;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #334155;
    }

    /* Comment Card dengan Scroll independent */
    .comment-card { 
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(10px);
        padding: 18px;
        border-radius: 14px;
        margin-bottom: 15px; 
        border: 1px solid #334155;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .comment-card.Positive { border-left: 4px solid #22c55e; }
    .comment-card.Negative { border-left: 4px solid #f87171; }
    .comment-card.Neutral { border-left: 1px solid #334155; }

    /* Tags Sentiment */
    .tag { 
        font-size: 9px; padding: 4px 10px; border-radius: 6px; 
        font-weight: 800; color: white; text-transform: uppercase; 
    }
    .tag.Positive { background: #22c55e; }
    .tag.Negative { background: #f87171; }
    .tag.Neutral { background: #64748b; }

    /* AI Card Summary */
    .ai-card { 
        width: 100%; padding: 20px; border-radius: 18px; font-size: 13px;
        background: linear-gradient(145deg, rgba(239, 68, 68, 0.08), rgba(0,0,0,0.02));
        border: 1px solid rgba(239, 68, 68, 0.2); 
    }

    /* Sembunyikan Header Streamlit */
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIKA DATABASE (CSV LOKAL) ---
DB_FILE = "voc_db.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["product", "comment", "sentiment"]).to_csv(DB_FILE, index=False)

def get_sentiment(text):
    t = str(text).lower()
    pos = ['mantap', 'keren', 'puas', 'bagus', 'gercep', '😍']
    neg = ['parah', 'kecewa', 'lelet', 'jelek', 'rugi', 'hancur', 'mahal']
    score = sum(3 for w in pos if w in t) - sum(4 for w in neg if w in t)
    return "Positive" if score >= 2 else ("Negative" if score <= -2 else "Neutral")

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:white;'>VoC <span style='color:#ef4444;'>TRACTION Hub</span></h2>", unsafe_allow_html=True)
    st.caption("TELKOMSEL ANALYTICS")
    st.divider()
    
    # List Produk
    product_list = ["OWDI", "Perplexity Pro", "ChatGPT Go", "ALL"]
    active_cat = st.radio("MOBILE SERVICE", product_list)
    
    st.divider()
    with st.expander("➕ Add New Product"):
        new_p = st.text_input("Nama Produk")
        if st.button("ADD PRODUCT", use_container_width=True):
            st.toast(f"Produk {new_p} ditambahkan!")

# --- MAIN CONTENT ---
col_left, col_right = st.columns([2.5, 1], gap="large")

with col_left:
    st.markdown(f"<h1>{active_cat}</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;'>Monitoring ulasan pelanggan secara real-time.</p>", unsafe_allow_html=True)
    
    # Fitur Unggah File
    uploaded_file = st.file_uploader("Upload CSV", type="csv", label_visibility="collapsed")
    if uploaded_file and active_cat != "ALL":
        df_new = pd.read_csv(uploaded_file)
        df_new = df_new.iloc[:, [0]] # Ambil kolom pertama
        df_new.columns = ['comment']
        df_new['product'] = active_cat
        df_new['sentiment'] = df_new['comment'].apply(get_sentiment)
        
        main_db = pd.read_csv(DB_FILE)
        pd.concat([main_db, df_new]).to_csv(DB_FILE, index=False)
        st.toast(f"Sukses! {len(df_new)} data ditambahkan.")
        st.rerun()

    # Load & Tampilkan Data dengan Scrollbar
    db = pd.read_csv(DB_FILE)
    filtered = db if active_cat == "ALL" else db[db['product'] == active_cat]
    
    if filtered.empty:
        st.info("KOSONG. IMPORT CSV UNTUK MULAI.")
    else:
        # Menggunakan height agar bisa di-scroll secara independen
        with st.container(height=550):
            for _, row in filtered.iloc[::-1].iterrows():
                st.markdown(f"""
                    <div class="comment-card {row['sentiment']}">
                        <div style="font-size:14px; flex:1; padding-right:20px;">"{row['comment']}"</div>
                        <span class="tag {row['sentiment']}">{row['sentiment']}</span>
                    </div>
                """, unsafe_allow_html=True)

# --- ANALYTICS CENTER (SISI KANAN) ---
with col_right:
    st.markdown("<h3 style='margin-top:0;'>Analytics Center</h3>", unsafe_allow_html=True)
    if not filtered.empty:
        counts = filtered['sentiment'].value_counts()
        fig = px.pie(values=counts.values, names=counts.index, hole=0.8,
                     color=counts.index, color_discrete_map={'Positive':'#22c55e','Negative':'#ef4444','Neutral':'#64748b'})
        fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

        # AI Summary Card
        st.markdown(f"""
            <div class="ai-card">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                    <div style="width:8px; height:8px; background:#ef4444; border-radius:50%"></div>
                    <b style="font-size:11px;">SUMMARY REPORT</b>
                </div>
                🟢 {counts.get('Positive',0)} | 🔴 {counts.get('Negative',0)} | ⚪ {counts.get('Neutral',0)}<br><br>
                <b>Insight:</b> { 'Sentimen positif mendominasi.' if counts.get('Positive',0) > counts.get('Negative',0) else 'Keluhan teknis meningkat.' }
            </div>
        """, unsafe_allow_html=True)
