import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Konfigurasi Halaman (Harus di awal)
st.set_page_config(page_title="VoC TRACTION Product", layout="wide", initial_sidebar_state="expanded")

# 2. Injeksi CSS Kustom agar Identik dengan index.html
st.markdown("""
<style>
    /* Reset & Global Styles */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #020617);
        color: #f1f5f9;
    }
    header, footer {visibility: hidden;}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #334155;
    }

    /* Typography */
    h1, h2, h3, p { font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Comment Card Style */
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

    /* AI Strategic Card */
    .ai-card { 
        width: 100%; padding: 20px; border-radius: 18px; font-size: 13px; line-height: 1.6;
        background: linear-gradient(145deg, rgba(239, 68, 68, 0.08), rgba(0,0,0,0.02));
        border: 1px solid rgba(239, 68, 68, 0.2); 
    }

    /* Scrollbar Styling agar Sleek */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }

    /* Sidebar Button Simulation */
    .group-tag {
        font-size: 10px; color: #64748b; font-weight: 800; text-transform: uppercase;
        letter-spacing: 1.5px; margin: 25px 0 12px 10px; display: flex; align-items: center; gap: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Logika Database (Lokal)
DB_FILE = "voc_data.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["product", "comment"]).to_csv(DB_FILE, index=False)

def get_sentiment(text):
    t = str(text).lower()
    pos = ['😍', '🥰', '👍', 'best', 'mantap', 'keren', 'puas', 'gercep', 'untung', 'bagus']
    neg = ['hancur', 'buruk', 'parah', 'kecewa', 'penipu', 'nyesel', 'lelet', 'jelek', 'rugi', 'pindah', 'cabut']
    score = sum(3 for w in pos if w in t) - sum(4 for w in neg if w in t)
    return "Positive" if score >= 2 else ("Negative" if score <= -2 else "Neutral")

# 4. Sidebar Rendering
with st.sidebar:
    st.markdown("""
        <div style="padding: 10px 0 20px 0;">
            <h2 style="margin:0; font-size:20px; font-weight:800; letter-spacing:-1px; color:white;">VoC <span style="color:#ef4444">TRACTION Product</span></h2>
            <div style="font-size:10px; color:#64748b; font-weight:600;">TELKOMSEL ANALYTICS</div>
        </div>
        <hr style="border-color:#334155; margin-bottom:20px;">
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="group-tag">MOBILE SERVICE</div>', unsafe_allow_html=True)
    # Gunakan selectbox untuk navigasi agar fungsional di Streamlit
    nav_list = ["OWDI", "IndiHome", "ALL"]
    active_cat = st.radio("Navigation", nav_list, label_visibility="collapsed")
    
    st.divider()
    st.markdown('<div class="group-tag">MANAGEMENT</div>', unsafe_allow_html=True)
    new_p = st.text_input("Product Name", placeholder="Input name...")
    if st.button("ADD NEW PRODUCT", use_container_width=True):
        st.toast(f"Product {new_p} Added!")

# 5. Main Layout (Left: Comments, Right: Analytics)
col_left, col_right = st.columns([2.5, 1], gap="large")

with col_left:
    st.markdown(f"<h1 style='margin:0; font-size:32px; font-weight:800;'>{active_cat}</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; font-size:14px; margin-bottom:25px;'>Monitoring ulasan pelanggan secara real-time.</p>", unsafe_allow_html=True)
    
    # Upload Data
    if active_cat != "ALL":
        uploaded_file = st.file_uploader("📂 IMPORT CSV", type="csv")
        if uploaded_file:
            df_new = pd.read_csv(uploaded_file)
            df_new = df_new.iloc[:, [0]] # Ambil kolom pertama
            df_new.columns = ['comment']
            df_new['product'] = active_cat
            
            main_db = pd.read_csv(DB_FILE)
            pd.concat([main_db, df_new]).to_csv(DB_FILE, index=False)
            st.toast(f"Success! {len(df_new)} rows added.")
            st.rerun()

    # Tampilkan Data Komentar dalam Scrollable Container
    db = pd.read_csv(DB_FILE)
    filtered = db if active_cat == "ALL" else db[db['product'] == active_cat]
    
    if filtered.empty:
        st.markdown("<div style='text-align:center; padding-top:100px; opacity:0.3; font-size:16px; font-weight:800;'>KOSONG. IMPORT CSV UNTUK MULAI.</div>", unsafe_allow_html=True)
    else:
        # Container dengan tinggi tetap agar bisa di-scroll secara independen
        with st.container(height=500):
            for _, row in filtered.iloc[::-1].iterrows():
                sentiment = get_sentiment(row['comment'])
                st.markdown(f"""
                    <div class="comment-card {sentiment}">
                        <div style="font-size:14px; flex:1; padding-right:20px; color:#f1f5f9;">"{row['comment']}"</div>
                        <span class="tag {sentiment}">{sentiment}</span>
                    </div>
                """, unsafe_allow_html=True)

# 6. Analytics Center (Sisi Kanan)
with col_right:
    st.markdown("<h3 style='margin-top:0; font-size:18px; font-weight:800;'>Analytics Center</h3>", unsafe_allow_html=True)
    
    if not filtered.empty:
        # Hitung Sentimen
        db_sent = filtered.copy()
        db_sent['sentiment'] = db_sent['comment'].apply(get_sentiment)
        counts = db_sent['sentiment'].value_counts()
        pos = counts.get('Positive', 0)
        neg = counts.get('Negative', 0)
        neu = counts.get('Neutral', 0)

        # Chart Doughnut (Plotly)
        fig = px.pie(
            values=[pos, neg, neu], 
            names=['Positive', 'Negative', 'Neutral'], 
            hole=0.8,
            color=['Positive', 'Negative', 'Neutral'],
            color_discrete_map={'Positive':'#22c55e', 'Negative':'#ef4444', 'Neutral':'#64748b'}
        )
        fig.update_layout(
            showlegend=False, 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            height=200, 
            margin=dict(t=0, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Strategic Card (Identik dengan HTML)
        st.markdown(f"""
            <div class="ai-card">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                    <div style="width:8px; height:8px; background:#ef4444; border-radius:50%"></div>
                    <b style="font-size:11px; letter-spacing:1px; color:white;">SUMMARY REPORT</b>
                </div>
                <div style="display:flex; gap:15px; font-weight:700; margin-bottom:15px; color:white;">
                    <span>🟢 {pos}</span> <span>🔴 {neg}</span> <span>⚪ {neu}</span>
                </div>
                <div style="color:#94a3b8; font-size:12px;">
                    <b>Insight:</b> { 'Sentimen positif mendominasi. Pertahankan layanan.' if pos > neg else 'Ditemukan anomali sentimen negatif. Segera periksa jalur teknis.' }
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#64748b; font-size:12px;'>No data available for analytics.</p>", unsafe_allow_html=True)
