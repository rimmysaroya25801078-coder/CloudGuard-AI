import streamlit as st
import pandas as pd
import numpy as np
import re
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="CloudGuard AI", page_icon="🛡️")

def extract_features(url):
    parsed = urlparse(url if "://" in url else "http://" + url)
    hostname = parsed.netloc
    url_length = len(url)
    has_ip = 1 if re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', hostname) else 0
    special_chars = sum(url.count(c) for c in ['@', '-', '_', '?', '=', '%'])
    is_insecure = 0 if url.lower().startswith("https://") else 1
    words = ['login', 'verify', 'update', 'secure', 'banking', 'account', 'free']
    keyword_count = sum(1 for w in words if w in url.lower())
    dot_count = hostname.count('.')
    return [url_length, has_ip, special_chars, is_insecure, keyword_count, dot_count]

@st.cache_resource
def train_model():
    X = np.array([
        [22, 0, 0, 0, 0, 1], [28, 0, 1, 0, 0, 2], [35, 0, 2, 0, 0, 1],
        [19, 0, 0, 0, 0, 1], [42, 0, 2, 0, 0, 2], [25, 0, 0, 0, 0, 2],
        [85, 1, 6, 1, 2, 3], [110, 0, 9, 1, 3, 4], [75, 1, 5, 1, 2, 2],
        [95, 0, 7, 0, 3, 4], [64, 1, 4, 1, 1, 3], [120, 0, 11, 1, 4, 5]
    ])
    y = np.array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    return model

model = train_model()

st.title("🛡️ CloudGuard AI: Cyber Threat Detector")
st.write("**Python + Cloud Computing + Cyber Security and AI Project**")
st.write("**Submitted By:** Rimmy Saroya (25801078) | **SBBSU**")
st.divider()

url_input = st.selectbox(
    "Select a Website URL to Scan:",
    [
        "https://www.sbbsuniversity.ac.in",
        "https://github.com",
        "http://192.168.0.1/verify-bank-account-login/update.php",
        "http://free-bonus-secure-login.com/account-update"
    ]
)

custom_url = st.text_input("Or type any URL here (optional):")
target_url = custom_url if custom_url else url_input

if st.button("Scan URL with AI", type="primary"):
    features = extract_features(target_url)
    prediction = model.predict([features])[0]
    risk = round(model.predict_proba([features])[0][1] * 100, 1)

    if prediction == 1:
        st.error(f"🚨 DANGER: Phishing / Malicious Website Detected! (Risk Score: {risk}%)")
    else:
        st.success(f"✅ SAFE: Legitimate Website Detected! (Risk Score: {risk}%)")

    df = pd.DataFrame({
        "Security Check": ["URL Length", "Hidden IP Address", "Special Symbols", "Missing HTTPS", "Suspicious Words", "Subdomains"],
        "Score": features
    })
    st.table(df)
