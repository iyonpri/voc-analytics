import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="VoC TRACTION Product", layout="wide", initial_sidebar_state="expanded")

# --- 2. CSS INJECTION (Identik dengan HTML Anda) ---
st.markdown("""
    <style>
    /* Menghilangkan header default streamlit */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Background Utama */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #020617);
        color: #f1f5f9;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #334155;
    }

    /* Custom Comment Card */
    .comment-card { 
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 15px; 
        border: 1px solid #334155;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: 0.3s;
    }
    .comment-card.Positive { border-left: 4px solid #22c55e; }
    .comment-card.Negative { border-left: 4px solid #f87171; }
    .comment-card.Neutral { border-left: 1px solid #334155; }

    /* Tags */
    .tag { 
        font-size: 9px; padding: 4px 10px; border-radius: 6px; 
        font-weight: 800; color: white; text-transform: uppercase; 
    }
    .tag.Positive { background: #22c55e; }
    .tag.Negative { background: #f87171; }
    .tag.Neutral { background: #64748b; }

    /* AI Card Summary */
    .ai-card { 
        width: 100%; padding: 20px; border-radius: 18px; font-size: 13px; line-height: 1.6;
        background: linear-gradient(145deg, rgba(239, 68, 68, 0.08), rgba(0,0,0,0.02));
        border: 1px solid rgba(239, 68, 68, 0.2); 
    }
    
    /* Typography */
    h1, h2, h3 { color: #f1f5f9 !important; font-family: 'Plus Jakarta Sans', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIKA SENTIMEN ---
def get_sentiment(text):
    t = str(text).lower()
    pos = ['😍', '🥰', '👍', 'best', 'mantap', 'keren', 'puas', 'gercep', 'untung', 'bagus']
    neg = ['hancur', 'buruk', 'parah', 'kecewa', 'penipu', 'nyesel', 'lelet', 'jelek', 'rugi', 'pindah', 'cabut']
    score = sum(3 for w in pos if w in t) - sum(4 for w in neg if w in t)
    return "Positive" if score >= 2 else ("Negative" if score <= -2 else "Neutral")

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0 20px 0;">
            <h2 style="margin:0; font-size:20px; font-weight:800;">VoC <span style="color:#ef4444">TRACTION Product</span></h2>
            <div style="font-size:10px; color:#64748b; font-weight:600;">TELKOMSEL ANALYTICS</div>
        </div>
        <hr style="border-color:#334155;">
    """, unsafe_allow_html=True)
    
    # Navigasi ala Sidebar Anda
    st.markdown("<div style='font-size:10px; color:#64748b; font-weight:800; margin-bottom:10px;'>MOBILE SERVICE</div>", unsafe_allow_html=True)
    selected_product = st.radio("Pilih Produk", ["OWDI", "Perplexity Pro", "ChatGPT Go", "ALL"], label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("➕ Add New Product"):
        new_name = st.text_input("Nama Produk")
        if st.button("ADD NEW PRODUCT", use_container_width=True):
            st.toast(f"Produk {new_name} ditambahkan!")

# --- 5. MAIN CONTENT ---
col_left, col_right = st.columns([2.5, 1], gap="large")

with col_left:
    st.markdown(f"<h1 style='margin-bottom:0;'>{selected_product}</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:14px;'>Monitoring ulasan pelanggan secara real-time.</p>", unsafe_allow_html=True)
    
    # Tombol Import CSV (Streamlit Native Button disesuaikan)
    uploaded_file = st.file_uploader("📂 IMPORT CSV", type="csv", label_visibility="collapsed")
    
    # Simulasi Data Komentar (Sesuai gambar)
    data = [
        {"comment": "Infonya bermanfaat bgt", "sentiment": "Neutral"},
        {"comment": "Thank you for information 😍", "sentiment": "Positive"},
        {"comment": "Mantap", "sentiment": "Positive"},
        {"comment": "BALAS DM min MAU CABUT. GAK KUAT MAHALNYA", "sentiment": "Negative"}
    ]
    
    # Render Card Ulasan (Identik dengan)
    for item in data:
        st.markdown(f"""
            <div class="comment-card {item['sentiment']}">
                <div style="font-size:14px; flex:1; padding-right:20px; color:#f1f5f9;">"{item['comment']}"</div>
                <span class="tag {item['sentiment']}">{item['sentiment']}</span>
            </div>
        """, unsafe_allow_html=True)

# --- 6. SUMMARY & ANALYTICS ---
with col_right:
    st.markdown("<h3 style='margin-top:0;'>Analytics Center</h3>", unsafe_allow_html=True)
    
    # Chart Doughnut (Plotly transparan agar menyatu dengan background)
    fig = px.pie(values=[43, 24, 412], names=['Pos', 'Neg', 'Neu'], hole=0.8,
                 color_discrete_sequence=['#22c55e', '#ef4444', '#64748b'])
    fig.update_layout(
        showlegend=False, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        height=200, 
        margin=dict(t=0, b=0, l=0, r=0)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # AI Strategic Report (Identik dengan)
    st.markdown(f"""
        <div class="ai-card">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                <div style="width:8px; height:8px; background:#ef4444; border-radius:50%"></div>
                <b style="font-size:11px; letter-spacing:1px;">SUMMARY REPORT</b>
            </div>
            <div style="display:flex; gap:15px; font-weight:700; margin-bottom:15px;">
                <span>🟢 43</span> <span>🔴 24</span> <span>⚪ 412</span>
            </div>
            <b>Insight:</b> Sentimen positif mendominasi. Pertahankan layanan.
        </div>
    """, unsafe_allow_html=True)
