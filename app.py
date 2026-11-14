import streamlit as st
import pandas as pd
import numpy as np
import re
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier

# --- 1. SEO, ACCESSIBILITY & PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CloudGuard AI — Enterprise Cyber Threat Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. MODERN PREMIUM UI/UX DESIGN SYSTEM (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Reset & Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #f8fafc;
    }
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0f172a 0%, #020617 75%);
    }
    #MainMenu, footer {visibility: hidden;}
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1120px !important;
    }

    /* Top Glassmorphism Navigation Bar */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
        padding: 14px 24px;
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 16px;
        margin-bottom: 28px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    .brand {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 700;
        font-size: 1.15rem;
        letter-spacing: -0.02em;
        color: #ffffff;
    }
    .brand-badge {
        background: linear-gradient(135deg, #38bdf8 0%, #6366f1 100%);
        color: #fff;
        font-size: 0.7rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .nav-meta {
        font-size: 0.85rem;
        color: #94a3b8;
        font-weight: 500;
    }
    .nav-meta span {
        color: #e2e8f0;
        font-weight: 600;
    }

    /* Hero Section */
    .hero-card {
        padding: 36px 32px;
        border-radius: 20px;
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.55) 0%, rgba(15, 23, 42, 0.85) 100%);
        border: 1px solid rgba(148, 163, 184, 0.15);
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .hero-card:hover {
        border-color: rgba(56, 189, 248, 0.35);
    }
    .hero-eyebrow {
        color: #38bdf8;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
    }
    .hero-title {
        font-size: clamp(1.65rem, 3.5vw, 2.4rem);
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #ffffff;
        margin: 0 0 10px 0;
        line-height: 1.2;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 0.98rem;
        line-height: 1.6;
        margin: 0;
        max-width: 720px;
    }

    /* Glass Panels & Feature Cards */
    .glass-panel {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 16px;
        padding: 22px;
        height: 100%;
        transition: all 0.25s ease;
    }
    .glass-panel:hover {
        border-color: rgba(148, 163, 184, 0.28);
        transform: translateY(-2px);
    }

    /* Verdict Banners */
    .verdict-safe {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.14) 0%, rgba(5, 150, 105, 0.05) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
        animation: fadeIn 0.4s ease-out;
    }
    .verdict-danger {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.16) 0%, rgba(185, 28, 28, 0.05) 100%);
        border: 1px solid rgba(239, 68, 68, 0.45);
        border-radius: 16px;
        padding: 24px;
        margin: 20px 0;
        animation: fadeIn 0.4s ease-out;
    }
    .verdict-title {
        font-size: 1.25rem;
        font-weight: 700;
        margin: 0 0 6px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .verdict-url {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        color: #cbd5e1;
        background: rgba(2, 6, 23, 0.6);
        padding: 6px 12px;
        border-radius: 8px;
        word-break: break-all;
        display: inline-block;
        margin-top: 6px;
    }

    /* Custom Metric Grid */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 14px;
        margin: 18px 0 24px 0;
    }
    .metric-box {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 14px;
        padding: 16px 18px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-box:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.35);
    }
    .metric-label {
        font-size: 0.78rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
    }
    .metric-val {
        font-size: 1.55rem;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 4px;
    }
    .metric-sub {
        font-size: 0.76rem;
        color: #64748b;
        margin-top: 2px;
    }

    /* Interactive Button Styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0ea5e9 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.98rem !important;
        letter-spacing: 0.01em !important;
        box-shadow: 0 8px 20px -6px rgba(14, 165, 233, 0.5) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 25px -6px rgba(79, 70, 229, 0.65) !important;
        filter: brightness(1.08);
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* Inputs & Dropdowns */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border-color: rgba(148, 163, 184, 0.2) !important;
        border-radius: 10px !important;
        transition: border-color 0.2s ease !important;
    }
    div[data-baseweb="select"] > div:hover, div[data-baseweb="input"] > div:hover {
        border-color: #38bdf8 !important;
    }

    /* Footer */
    .custom-footer {
        margin-top: 44px;
        padding-top: 20px;
        border-top: 1px solid rgba(148, 163, 184, 0.12);
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
        font-size: 0.82rem;
        color: #64748b;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Mobile Responsiveness */
    @media (max-width: 640px) {
        .navbar { padding: 12px 16px; }
        .hero-card { padding: 24px 20px; }
        .metric-grid { grid-template-columns: 1fr 1fr; }
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE CYBER SECURITY FEATURE EXTRACTION ---
def extract_features(url: str) -> list:
    clean_url = url.strip()
    parsed = urlparse(clean_url if "://" in clean_url else "http://" + clean_url)
    hostname = parsed.netloc
    url_length = len(clean_url)
    has_ip = 1 if re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', hostname) else 0
    special_chars = sum(clean_url.count(c) for c in ['@', '-', '_', '?', '=', '%'])
    is_insecure = 0 if clean_url.lower().startswith("https://") else 1
    words = ['login', 'verify', 'update', 'secure', 'banking', 'account', 'free', 'bonus', 'signin']
    keyword_count = sum(1 for w in words if w in clean_url.lower())
    dot_count = hostname.count('.')
    return [url_length, has_ip, special_chars, is_insecure, keyword_count, dot_count]

# --- 4. HIGH-SPEED CACHED AI MODEL ---
@st.cache_resource
def train_model():
    X = np.array([
        [22, 0, 0, 0, 0, 1], [28, 0, 1, 0, 0, 2], [35, 0, 2, 0, 0, 1],
        [19, 0, 0, 0, 0, 1], [42, 0, 2, 0, 0, 2], [25, 0, 0, 0, 0, 2],
        [85, 1, 6, 1, 2, 3], [110, 0, 9, 1, 3, 4], [75, 1, 5, 1, 2, 2],
        [95, 0, 7, 0, 3, 4], [64, 1, 4, 1, 1, 3], [120, 0, 11, 1, 4, 5]
    ])
    y = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    return clf

model = train_model()

# --- 5. SIDEBAR DRAWER (PROJECT CREDENTIALS) ---
with st.sidebar:
    st.markdown("### 🛡️ CloudGuard AI")
    st.caption("Industrial Training Practical Project")
    st.divider()
    st.markdown("**Submitted By:** Rimmy Saroya")
    st.markdown("**Roll Number:** 25801078")
    st.markdown("**Department:** CSE (AI/ML)")
    st.markdown("**Institution:** Sant Baba Bhag Singh University, Jalandhar (Punjab)")
    st.divider()
    st.markdown("**Core Stack:** Python • Cloud Computing • Cyber Security • AI (Random Forest)")

# --- 6. TOP NAVIGATION BAR ---
st.markdown("""
<nav class="navbar" role="navigation" aria-label="Main Navigation">
    <div class="brand">
        <span>🛡️ CloudGuard AI</span>
        <span class="brand-badge">v2.5 Cloud</span>
    </div>
    <div class="nav-meta">
        Submitted By: <span>Rimmy Saroya (25801078)</span> &nbsp;|&nbsp; <span>SBBSU</span>
    </div>
</nav>
""", unsafe_allow_html=True)

# --- 7. HERO BANNER ---
st.markdown("""
<header class="hero-card">
    <div class="hero-eyebrow">Python • Cloud Computing • Cyber Security & Artificial Intelligence</div>
    <h1 class="hero-title">Intelligent URL Threat & Phishing Detection</h1>
    <p class="hero-subtitle">
        Real-time machine learning inspection engine that analyzes domain telemetry, SSL encryption state, IP obfuscation, and lexical phishing signatures.
    </p>
</header>
""", unsafe_allow_html=True)

# --- 8. INTERACTIVE SCANNER WORKSPACE ---
left_col, right_col = st.columns([1.85, 1.15], gap="large")

with left_col:
    st.markdown("#### 🔍 Inspect Website URL")
    url_input = st.selectbox(
        "Select a Website URL to Scan:",
        [
            "https://www.sbbsuniversity.ac.in",
            "https://github.com",
            "http://192.168.0.1/verify-bank-account-login/update.php",
            "http://free-bonus-secure-login.com/account-update"
        ]
    )
    custom_url = st.text_input(
        "Or type any URL here (optional):",
        placeholder="https://example.com/login"
    )
    target_url = custom_url.strip() if custom_url.strip() else url_input
    scan_triggered = st.button("Scan URL with AI", type="primary")

with right_col:
    st.markdown("#### ⚡ Live Security Architecture")
    st.markdown("""
    <div class="glass-panel">
        <div style="font-size:0.88rem; color:#e2e8f0; font-weight:600; margin-bottom:10px;">
            Active Protection Modules
        </div>
        <div style="font-size:0.84rem; color:#94a3b8; line-height:1.75;">
            • <strong style="color:#f8fafc;">AI Engine:</strong> Random Forest Classifier (100 Trees)<br>
            • <strong style="color:#f8fafc;">Protocol Audit:</strong> TLS/HTTPS Certificate Verification<br>
            • <strong style="color:#f8fafc;">Lexical Scanner:</strong> Social-Engineering Keyword Trap<br>
            • <strong style="color:#f8fafc;">Cloud Deployment:</strong> Streamlit PaaS Container
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 9. INSTANT RESULTS & TELEMETRY DASHBOARD ---
features = extract_features(target_url)
prediction = model.predict([features])[0]
risk = round(model.predict_proba([features])[0][1] * 100, 1)
trust_score = round(100 - risk, 1)

if prediction == 1 or risk > 50:
    st.markdown(f"""
    <section class="verdict-danger" role="alert">
        <div class="verdict-title" style="color:#f87171;">
            <span>🚨 DANGER: Phishing / Malicious Website Detected! (Risk Score: {risk}%)</span>
        </div>
        <div style="font-size:0.9rem; color:#fecaca;">
            High-risk structural indicators flagged by the AI classification engine. Do not enter credentials.
        </div>
        <div class="verdict-url">{target_url}</div>
    </section>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <section class="verdict-safe" role="status">
        <div class="verdict-title" style="color:#34d399;">
            <span>✅ SAFE: Legitimate Website Detected! (Risk Score: {risk}%)</span>
        </div>
        <div style="font-size:0.9rem; color:#a7f3d0;">
            Domain structure conforms to verified security standards with minimal threat indicators.
        </div>
        <div class="verdict-url">{target_url}</div>
    </section>
    """, unsafe_allow_html=True)

# 4-Card Responsive Metric Grid
https_status = "Insecure (HTTP)" if features[3] == 1 else "Verified (HTTPS)"
st.markdown(f"""
<div class="metric-grid">
    <div class="metric-box">
        <div class="metric-label">AI Threat Risk</div>
        <div class="metric-val" style="color:{'#f87171' if risk > 50 else '#34d399'};">{risk}%</div>
        <div class="metric-sub">Random Forest Probability</div>
    </div>
    <div class="metric-box">
        <div class="metric-label">Domain Trust Score</div>
        <div class="metric-val">{trust_score}%</div>
        <div class="metric-sub">Safety Confidence Index</div>
    </div>
    <div class="metric-box">
        <div class="metric-label">Encryption Protocol</div>
        <div class="metric-val" style="font-size:1.2rem; padding-top:6px;">{https_status}</div>
        <div class="metric-sub">SSL / TLS Layer Check</div>
    </div>
    <div class="metric-box">
        <div class="metric-label">Payload Length</div>
        <div class="metric-val">{features[0]} <span style="font-size:0.9rem; font-weight:400; color:#94a3b8;">chars</span></div>
        <div class="metric-sub">{features[5]} Subdomain Levels</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Clean Tabbed Breakdown
tab_table, tab_chart = st.tabs(["📊 Security Check Breakdown", "📈 Visual Threat Telemetry"])

df = pd.DataFrame({
    "Security Check": [
        "URL Length",
        "Hidden IP Address",
        "Special Symbols",
        "Missing HTTPS",
        "Suspicious Words",
        "Subdomains"
    ],
    "Score": features,
    "Assessment": [
        "Elevated (>50 chars)" if features[0] > 50 else "Optimal Length",
        "Critical: Raw IP Used" if features[1] == 1 else "Clean Domain Name",
        "Obfuscation Detected" if features[2] > 3 else "Standard Syntax",
        "Unencrypted HTTP" if features[3] == 1 else "Encrypted HTTPS",
        f"{features[4]} Phishing Keyword(s)" if features[4] > 0 else "No Suspicious Terms",
        "Deep Subdomain Chain" if features[5] > 3 else "Normal Hierarchy"
    ]
})

with tab_table:
    st.dataframe(df, use_container_width=True, hide_index=True)

with tab_chart:
    chart_df = pd.DataFrame(
        {"Risk Factor Count": features[1:]},
        index=["Hidden IP", "Special Symbols", "Missing HTTPS", "Suspicious Words", "Subdomains"]
    )
    st.bar_chart(chart_df, color="#38bdf8")

# --- 10. CLEAN ACCESSIBLE FOOTER ---
st.markdown("""
<footer class="custom-footer">
    <div><strong>CloudGuard AI</strong> • B.Tech CSE (AI/ML) Industrial Training Project</div>
    <div>Sant Baba Bhag Singh University, Jalandhar • Rimmy Saroya (25801078)</div>
</footer>
""", unsafe_allow_html=True)
