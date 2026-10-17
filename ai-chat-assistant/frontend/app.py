
import os
import requests
import streamlit as st

API_URL = os.getenv(
    "CHAT_API_URL",
    "http://127.0.0.1:8000"
).rstrip("/") + "/chat"

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Nova AI | Intelligent Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
    /* Global */
    :root {
        --bg: #0b0f19;
        --panel: #111827;
        --border: rgba(148, 163, 184, 0.15);
        --text: #e5e7eb;
        --muted: #94a3b8;
        --accent: #8b5cf6;
        --accent2: #06b6d4;
    }

    .stApp {
        background:
            radial-gradient(
                ellipse at 50% 0%,
                rgba(91, 33, 182, 0.13),
                transparent 42%
            ),
            var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1080px;
        padding: 1.5rem 2rem 2rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0e1421;
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 4px 24px;
    }

    .brand-icon {
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
        font-size: 23px;
        background: linear-gradient(135deg, #7c3aed, #0891b2);
        box-shadow: 0 5px 24px rgba(124, 58, 237, 0.25);
    }

    .brand-name {
        color: #f8fafc;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -0.6px;
    }

    .brand-caption {
        color: #94a3b8;
        font-size: 11px;
        margin-top: 3px;
    }

    .sidebar-label {
        color: #64748b;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        margin: 18px 0 10px;
    }

    .model-card {
        padding: 14px;
        border: 1px solid var(--border);
        background: rgba(30, 41, 59, 0.55);
        border-radius: 14px;
        margin: 10px 0 20px;
    }

    .model-title {
        color: #f1f5f9;
        font-size: 13px;
        font-weight: 700;
    }

    .model-subtitle {
        color: #94a3b8;
        font-size: 11px;
        margin-top: 6px;
    }

    .online-dot {
        color: #34d399;
        font-size: 12px;
    }

    /* Header */
    .hero {
        text-align: center;
        padding: 30px 0 25px;
    }

    .hero-pill {
        display: inline-block;
        padding: 7px 13px;
        border-radius: 30px;
        border: 1px solid rgba(139, 92, 246, 0.35);
        background: rgba(139, 92, 246, 0.09);
        color: #c4b5fd;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.7px;
        margin-bottom: 18px;
    }

    .hero h1 {
        font-size: clamp(32px, 5vw, 48px);
        line-height: 1.15;
        font-weight: 850;
        letter-spacing: -2px;
        color: #f8fafc;
        margin: 0 0 13px;
    }

    .gradient-text {
        background: linear-gradient(90deg, #a78bfa, #67e8f9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        color: #94a3b8;
        font-size: 14px;
        line-height: 1.8;
        max-width: 520px;
        margin: auto;
    }

    /* Suggestion cards */
    .section-label {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 700;
        margin: 14px 0 12px;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 12px;
    }

    .stButton > button {
        min-height: 44px;
        border: 1px solid var(--border);
        border-radius: 12px;
        background: rgba(30, 41, 59, 0.5);
        color: #e2e8f0;
        font-size: 12px;
        font-weight: 600;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: rgba(139, 92, 246, 0.75);
        background: rgba(124, 58, 237, 0.12);
        color: #ddd6fe;
        transform: translateY(-1px);
    }

    /* Chat messages */
    div[data-testid="stChatMessage"] {
        background: rgba(17, 24, 39, 0.65);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 15px;
    }

    div[data-testid="stChatMessage"] p {
        color: #e2e8f0;
        font-size: 14px;
        line-height: 1.8;
    }

    div[data-testid="stChatMessage"] pre {
        border: 1px solid var(--border);
        border-radius: 12px;
    }

    /* Chat input */
    div[data-testid="stChatInput"] {
        border: 1px solid rgba(139, 92, 246, 0.4);
        border-radius: 18px;
        background: #111827;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.18);
    }

    div[data-testid="stChatInput"]:focus-within {
        border-color: #8b5cf6;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.12);
    }

    div[data-testid="stChatInput"] textarea {
        color: #f8fafc;
    }

    /* General text */
    h1, h2, h3 {
        color: #f8fafc;
    }

    p, label, li {
        color: #cbd5e1;
    }

    hr {
        border-color: var(--border);
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: 11px;
        padding: 20px 0 5px;
    }

    /* Mobile */
    @media (max-width: 640px) {
        .block-container {
            padding: 1rem 0.8rem 1.5rem;
        }

        .hero {
            padding: 22px 0 18px;
        }

        .hero h1 {
            letter-spacing: -1px;
        }

        div[data-testid="stChatMessage"] {
            padding: 12px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">✦</div>
            <div>
                <div class="brand-name">NOVA AI</div>
                <div class="brand-caption">YOUR INTELLIGENT ASSISTANT</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("＋  New conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.markdown(
        '<div class="sidebar-label">MODEL CONFIGURATION</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="model-card">
            <div class="model-title">🧠 &nbsp; Llama 3.1</div>
            <div class="model-subtitle">Ollama · Local inference</div>
            <div class="model-subtitle">
                <span class="online-dot">●</span>
                &nbsp; Configured local model
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-label">CAPABILITIES</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        💬 &nbsp; Conversational AI

        🧩 &nbsp; Coding assistance

        📝 &nbsp; Markdown responses

        🔗 &nbsp; FastAPI integration

        🔒 &nbsp; Local model inference
        """,
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-label">CONVERSATION</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        f"Messages in this session: {len(st.session_state.messages)}"
    )

    if st.button("🗑️  Clear chat history", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.divider()

    st.caption("Powered by")
    st.markdown("**FastAPI** · LangChain · Ollama")

# =========================================================
# HERO HEADER
# =========================================================

if not st.session_state.messages:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-pill">✦ &nbsp; YOUR PERSONAL AI WORKSPACE</div>
            <h1>Think better.<br>
                <span class="gradient-text">Build smarter.</span>
            </h1>
            <p>
                Meet Nova, your AI companion for coding, learning,
                problem-solving and creative thinking.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div style="padding: 10px 0 22px;">
            <span style="font-size: 22px; font-weight: 800; color: #f8fafc;">
                ✦ Nova AI
            </span>
            <span style="color: #64748b; font-size: 12px;">
                &nbsp; / &nbsp; Chat workspace
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# SUGGESTED PROMPTS
# =========================================================

if not st.session_state.messages:
    st.markdown(
        '<div class="section-label">GET STARTED WITH A SUGGESTION</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "💻  Explain Python decorators",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = (
                "Explain Python decorators with a simple example."
            )
            st.rerun()

        if st.button(
            "🧠  What is Agentic AI?",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = (
                "Explain Agentic AI and how it differs from a normal LLM chatbot."
            )
            st.rerun()

    with col2:
        if st.button(
            "⚡  Explain async and await",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = (
                "Explain async and await in Python with examples."
            )
            st.rerun()

        if st.button(
            "🚀  Design a REST API",
            use_container_width=True,
        ):
            st.session_state.pending_prompt = (
                "Show me how to design a clean REST API using FastAPI."
            )
            st.rerun()

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for item in st.session_state.messages:
    avatar = "👤" if item["role"] == "user" else "🤖"

    with st.chat_message(item["role"], avatar=avatar):
        st.markdown(item["content"])

# =========================================================
# HANDLE USER INPUT
# =========================================================

typed_prompt = st.chat_input(
    "Message Nova... ask anything"
)

prompt = typed_prompt or st.session_state.pending_prompt

if prompt:
    st.session_state.pending_prompt = None

    # Show the latest user message.
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Preserve existing conversation context.
    history = list(st.session_state.messages)

    payload = {
        "message": prompt,
        "history": history,
    }

    with st.chat_message("assistant", avatar="🤖"):
        try:
            with st.spinner("Nova is thinking..."):
                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=180,
                )

                response.raise_for_status()

                data = response.json()
                answer = data["answer"]

            st.markdown(answer)

            st.session_state.messages.extend(
                [
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": answer},
                ]
            )

        except requests.exceptions.Timeout:
            st.error(
                "⏱️ The model took too long to respond. "
                "Try again or check your Ollama model."
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "🔌 Cannot connect to FastAPI. "
                "Start the backend on port 8000 and retry."
            )

        except requests.exceptions.HTTPError:
            try:
                detail = response.json().get(
                    "detail", "Unknown API error"
                )
            except (ValueError, AttributeError):
                detail = "The backend returned an invalid error response."

            st.error(f"API error: {detail}")

        except (ValueError, KeyError):
            st.error("The backend returned an unexpected response.")

        except requests.exceptions.RequestException as exc:
            st.error(f"Request failed: {exc}")

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        NOVA AI &nbsp; · &nbsp; LOCAL AI, BUILT FOR YOU
    </div>
    """,
    unsafe_allow_html=True,
)
