import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from scanner import run_scan, load_latest_report

st.set_page_config(page_title="Security Dashboard", layout="wide")

st.title("🔐 Security Analysis & Vulnerability Dashboard")

# Sidebar
st.sidebar.header("Scan Options")
files = os.listdir("sample_code")
code_files = [f for f in files if f.endswith((".py", ".java", ".c", ".cpp"))]

selected_file = st.sidebar.selectbox("Choose file to scan:", code_files)

if st.sidebar.button("🔍 Scan Selected File"):
    with st.spinner(f"Scanning {selected_file}..."):
        run_scan(local_path=f"sample_code/{selected_file}")
    st.success("✅ Scan complete!")

# Load report
data = load_latest_report()

if not data:
    st.warning("No scan reports found. Run a scan first.")
    st.stop()

results = data.get("results", [])
repo_url = data.get("repo_url", "local")

# ── Top Info ───────────────────────────────────────────
st.info(f"📊 Scanned: **{selected_file}** | Languages: **{', '.join(data.get('languages', ['None']))}**")

# ── KPI Cards ──────────────────────────────────────────
total = len(results)
critical = sum(1 for r in results if r["severity"] == "HIGH")
medium   = sum(1 for r in results if r["severity"] == "MEDIUM")
low      = sum(1 for r in results if r["severity"] == "LOW")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Issues", total)
col2.metric("🔴 High", critical)
col3.metric("🟠 Medium", medium)
col4.metric("🟢 Low", low)

st.divider()

if not results:
    st.success("✅ No vulnerabilities found!")
    st.stop()

# ── Build DataFrame ────────────────────────────────────
df = pd.DataFrame([{
    "File": os.path.basename(r["file"]),
    "Line": r["line"],
    "Severity": r["severity"],
    "Confidence": r["confidence"],
    "Issue": r["issue"],
    "Tool": r["tool"],
} for r in results])

# ── Charts ─────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Issues by Severity")
    fig1 = px.pie(
        df, names="Severity",
        color="Severity",
        color_discrete_map={"HIGH": "#e74c3c", "MEDIUM": "#f39c12", "LOW": "#2ecc71"}
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Issues by Tool")
    fig2 = px.bar(
        df.groupby("Tool").size().reset_index(name="Count"),
        x="Tool", y="Count", color="Count",
        color_continuous_scale="reds"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Detailed Table ─────────────────────────────────────
st.subheader("📋 Detailed Findings")

severity_filter = st.multiselect(
    "Filter by Severity",
    options=["HIGH", "MEDIUM", "LOW"],
    default=["HIGH", "MEDIUM", "LOW"]
)

filtered_df = df[df["Severity"].isin(severity_filter)]
st.dataframe(filtered_df, use_container_width=True)

# ── Summary ────────────────────────────────────────────
st.divider()
st.subheader("📊 Summary")
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Scanned Files", len(set([r["file"] for r in results])))
with col2:
    st.metric("Critical Issues", critical)