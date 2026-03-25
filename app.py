import streamlit as st
import pandas as pd
import re
import time

# Import demo data from our separate data file
from data import get_initial_tickets, get_initial_chat_history

# --- Page Configuration ---
st.set_page_config(
    page_title="Jira Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- State Initialization ---
def init_demo_data():
    if "theme" not in st.session_state:
        st.session_state.theme = "Dark"

    if "jira_tickets" not in st.session_state:
        st.session_state.jira_tickets = get_initial_tickets()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = get_initial_chat_history()


init_demo_data()

# --- Custom Styling (Dynamic Light/Dark) ---

SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=DM+Sans:ital,opsz,wght@0,9..40,500;0,9..40,600;0,9..40,700&display=swap');

/* ── Keyframe Animations ── */
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 0 0 var(--accent-glow); }
    50%       { box-shadow: 0 0 18px 4px var(--accent-glow); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
@keyframes spinIn {
    from { opacity: 0; transform: scale(0.85) rotate(-4deg); }
    to   { opacity: 1; transform: scale(1)    rotate(0deg); }
}
@keyframes borderFlow {
    0%   { background-position: 0% 50%;   }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%;   }
}
@keyframes metricPop {
    0%   { transform: scale(1);    }
    40%  { transform: scale(1.08); }
    100% { transform: scale(1);    }
}

/* ── Global Reset & Font ── */
* { box-sizing: border-box; }
html, body, .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: background-color 0.4s ease, color 0.4s ease;
}

/* ── Page fade-in ── */
.stApp > section {
    animation: fadeSlideIn 0.5s ease both;
}

/* ── Hide Streamlit branding ── */
#MainMenu, footer { visibility: hidden !important; }
header { background: transparent !important; }
header [data-testid="stToolbar"] { visibility: white !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important;
    padding: 0 !important;
    border-bottom: 2px solid var(--border) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.03em !important;
    text-transform: uppercase !important;
    padding: 0.75rem 1.2rem !important;
    margin-right: 0.2rem !important;
    border-radius: 12px 12px 0 0 !important;
    transition: all 0.2s ease !important;
    color: var(--text-muted) !important;
    background: transparent !important;
    border: none !important;
    position: relative !important;
    white-space: nowrap !important;
    min-width: 0 !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--accent) !important;
    background: var(--surface-hover) !important;
    border-radius: 12px 12px 0 0 !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    background: var(--tab-active-bg) !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* ── Sidebar Title ── */
[data-testid="stSidebar"] h1 {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    background: linear-gradient(135deg, var(--accent), var(--accent-2));
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin-bottom: 0.5rem !important;
}

/* ── Metric Cards ── */
[data-testid="stMetric"] {
    background: var(--card-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    animation: fadeSlideIn 0.4s ease both;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px var(--shadow) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    animation: metricPop 0.5s ease both;
}
[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.03em !important;
    background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 24px !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px var(--accent-glow) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px var(--accent-glow) !important;
    filter: brightness(1.12) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Form Submit Button ── */
[data-testid="stFormSubmitButton"] > button {
    width: 100% !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 60%, var(--accent-3) 100%) !important;
    border: none !important;
    border-radius: 32px !important;
    margin-top: 0.75rem !important;
    position: relative !important;
    overflow: hidden !important;
    transition: transform 0.22s ease, box-shadow 0.22s ease, filter 0.22s ease !important;
    box-shadow: 0 4px 18px var(--accent-glow), 0 1px 4px rgba(0,0,0,0.10) !important;
    animation: borderFlow 5s ease infinite !important;
}
/* Force white text on all child elements inside submit button */
[data-testid="stFormSubmitButton"] > button p,
[data-testid="stFormSubmitButton"] > button span,
[data-testid="stFormSubmitButton"] > button div {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
[data-testid="stFormSubmitButton"] > button::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    background: linear-gradient(120deg, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0.0) 60%) !important;
    border-radius: inherit !important;
    pointer-events: none !important;
    transition: opacity 0.22s ease !important;
    opacity: 1 !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 10px 32px var(--accent-glow), 0 2px 8px rgba(0,0,0,0.14) !important;
    filter: brightness(1.1) saturate(1.15) !important;
}
[data-testid="stFormSubmitButton"] > button:hover::before {
    opacity: 0.6 !important;
}
[data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(0px) scale(0.99) !important;
    filter: brightness(0.97) !important;
    box-shadow: 0 3px 10px var(--accent-glow) !important;
}

/* ── Text Inputs & Select Boxes ── */
div[data-baseweb="base-input"],
div[data-baseweb="select"] > div {
    background: var(--card-bg) !important;
    border: 1.5px solid var(--border) !important;
    color: var(--text-primary) !important;
    box-shadow: 0 4px 12px var(--shadow) !important;
    transition: all 0.2s ease !important;
}
div[data-baseweb="base-input"]:focus-within,
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="select"] > div:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 4px 12px var(--accent-glow) !important;
}

/* Ensure inner raw inputs don't layer an extra background */
.stTextInput input,
.stTextArea textarea {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: transparent !important;
    color: var(--text-primary) !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    padding: 0.6rem 0.9rem !important;
}



/* ── Radio Buttons ── */
[data-testid="stRadio"] label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    transition: color 0.2s !important;
}
[data-testid="stRadio"] label:has(input:checked) {
    color: var(--accent) !important;
}

/* ── Chat Input ── */
div[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 3.5rem !important;
    right: 0 !important;
    z-index: 1000 !important;
    padding: 0 2rem 1rem 2rem !important;
    background: transparent !important;
    border-top: none !important;
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
    box-shadow: none;
    transition: left 0.3s ease;
}
div[data-testid="stChatInput"] > div {
    background: var(--chat-input-bg) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 24px !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    box-shadow: 0 8px 32px var(--shadow) !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
div[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
div[data-testid="stChatInput"] div[data-baseweb="textarea"],
div[data-testid="stChatInput"] div[data-baseweb="base-input"],
div[data-testid="stChatInput"] input,
div[data-testid="stChatInput"] textarea {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    color: var(--text-primary) !important;
    caret-color: var(--accent) !important;
    box-shadow: none !important;
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
}
div[data-testid="stChatInput"] textarea::-webkit-scrollbar {
    display: none !important;
    width: 0 !important;
    background: transparent !important;
}
div[data-testid="stChatInput"] textarea,
div[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-primary) !important;
}
div[data-testid="stChatInput"] textarea:focus {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}
/* Send button inside chat input */
div[data-testid="stChatInput"] button {
    border-radius: 50% !important;
    transition: transform 0.2s ease, background 0.2s ease;
}
div[data-testid="stChatInput"] button:hover {
    transform: scale(1.1);
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    animation: fadeSlideIn 0.4s ease both !important;
}

/* ── Divider ── */
hr {
    border-color: var(--border) !important;
    margin: 1rem 0 !important;
}

/* ── Subheaders ── */
h2, h3 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
    color: var(--text-primary) !important;
}

/* ── Caption / small text ── */
.stCaption, caption, small {
    font-size: 0.78rem !important;
    color: var(--text-muted) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Success / Error / Info banners ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    animation: fadeSlideIn 0.3s ease both !important;
}

/* ── Scrollable chat history ── */
.chat-history-container {
    overflow-y: auto;
    max-height: calc(100vh - 320px);
    padding-bottom: 0.5rem;
    scroll-behavior: smooth;
}

/* ── Bottom padding so last message isn't hidden ── */
section[data-testid="stMainBlockContainer"] {
    padding-bottom: 140px !important;
}

/* ── Sidebar accent bar ── */
[data-testid="stSidebar"]::before {
    content: '';
    display: block;
    height: 3px;
    width: 100%;
    background: linear-gradient(90deg, var(--accent), var(--accent-2), var(--accent-3));
    background-size: 200% 200%;
    animation: borderFlow 4s ease infinite;
    margin-bottom: 0.5rem;
    border-radius: 0 0 4px 4px;
}

/* ── Page title shimmer ── */
.stApp h1 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    background: linear-gradient(90deg, var(--accent) 0%, var(--accent-2) 40%, var(--accent-3) 70%, var(--accent) 100%);
    background-size: 200% auto;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    animation: shimmer 4s linear infinite !important;
}


/* Text styles */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div {
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Remove chat avatar icons (yellow rectangle / bot icon) ── */
[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"],
[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"],
[data-testid="stChatMessage"] .stChatMessageAvatarAssistant,
[data-testid="stChatMessage"] .stChatMessageAvatarUser,
[data-testid="stChatMessage"] > div:first-child img,
[data-testid="stChatMessage"] > div:first-child svg {
    display: none !important;
}
[data-testid="stChatMessage"] > div:first-child {
    display: none !important;
}
</style>
"""

DARK_VARS = """
<style>
:root {
    --accent:        #6EE7B7;
    --accent-2:      #38BDF8;
    --accent-3:      #818CF8;
    --accent-glow:   rgba(110, 231, 183, 0.18);
    --text-primary:  #F1F5F9;
    --text-muted:    #64748B;
    --border:        #1E293B;
    --card-bg:       rgba(30, 41, 59, 0.8);
    --surface-hover: rgba(110, 231, 183, 0.06);
    --tab-active-bg: rgba(110, 231, 183, 0.08);
    --input-bg:      #0F172A;
    --chat-input-bg: rgba(15, 23, 42, 0.85);
    --shadow:        rgba(0, 0, 0, 0.35);
}
.stApp, .stApp > header {
    background-color: #080F1E !important;
    background-image:
        radial-gradient(ellipse at 20% 10%, rgba(56,189,248,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(110,231,183,0.05) 0%, transparent 50%);
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
    background-color: #0D1526 !important;
    border-right: 1px solid #1E293B !important;
}
h1, h2, h3, h4, h5, h6 { color: var(--text-primary) !important; }
p, span, label, .stMarkdown { color: #94A3B8 !important; }
/* Dark mode submit button — deeper glow */
[data-testid="stFormSubmitButton"] > button {
    box-shadow: 0 4px 22px rgba(110,231,183,0.28), 0 1px 4px rgba(0,0,0,0.35) !important;
    text-shadow: 0 1px 8px rgba(0,0,0,0.25) !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    box-shadow: 0 10px 40px rgba(110,231,183,0.38), 0 2px 12px rgba(0,0,0,0.4) !important;
}
/* Override global p/span/label rule for submit button children */
[data-testid="stFormSubmitButton"] > button p,
[data-testid="stFormSubmitButton"] > button span,
[data-testid="stFormSubmitButton"] > button label {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
</style>
"""

LIGHT_VARS = """
<style>
:root {
    --accent:        #0EA5E9;
    --accent-2:      #6366F1;
    --accent-3:      #10B981;
    --accent-glow:   rgba(14, 165, 233, 0.18);
    --text-primary:  #0F172A;
    --text-muted:    #64748B;
    --border:        #E2E8F0;
    --card-bg:       #FFFFFF;
    --surface-hover: rgba(14, 165, 233, 0.06);
    --tab-active-bg: rgba(14, 165, 233, 0.07);
    --input-bg:      #F8FAFC;
    --chat-input-bg: rgba(248, 250, 252, 0.92);
    --shadow:        rgba(15, 23, 42, 0.08);
}
.stApp, .stApp > header {
    background-color: #F0F6FF !important;
    background-image:
        radial-gradient(ellipse at 15% 10%, rgba(99, 102, 241, 0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 85% 85%, rgba(14, 165, 233, 0.06) 0%, transparent 50%);
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0 !important;
    box-shadow: 2px 0 12px rgba(15,23,42,0.05) !important;
}
h1, h2, h3, h4, h5, h6 { color: var(--text-primary) !important; }
p, span, label, .stMarkdown { color: #475569 !important; }
/* Ensure text colors are correct in light mode */
div[data-testid="stChatInput"] textarea,
.stTextInput input,
.stTextArea textarea {
    color: #0F172A !important;
}
div[data-testid="stChatInput"] textarea::placeholder,
.stTextInput input::placeholder {
    color: #94A3B8 !important;
    opacity: 1 !important;
}
/* Light mode submit button — crisp, vivid shadow */
[data-testid="stFormSubmitButton"] > button {
    box-shadow: 0 4px 18px rgba(14,165,233,0.30), 0 1px 4px rgba(15,23,42,0.10) !important;
    text-shadow: none !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    box-shadow: 0 10px 36px rgba(14,165,233,0.42), 0 2px 10px rgba(15,23,42,0.12) !important;
}
/* Override global p/span/label rule for submit button children */
[data-testid="stFormSubmitButton"] > button p,
[data-testid="stFormSubmitButton"] > button span,
[data-testid="stFormSubmitButton"] > button label {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
</style>
"""

SIDEBAR_JS = """
<script>
(function() {
    function adjustChatInput() {
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        const chatInput = document.querySelector('[data-testid="stChatInput"]');
        if (!chatInput) return;
        if (sidebar) {
            const rect = sidebar.getBoundingClientRect();
            const sidebarWidth = rect.width > 50 ? rect.right : 0;
            chatInput.style.left = sidebarWidth + 'px';
        } else {
            chatInput.style.left = '0px';
        }
    }
    adjustChatInput();
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) { new ResizeObserver(() => adjustChatInput()).observe(sidebar); }
    document.addEventListener('click', () => setTimeout(adjustChatInput, 350));
    let t = 0;
    const iv = setInterval(() => { adjustChatInput(); if (++t >= 10) clearInterval(iv); }, 200);
})();
</script>
"""

# --- Apply Theme CSS ---
st.markdown(SHARED_CSS, unsafe_allow_html=True)
if st.session_state.theme == "Dark":
    st.markdown(DARK_VARS, unsafe_allow_html=True)
else:
    st.markdown(LIGHT_VARS, unsafe_allow_html=True)
st.markdown(SIDEBAR_JS, unsafe_allow_html=True)


# --- Query Parser ---
def parse_query(prompt, df):
    prompt_lower = prompt.lower()

    # 1. Ticket lookup by ID
    key_match = re.search(r"([a-zA-Z]+-\d+)", prompt)
    if key_match:
        key = key_match.group(1).upper()
        res = df[df["Key"] == key]
        if not res.empty:
            return f"Here is the information for ticket **{key}**:", res
        else:
            return f"I couldn't find a ticket matching ID **{key}**.", None

    # 2. Sprint queries
    sprint_match = re.search(r"sprint\s+(\d+|[a-z0-9]+)", prompt_lower)
    if sprint_match:
        sprint_name = f"Sprint {sprint_match.group(1)}"
        if "Sprint" in df.columns:
            res = df[df["Sprint"].str.lower() == sprint_name.lower()]
            if not res.empty:
                return f"Here are the tickets for **{sprint_name}**:", res
            else:
                return f"No tickets found for **{sprint_name}**.", None
        else:
            return "Sprint data is not available.", None

    # 3. Assignee filtering
    assignees = df["Assignee"].dropna().unique()
    for assignee in assignees:
        if assignee.lower() in prompt_lower:
            res = df[df["Assignee"].str.lower() == assignee.lower()]
            return f"Here are the tickets assigned to **{assignee}**:", res

    # 4. Priority filtering
    priorities = df["Priority"].dropna().unique()
    for priority in priorities:
        if priority.lower() in prompt_lower or (
            priority.lower() == "highest" and "critical" in prompt_lower
        ):
            prio_search = priority
            if "critical" in prompt_lower:
                prio_search = "Highest"
            res = df[df["Priority"].str.lower() == prio_search.lower()]
            return f"Here are the **{prio_search}** priority tickets:", res

    # 5. Status filtering
    if (
        "in progress" in prompt_lower
        or "in-progress" in prompt_lower
        or "working on" in prompt_lower
    ):
        res = df[df["Status"] == "In Progress"]
        return "Here are the tickets currently **In Progress**:", res
    if (
        "done" in prompt_lower
        or "completed" in prompt_lower
        or "finished" in prompt_lower
    ):
        res = df[df["Status"] == "Done"]
        return "Here are the **Completed** tickets:", res
    if "to do" in prompt_lower or "todo" in prompt_lower or "open" in prompt_lower:
        res = df[df["Status"] == "To Do"]
        return "Here are the **Open** (To Do) tickets:", res

    # 6. Summary / overview
    if (
        "summary" in prompt_lower
        or "overview" in prompt_lower
        or "report" in prompt_lower
    ):
        counts = df["Status"].value_counts().to_dict()
        summary_text = "**Project Summary:**\n"
        for stat, count in counts.items():
            summary_text += f"- **{stat}**: {count}\n"
        summary_text += f"\n**Total Tickets**: {len(df)}"
        return summary_text, None

    # 7. Greeting
    if prompt_lower in ["hi", "hello", "hey", "help"]:
        return (
            "Hello! I am your Jira Assistant. You can ask me to find tickets by ID (e.g. `PROJ-101`), filter by assignee (e.g. `Alice`), check sprints (`Sprint 1`), or get a project `summary`.",
            None,
        )

    # Fallback
    res = df.copy()
    return (
        "I wasn't sure exactly what you meant, so here are all current tickets. Try asking for a specific **Assignee**, **Status**, **Sprint**, or **Ticket ID**.",
        res,
    )


# --- Sidebar UI ---
with st.sidebar:
    st.title("⚡ Jira Assistant")

    theme_choice = st.radio(
        "Theme",
        ["Light", "Dark"],
        index=1 if st.session_state.theme == "Dark" else 0,
        horizontal=True,
    )
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        st.rerun()

    st.markdown("---")
    st.subheader("📊 Live Metrics")

    df_global = st.session_state.jira_tickets

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total", len(df_global))
        st.metric("To Do", len(df_global[df_global["Status"] == "To Do"]))
    with col2:
        st.metric("In Progress", len(df_global[df_global["Status"] == "In Progress"]))
        st.metric("Done", len(df_global[df_global["Status"] == "Done"]))

    st.markdown("---")

    # Mini status breakdown bar
    total = len(df_global)
    if total > 0:
        done_pct = int(len(df_global[df_global["Status"] == "Done"]) / total * 100)
        prog_pct = int(
            len(df_global[df_global["Status"] == "In Progress"]) / total * 100
        )
        todo_pct = 100 - done_pct - prog_pct
        st.markdown(
            f"""
        <div style="margin-top:0.3rem;">
            <div style="font-size:0.7rem;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;color:var(--text-muted);margin-bottom:0.4rem;">Progress</div>
            <div style="display:flex;height:8px;border-radius:99px;overflow:hidden;gap:2px;">
                <div style="width:{done_pct}%;background:var(--accent-3);border-radius:99px;transition:width 0.6s ease;"></div>
                <div style="width:{prog_pct}%;background:var(--accent-2);border-radius:99px;transition:width 0.6s ease;"></div>
                <div style="width:{todo_pct}%;background:var(--border);border-radius:99px;transition:width 0.6s ease;"></div>
            </div>
            <div style="display:flex;gap:1rem;margin-top:0.5rem;font-size:0.7rem;">
                <span style="color:var(--accent-3);">● Done {done_pct}%</span>
                <span style="color:var(--accent-2);">● Active {prog_pct}%</span>
                <span style="color:var(--text-muted);">● Todo {todo_pct}%</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.caption("⚙️ Settings · ❓ Help · 🔒 Sign Out")


# --- Main Area (Tabs) ---
st.title("Jira Workspace")

tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "➕ Create Ticket", "💬 Chat Assistant"])

# --- TAB 1: Dashboard ---
with tab1:
    st.subheader("Ticket Dashboard")

    # Filters
    col_search, col_proj, col_stat, col_assn = st.columns([2, 1, 1, 1])

    with col_search:
        search_query = st.text_input("Search Summary or Key...", "")

    with col_proj:
        projects = ["All"] + sorted(
            list(st.session_state.jira_tickets["Project"].unique())
        )
        selected_project = st.selectbox("Project", projects)

    with col_stat:
        statuses = ["All"] + sorted(
            list(st.session_state.jira_tickets["Status"].unique())
        )
        selected_status = st.selectbox("Status", statuses)

    with col_assn:
        assignees = ["All"] + sorted(
            list(st.session_state.jira_tickets["Assignee"].unique())
        )
        selected_assignee = st.selectbox("Assignee", assignees)

    filtered_df = st.session_state.jira_tickets.copy()

    if search_query:
        mask = filtered_df["Key"].str.contains(
            search_query, case=False, na=False
        ) | filtered_df["Summary"].str.contains(search_query, case=False, na=False)
        filtered_df = filtered_df[mask]

    if selected_project != "All":
        filtered_df = filtered_df[filtered_df["Project"] == selected_project]

    if selected_status != "All":
        filtered_df = filtered_df[filtered_df["Status"] == selected_status]

    if selected_assignee != "All":
        filtered_df = filtered_df[filtered_df["Assignee"] == selected_assignee]

    # Status badge counts
    total_f = len(filtered_df)
    todo_f = len(filtered_df[filtered_df["Status"] == "To Do"]) if total_f else 0
    prog_f = len(filtered_df[filtered_df["Status"] == "In Progress"]) if total_f else 0
    done_f = len(filtered_df[filtered_df["Status"] == "Done"]) if total_f else 0

    st.markdown(
        f"""
    <div style="display:flex;align-items:center;gap:0.75rem;margin:0.5rem 0 0.75rem;">
        <span style="font-size:0.8rem;font-weight:600;color:var(--text-muted);">
            Showing <strong style="color:var(--accent)">{total_f}</strong> tickets
        </span>
        <span style="background:rgba(var(--accent-rgb,14,165,233),0.12);color:var(--accent-2);
              font-size:0.72rem;font-weight:700;padding:2px 10px;border-radius:99px;
              border:1px solid var(--border);">📋 To Do: {todo_f}</span>
        <span style="background:rgba(14,165,233,0.10);color:var(--accent-2);
              font-size:0.72rem;font-weight:700;padding:2px 10px;border-radius:99px;
              border:1px solid var(--border);">🔄 Active: {prog_f}</span>
        <span style="background:rgba(16,185,129,0.10);color:var(--accent-3);
              font-size:0.72rem;font-weight:700;padding:2px 10px;border-radius:99px;
              border:1px solid var(--border);">✅ Done: {done_f}</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.dataframe(filtered_df, hide_index=True)


# --- TAB 2: Create Ticket ---
with tab2:
    st.subheader("Create a New Ticket")

    with st.form("create_ticket_form", clear_on_submit=True):
        col_form1, col_form2 = st.columns(2)

        with col_form1:
            new_summary = st.text_input(
                "Summary*", help="Brief description of the issue"
            )
            new_project = st.selectbox("Project*", ["Alpha", "Beta", "Gamma", "Delta"])
            new_sprint = st.selectbox(
                "Sprint", ["Backlog", "Sprint 1", "Sprint 2", "Sprint 3"]
            )

        with col_form2:
            new_priority = st.selectbox(
                "Priority", ["Highest", "High", "Medium", "Low"]
            )
            new_assignee = st.selectbox(
                "Assignee", ["Unassigned", "Alice", "Bob", "Charlie", "Dave"]
            )
            new_status = st.selectbox(
                "Status", ["To Do", "In Progress", "Review", "Done"]
            )

        submitted = st.form_submit_button("Create Ticket")

        if submitted:
            if not new_summary.strip():
                st.error("Summary is required!")
            else:
                prefix = new_project[:3].upper()
                proj_tickets = st.session_state.jira_tickets[
                    st.session_state.jira_tickets["Project"] == new_project
                ]
                new_num = len(proj_tickets) + 101
                new_key = f"{prefix}-{new_num}"

                new_ticket = {
                    "Key": new_key,
                    "Summary": new_summary,
                    "Status": new_status,
                    "Priority": new_priority,
                    "Assignee": new_assignee,
                    "Project": new_project,
                    "Sprint": new_sprint,
                }

                st.session_state.jira_tickets = pd.concat(
                    [st.session_state.jira_tickets, pd.DataFrame([new_ticket])],
                    ignore_index=True,
                )

                st.success(f"Ticket {new_key} created successfully!")


# --- TAB 3: Chat Assistant ---
with tab3:
    st.caption(
        "💬 Ask questions about your tickets — by ID, assignee, sprint, status, or get a summary."
    )

    # Render all chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "data" in message:
                st.dataframe(message["data"], hide_index=True)

    # Chat input — pinned at bottom via SHARED_CSS + SIDEBAR_JS
    if prompt := st.chat_input(
        "Ask about your Jira tickets (e.g. 'Show open tickets for Alice')"
    ):
        # Visually render the user's prompt immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Searching..."):
                time.sleep(0.4)
                ans_text, ans_data = parse_query(prompt, st.session_state.jira_tickets)

            # Immediately show assistant's response
            st.markdown(ans_text)
            if ans_data is not None and not ans_data.empty:
                st.dataframe(ans_data, hide_index=True)
            elif ans_data is not None and ans_data.empty:
                st.info("No tickets found matching that criteria.")

        msg = {"role": "assistant", "content": ans_text}
        if ans_data is not None and not ans_data.empty:
            msg["data"] = ans_data
        st.session_state.chat_history.append(msg)