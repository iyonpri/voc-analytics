import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- SETUP HALAMAN ---
st.set_page_config(page_title="VoC TRACTION", layout="wide")

# --- DATABASE SIMULASI (Agar bisa online, kita gunakan st.session_state) ---
# Note: Untuk permanen selamanya bagi tim, nanti tinggal hubungkan ke Google Sheets
if 'database' not in st.session_state:
    st.session_state.database = pd.DataFrame([
        {"product": "OWDI", "comment": "Sinyal mantap bgt", "sentiment": "Positive"},
        {"comment": "MAHAL BANGET NYESEL", "product": "OWDI", "sentiment": "Negative"}
    ])

# --- INJEKSI CSS & HTML (SAMA PERSIS DENGAN INDEX.HTML ANDA) ---
st.markdown(f"""
<style>
    /* Reset Streamlit */
    [data-testid="stAppViewContainer"] {{ background: radial-gradient(circle at top right, #1e293b, #020617); }}
    [data-testid="stHeader"], [data-testid="stToolbar"] {{ display: none; }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{ background-color: #0f172a !important; border-right: 1px solid #334155; }}

    /* Font & Card Style (DARI INDEX.HTML ANDA) */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    * {{ font-family: 'Plus Jakarta Sans', sans-serif; }}

    .comment-card {{ 
        background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(10px);
        padding: 20px; border-radius: 14px; margin-bottom: 15px; 
        border: 1px solid #334155; display: flex; align-items: center; justify-content: space-between;
    }}
    .comment-card.Positive {{ border-left: 4px solid #22c55e; }}
    .comment-card.Negative {{ border-left: 4px solid #f87171; }}
    
    .tag {{ font-size:9px; padding:4px 10px; border-radius:6px; font-weight:800; color:white; text-transform:uppercase; }}
    .tag.Negative {{ background:#f87171; }} .tag.Positive {{ background:#22c55e; }} .tag.Neutral {{ background:#64748b; }}

    .ai-card {{ 
        width: 100%; padding:20px; border-radius:18px; font-size:13px; line-height:1.6;
        background: linear-gradient(145deg, rgba(239, 68, 68, 0.08), rgba(0,0,0,0.02));
        border:1px solid rgba(239, 68, 68, 0.2); color: white;
    }}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGASI ---
with st.sidebar:
    st.markdown("""<h2 style='color:white; font-weight:800;'>VoC <span style='color:#ef4444'>TRACTION</span></h2>""", unsafe_allow_html=True)
    product_choice = st.selectbox("Pilih Produk", ["OWDI", "IndiHome", "ALL"])
    st.divider()
    
    # Form Tambah Data (Agar Orang Lain Bisa Add)
    st.markdown("### Add New Feedback")
    new_comment = st.text_area("Tulis ulasan...", height=100)
    if st.button("KIRIM ULASAN"):
        if new_comment:
            # Logika Sentimen Sederhana
            sent = "Positive" if any(x in new_comment.lower() for x in ['bagus','mantap','puas']) else "Negative"
            new_data = pd.DataFrame([{"product": product_choice, "comment": new_comment, "sentiment": sent}])
            st.session_state.database = pd.concat([st.session_state.database, new_data], ignore_index=True)
            st.toast("Ulasan terkirim!")
            st.rerun()

# --- MAIN CONTENT ---
col1, col2 = st.columns([2.5, 1])

with col1:
    st.markdown(f"<h1 style='color:white;'>{product_choice}</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;'>Monitoring ulasan pelanggan secara real-time.</p>", unsafe_allow_html=True)
    
    # Filter Data
    df = st.session_state.database
    if product_choice != "ALL":
        df = df[df['product'] == product_choice]
    
    # RENDER COMMENT CARDS (PERSIS HTML)
    # Gunakan Container agar bisa scroll
    with st.container(height=500):
        for _, row in df.iloc[::-1].iterrows():
            st.markdown(f"""
                <div class="comment-card {row['sentiment']}">
                    <div style="font-size:14px; color:white; flex:1; padding-right:20px;">"{row['comment']}"</div>
                    <span class="tag {row['sentiment']}">{row['sentiment']}</span>
                </div>
            """, unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='color:white;'>Analytics Center</h3>", unsafe_allow_html=True)
    
    # CHART DOUGHNUT
    counts = df['sentiment'].value_counts()
    fig = px.pie(values=counts.values, names=counts.index, hole=0.7,
                 color=counts.index, color_discrete_map={'Positive':'#22c55e','Negative':'#ef4444','Neutral':'#64748b'})
    fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=200, margin=dict(t=0,b=0,l=0,r=0))
    st.plotly_chart(fig, use_container_width=True)

    # AI SUMMARY CARD
    pos = (df['sentiment'] == "Positive").sum()
    neg = (df['sentiment'] == "Negative").sum()
    st.markdown(f"""
        <div class="ai-card">
            <b style="font-size:11px; color:#ef4444;">SUMMARY REPORT</b><br>
            🟢 {pos} | 🔴 {neg}<br><br>
            <b>Insight:</b> Data diperbarui secara real-time dari kontribusi tim.
        </div>
    """, unsafe_allow_html=True)
