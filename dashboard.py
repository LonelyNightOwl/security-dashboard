import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from scanner import run_scan, load_latest_report

st.set_page_config(page_title="Security Dashboard", layout="wide")

st.title("🔐 Security Analysis & Vulnerability Dashboard")

# Sidebar
st.sidebar.header("Controls")
if st.sidebar.button("🔍 Run New Scan"):
    with st.spinner("Scanning..."):
        run_scan()
    st.success("Scan complete!")

# Load report
data = load_latest_report()

if not data:
    st.warning("No scan reports found. Run a scan first.")
    st.stop()

results = data.get("results", [])
metrics = data.get("metrics", {})

# ── Top KPI Cards ──────────────────────────────────────────
total = len(results)
critical = sum(1 for r in results if r["issue_severity"] == "HIGH")
medium   = sum(1 for r in results if r["issue_severity"] == "MEDIUM")
low      = sum(1 for r in results if r["issue_severity"] == "LOW")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Issues",    total)
col2.metric("🔴 High",         critical)
col3.metric("🟠 Medium",       medium)
col4.metric("🟢 Low",          low)

st.divider()

if not results:
    st.success("✅ No vulnerabilities found!")
    st.stop()

# ── Build DataFrame ────────────────────────────────────────
df = pd.DataFrame([{
    "File":        os.path.basename(r["filename"]),
    "Line":        r["line_number"],
    "Severity":    r["issue_severity"],
    "Confidence":  r["issue_confidence"],
    "Issue":       r["issue_text"],
    "Test ID":     r["test_id"],
} for r in results])

# ── Charts ─────────────────────────────────────────────────
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
    st.subheader("Issues by Type")
    fig2 = px.bar(
        df.groupby("Test ID").size().reset_index(name="Count"),
        x="Test ID", y="Count", color="Count",
        color_continuous_scale="reds"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ── Detailed Table ─────────────────────────────────────────
st.subheader("📋 Detailed Findings")

severity_filter = st.multiselect(
    "Filter by Severity",
    options=["HIGH", "MEDIUM", "LOW"],
    default=["HIGH", "MEDIUM", "LOW"]
)

filtered_df = df[df["Severity"].isin(severity_filter)]
st.dataframe(filtered_df, use_container_width=True)

# ── Raw Log Viewer ─────────────────────────────────────────
st.divider()
st.subheader("🗂️ Raw Findings")
for r in results:
    severity = r["issue_severity"]
    color = "🔴" if severity == "HIGH" else "🟠" if severity == "MEDIUM" else "🟢"
    with st.expander(f"{color} {r['issue_text']} — Line {r['line_number']}"):
        st.code(r.get("code", "N/A"), language="python")
        st.caption(f"File: {r['filename']} | Test: {r['test_id']} | Confidence: {r['issue_confidence']}")