import streamlit as st
import time
from agents.agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #080d18;
    --surface: #101827;
    --surface-hover: #162235;
    --border: rgba(148, 163, 184, 0.13);
    --text: #f1f5f9;
    --muted: #94a3b8;
    --cyan: #67e8f9;
    --purple: #a78bfa;
    --green: #4ade80;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 0%, #14253d 0%, transparent 40%),
        radial-gradient(ellipse at 90% 100%, #1c1537 0%, transparent 35%),
        var(--bg);
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    max-width: 1180px;
    padding: 2rem 2.5rem 4rem;
}

/* Hero */

.hero {
    text-align: center;
    padding: 3rem 0 2rem;
}

.hero-eyebrow {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--cyan);
    background: rgba(103, 232, 249, 0.07);
    border: 1px solid rgba(103, 232, 249, 0.18);
    border-radius: 999px;
    padding: 0.45rem 0.9rem;
    margin-bottom: 1.5rem;
}

.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.8rem, 6vw, 4.8rem);
    font-weight: 700;
    letter-spacing: -0.055em;
    line-height: 1.05;
    color: var(--text);
    margin: 0 0 1rem;
}

.hero h1 span {
    background: linear-gradient(120deg, var(--cyan), var(--purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    max-width: 540px;
    margin: 0 auto;
    color: var(--muted);
    font-size: 1rem;
    line-height: 1.8;
}

/* Divider */

.divider {
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(103, 232, 249, 0.2),
        transparent
    );
    margin: 2rem 0;
}

/* Research input */

.input-card {
    background: linear-gradient(
        145deg,
        rgba(22, 34, 53, 0.95),
        rgba(13, 21, 35, 0.95)
    );
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.stTextInput > div > div > input {
    background: #0a1220 !important;
    border: 1px solid #27364b !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-size: 0.95rem !important;
    padding: 0.85rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}

.stTextInput > div > div > input:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 3px rgba(103, 232, 249, 0.1) !important;
}

.stTextInput > label {
    color: #cbd5e1 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    margin-bottom: 0.5rem !important;
}

/* Buttons */

.stButton > button {
    background: linear-gradient(120deg, #0891b2, #7c3aed) !important;
    color: white !important;
    border: 0 !important;
    border-radius: 12px !important;
    padding: 0.8rem 1.2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    box-shadow: 0 8px 24px rgba(8, 145, 178, 0.15) !important;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(8, 145, 178, 0.25) !important;
}

/* Pipeline */

.section-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    color: var(--text);
    margin: 1rem 0 1.2rem;
}

.step-card {
    background: rgba(16, 24, 39, 0.75);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.8rem;
    transition: all 0.2s ease;
}

.step-card:hover {
    background: var(--surface-hover);
    border-color: rgba(103, 232, 249, 0.25);
    transform: translateY(-1px);
}

.step-card.active {
    border-color: rgba(103, 232, 249, 0.5);
    background: rgba(8, 145, 178, 0.08);
    box-shadow: 0 0 24px rgba(8, 145, 178, 0.06);
}

.step-card.done {
    border-color: rgba(74, 222, 128, 0.25);
    background: rgba(34, 197, 94, 0.045);
}

.step-card::before {
    content: '';
    display: none;
}

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.step-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--cyan);
    background: rgba(103, 232, 249, 0.08);
    border-radius: 7px;
    padding: 0.35rem 0.5rem;
}

.step-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text);
}

.step-status {
    margin-left: auto;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.08em;
}

.status-waiting {
    color: #64748b;
}

.status-running {
    color: var(--cyan);
}

.status-done {
    color: var(--green);
}

/* Results */

.result-panel,
.report-panel,
.feedback-panel {
    background: rgba(16, 24, 39, 0.8);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 1.6rem;
    margin: 1rem 0 1.5rem;
}

.report-panel {
    border-color: rgba(103, 232, 249, 0.2);
    background: linear-gradient(
        145deg,
        rgba(16, 24, 39, 0.95),
        rgba(12, 20, 34, 0.95)
    );
}

.feedback-panel {
    border-color: rgba(74, 222, 128, 0.2);
}

.result-panel-title,
.panel-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding-bottom: 0.8rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}

.result-panel-title,
.panel-label.orange {
    color: var(--cyan);
}

.panel-label.green {
    color: var(--green);
}

.result-content {
    font-size: 0.9rem;
    line-height: 1.85;
    color: #cbd5e1;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

/* Expander */

details {
    background: rgba(16, 24, 39, 0.65);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.5rem 0.9rem;
}

details summary {
    color: #cbd5e1 !important;
    font-size: 0.8rem !important;
    font-weight: 600;
    cursor: pointer;
}

/* Download button */

.stDownloadButton > button {
    background: rgba(103, 232, 249, 0.08) !important;
    border: 1px solid rgba(103, 232, 249, 0.25) !important;
    color: var(--cyan) !important;
    border-radius: 10px !important;
}

/* Status and footer */

.stSpinner > div {
    border-top-color: var(--cyan) !important;
}

.notice {
    color: #64748b;
    text-align: center;
    font-size: 0.75rem;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
}

/* Responsive */

@media (max-width: 768px) {
    .block-container {
        padding: 1rem 1rem 3rem;
    }

    .hero {
        padding: 2rem 0 1rem;
    }

    .hero h1 {
        font-size: 2.8rem;
    }

    .input-card,
    .report-panel,
    .feedback-panel {
        padding: 1.2rem;
    }

    .step-card {
        padding: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
def step_card(num: str, title: str, state: str, desc: str = ""):
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }

    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")

    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {"<div style='font-size:0.82rem;color:#94a3b8;margin-top:0.3rem;'>"+desc+"</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>Researcher<span>Agent</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>

<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────

col_input, col_spacer, col_pipeline = st.columns([1.1, 0.08, 1])

with col_input:
    st.markdown(
        '<div class="section-heading">Start your research</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="color:#94a3b8; font-size:0.9rem; '
        'margin-bottom:1.2rem;">'
        'Enter a topic and let your AI agents investigate, '
        'analyze, and prepare a research report.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. The future of AI agents",
        key="topic_input",
    )

    run_btn = st.button(
        "⚡  Start Research",
        use_container_width=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size:0.75rem; color:#64748b; '
        'margin-bottom:0.7rem;">TRY A TOPIC</div>',
        unsafe_allow_html=True,
    )

    examples = [
        "Future of LLMs",
        "AI agents in 2026",
        "AGI development",
    ]

    st.markdown(
        '<div style="display:flex; gap:0.5rem; flex-wrap:wrap;">'
        + "".join(
            f'<span style="background:rgba(148,163,184,0.06); '
            f'border:1px solid rgba(148,163,184,0.12); '
            f'border-radius:8px; padding:0.4rem 0.7rem; '
            f'font-size:0.75rem; color:#cbd5e1;">{ex}</span>'
            for ex in examples
        )
        + "</div>",
        unsafe_allow_html=True,
    )

with col_pipeline:
    st.markdown(
        '<div class="section-heading">Research pipeline</div>',
        unsafe_allow_html=True,
    )

    # Keep your existing pipeline status logic and step_card()
    # calls here.

    r = st.session_state.results
    done = st.session_state.done

    def s(step):

        if not r:
            return "waiting"

        steps = ["search", "reader", "writer", "critic"]

        if step in r:
            return "done"

        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"

        return "waiting"

    step_card(
        "01",
        "Search Agent",
        s("search"),
        "Gathers recent web information"
    )

    step_card(
        "02",
        "Reader Agent",
        s("reader"),
        "Scrapes & extracts deep content"
    )

    step_card(
        "03",
        "Writer Chain",
        s("writer"),
        "Drafts the full research report"
    )

    step_card(
        "04",
        "Critic Chain",
        s("critic"),
        "Reviews & scores the report"
    )


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:

    if not topic.strip():
        st.warning("Please enter a research topic first.")

    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()


if st.session_state.running and not st.session_state.done:

    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("🔍 Search Agent is working…"):

        search_agent = build_search_agent()

        sr = search_agent.invoke({
            "messages": [
                ("user",
                 f"Find recent, reliable and detailed information about: {topic_val}")
            ]
        })

        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 2: Reader ──
    with st.spinner("📄 Reader Agent is scraping top resources…"):

        reader_agent = build_reader_agent()

        rr = reader_agent.invoke({
            "messages": [(
                "user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })

        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("✍️ Writer is drafting the report…"):

        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )

        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })

        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("🧐 Critic is reviewing the report…"):

        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })

        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True

    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">Results</div>',
        unsafe_allow_html=True
    )

    # Raw outputs
    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):

            st.markdown(
                f'''
                <div class="result-panel">
                    <div class="result-panel-title">
                        Search Agent Output
                    </div>

                    <div class="result-content">
                        {r["search"]}
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):

            st.markdown(
                f'''
                <div class="result-panel">
                    <div class="result-panel-title">
                        Reader Agent Output
                    </div>

                    <div class="result-content">
                        {r["reader"]}
                    </div>
                </div>
                ''',
                unsafe_allow_html=True
            )

    # Final report
    if "writer" in r:

        st.markdown("""
        <div class="report-panel">
            <div class="panel-label orange">
                📝 Final Research Report
            </div>
        """, unsafe_allow_html=True)

        st.markdown(r["writer"])

        st.markdown("</div>", unsafe_allow_html=True)

        # Download button
        st.download_button(
            label="⬇ Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic feedback
    if "critic" in r:

        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label green">
                🧐 Critic Feedback
            </div>
        """, unsafe_allow_html=True)

        st.markdown(r["critic"])

        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchAgent · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)