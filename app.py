import streamlit as st
import time
from pipeline import run_research_pipeline

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchBot",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* Global Reset */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: #0a0a0f;
    color: #e8e4d9;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* App background */
.stApp {
    background: #0a0a0f;
}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
}
.hero-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.3em;
    color: #5a9e6f;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    color: #e8e4d9;
    line-height: 1.1;
    margin: 0;
}
.hero-title span {
    color: #5a9e6f;
}
.hero-sub {
    font-size: 0.85rem;
    color: #6b6b7a;
    margin-top: 0.8rem;
    letter-spacing: 0.05em;
}

/* ── Input Area ── */
.stTextInput > div > div > input {
    background: #13131a !important;
    border: 1px solid #2a2a3a !important;
    border-radius: 4px !important;
    color: #e8e4d9 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s ease;
}
.stTextInput > div > div > input:focus {
    border-color: #5a9e6f !important;
    box-shadow: 0 0 0 2px rgba(90,158,111,0.15) !important;
}
.stTextInput > div > div > input::placeholder {
    color: #3a3a4a !important;
}

/* ── Button ── */
.stButton > button {
    background: #5a9e6f !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: #6fc484 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(90,158,111,0.3) !important;
}
.stButton > button:active {
    transform: translateY(0);
}

/* ── Pipeline Step Cards ── */
.step-card {
    background: #13131a;
    border: 1px solid #2a2a3a;
    border-left: 3px solid #5a9e6f;
    border-radius: 4px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
}
.step-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.6rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #5a9e6f;
    letter-spacing: 0.2em;
    background: rgba(90,158,111,0.1);
    padding: 2px 8px;
    border-radius: 2px;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    color: #e8e4d9;
}
.step-content {
    font-size: 0.82rem;
    color: #9a9aaa;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 220px;
    overflow-y: auto;
}
.step-content::-webkit-scrollbar { width: 4px; }
.step-content::-webkit-scrollbar-track { background: #1a1a25; }
.step-content::-webkit-scrollbar-thumb { background: #3a3a4a; border-radius: 2px; }

/* ── Report Card ── */
.report-card {
    background: #13131a;
    border: 1px solid #5a9e6f;
    border-radius: 4px;
    padding: 2rem;
    margin-top: 1rem;
}
.report-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.3rem;
    color: #5a9e6f;
    margin-bottom: 1.2rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.report-body {
    font-size: 0.88rem;
    color: #c8c4b9;
    line-height: 1.85;
    white-space: pre-wrap;
}

/* ── Critic Card ── */
.critic-card {
    background: #13131a;
    border: 1px solid #9e6f5a;
    border-radius: 4px;
    padding: 1.5rem;
    margin-top: 1rem;
}
.critic-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: #9e6f5a;
    margin-bottom: 0.8rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.critic-body {
    font-size: 0.83rem;
    color: #9a9aaa;
    line-height: 1.75;
    white-space: pre-wrap;
}

/* ── Divider ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #3a3a5a;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin: 2rem 0 1rem;
}

/* ── Status bar ── */
.status-bar {
    background: #13131a;
    border: 1px solid #2a2a3a;
    border-radius: 4px;
    padding: 0.8rem 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #5a9e6f;
    display: inline-block;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
.status-text {
    font-size: 0.8rem;
    color: #5a9e6f;
    letter-spacing: 0.05em;
}

/* ── Error ── */
.error-card {
    background: #1a1013;
    border: 1px solid #9e3a3a;
    border-radius: 4px;
    padding: 1.2rem 1.5rem;
    margin-top: 1rem;
}
.error-text {
    font-size: 0.83rem;
    color: #c07070;
}

/* Progress bar override */
.stProgress > div > div > div > div {
    background: #5a9e6f !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-label">AI Research Pipeline</div>
    <div class="hero-title">Research<span>Bot</span></div>
    <div class="hero-sub">Search → Scrape → Write → Critique</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─── Input ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    topic = st.text_input(
        "",
        placeholder="e.g.  LangGraph multi-agent systems, RAG vs fine-tuning, AlphaFold 3...",
        label_visibility="collapsed"
    )
with col2:
    run_btn = st.button("▶  RUN", use_container_width=True)

# ─── Pipeline Execution ────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        # Status bar
        status_placeholder = st.empty()
        status_placeholder.markdown("""
        <div class="status-bar">
            <span class="status-dot"></span>
            <span class="status-text">Pipeline running — this may take 30–60 seconds...</span>
        </div>
        """, unsafe_allow_html=True)

        progress = st.progress(0)
        result_placeholder = st.empty()

        try:
            # ── Step tracking via live updates ──
            steps_display = st.container()

            with st.spinner(""):
                progress.progress(10)
                state = run_research_pipeline(topic)
                progress.progress(100)

            status_placeholder.markdown("""
            <div class="status-bar" style="border-color:#2a3a2a;">
                <span class="status-dot" style="background:#5a9e6f;animation:none;"></span>
                <span class="status-text">Pipeline complete ✓</span>
            </div>
            """, unsafe_allow_html=True)

            # ── Pipeline Steps ──
            st.markdown('<div class="section-label">// Pipeline Steps</div>', unsafe_allow_html=True)

            # Step 1 - Search
            search_preview = str(state.get("search_result", ""))[:600] + ("..." if len(str(state.get("search_result", ""))) > 600 else "")
            st.markdown(f"""
            <div class="step-card">
                <div class="step-header">
                    <span class="step-num">STEP 01</span>
                    <span class="step-title">Search Agent</span>
                </div>
                <div class="step-content">{search_preview}</div>
            </div>
            """, unsafe_allow_html=True)

            # Step 2 - Scrape
            scrape_preview = str(state.get("scraped_content", ""))[:600] + ("..." if len(str(state.get("scraped_content", ""))) > 600 else "")
            st.markdown(f"""
            <div class="step-card">
                <div class="step-header">
                    <span class="step-num">STEP 02</span>
                    <span class="step-title">Reader / Scraper Agent</span>
                </div>
                <div class="step-content">{scrape_preview}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Final Report ──
            st.markdown('<div class="section-label">// Generated Report</div>', unsafe_allow_html=True)
            report_text = str(state.get("report", "No report generated."))
            st.markdown(f"""
            <div class="report-card">
                <div class="report-title">📄 Research Report — {topic[:60]}</div>
                <div class="report-body">{report_text}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Critic Feedback ──
            st.markdown('<div class="section-label">// Critic Feedback</div>', unsafe_allow_html=True)
            feedback_text = str(state.get("feedback", "No feedback generated."))
            st.markdown(f"""
            <div class="critic-card">
                <div class="critic-title">🔍 Critic Review</div>
                <div class="critic-body">{feedback_text}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Download Button ──
            st.markdown("<br>", unsafe_allow_html=True)
            download_content = f"""RESEARCHBOT — REPORT
Topic: {topic}
{'='*60}

SEARCH RESULT:
{state.get('search_result', '')}

SCRAPED CONTENT:
{state.get('scraped_content', '')}

FINAL REPORT:
{state.get('report', '')}

CRITIC FEEDBACK:
{state.get('feedback', '')}
"""
            st.download_button(
                label="⬇  Download Full Report (.txt)",
                data=download_content,
                file_name=f"report_{topic[:30].replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        except Exception as e:
            progress.progress(0)
            status_placeholder.empty()
            st.markdown(f"""
            <div class="error-card">
                <div class="critic-title" style="color:#c07070;">⚠ Pipeline Error</div>
                <div class="error-text">{str(e)}</div>
            </div>
            """, unsafe_allow_html=True)
            st.info("Make sure your `.env` is configured and all agent dependencies are installed.")

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; font-size:0.7rem; color:#2a2a3a; letter-spacing:0.2em; text-transform:uppercase;">
    ResearchBot · Search → Scrape → Write → Critique
</div>
""", unsafe_allow_html=True)