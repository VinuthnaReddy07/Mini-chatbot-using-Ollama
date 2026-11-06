
import json
import uuid
import requests
import streamlit as st

# =========================================================
# CONFIGURATION
# =========================================================

OLLAMA_URL = "http://localhost:11434"
CHAT_API = f"{OLLAMA_URL}/api/chat"
TAGS_API = f"{OLLAMA_URL}/api/tags"

DEFAULT_MODEL = "qwen2.5:1.5b"

DEFAULT_SYSTEM_PROMPT = """
You are MiniGPT, a helpful AI assistant.

Instructions:
- Give accurate and clear answers.
- Explain complex concepts in simple language.
- Use practical examples.
- Structure long answers with headings and bullet points.
- If you do not know something, say so honestly.
"""

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MiniGPT | AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# ANIMATED PREMIUM CSS
# =========================================================

st.markdown("""
<style>

/* GLOBAL */

.stApp {
    background:
        radial-gradient(ellipse at 10% 10%, #18234b 0%, transparent 40%),
        radial-gradient(ellipse at 90% 85%, #281747 0%, transparent 40%),
        #090d16;
    color: #e6edf7;
    font-family: Inter, sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #101521;
    border-right: 1px solid #263149;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 25px 18px;
}

[data-testid="stSidebar"] h3 {
    font-size: 13px;
    color: #9ba9c0;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* BRAND */

.brand-icon {
    font-size: 38px;
    display: inline-block;
    animation: logoPulse 2.5s infinite ease-in-out;
}

.brand-name {
    font-size: 27px;
    font-weight: 800;
    letter-spacing: -1px;
    color: white;
}

.brand-description {
    color: #8996aa;
    font-size: 12px;
}

/* LOGO ANIMATION */

@keyframes logoPulse {
    0%, 100% {
        transform: scale(1);
        filter: drop-shadow(0 0 5px #818cf8);
    }
    50% {
        transform: scale(1.12);
        filter: drop-shadow(0 0 20px #818cf8);
    }
}

/* GRADIENT TEXT */

@keyframes gradientMove {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}

.main-heading {
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: white;
}

.welcome-title {
    font-size: 37px;
    font-weight: 800;
    background: linear-gradient(
        90deg,
        #ffffff,
        #a5b4fc,
        #c084fc,
        #60a5fa,
        #ffffff
    );
    background-size: 200% auto;
    color: transparent;
    background-clip: text;
    -webkit-background-clip: text;
    animation: gradientMove 5s linear infinite;
}

.main-subheading {
    color: #8b98ac;
    font-size: 14px;
    margin-top: -8px;
}

/* WELCOME ANIMATION */

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.welcome-container {
    text-align: center;
    padding-top: 65px;
    padding-bottom: 35px;
    animation: fadeUp 0.9s ease-out both;
}

.welcome-icon {
    font-size: 55px;
    display: inline-block;
    animation: logoPulse 2.5s infinite ease-in-out;
}

.welcome-description {
    color: #9ba8bc;
    font-size: 15px;
    margin-top: 12px;
}

/* BUTTONS */

.stButton > button {
    background: rgba(25, 34, 52, 0.85);
    color: #e6edf7;
    border: 1px solid #35435c;
    border-radius: 13px;
    min-height: 48px;
    font-weight: 600;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background: #252e4b;
    border-color: #818cf8;
    color: white;
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.25);
}

/* CHAT MESSAGES */

@keyframes messageAppear {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

[data-testid="stChatMessage"] {
    background: rgba(21, 29, 43, 0.92);
    border: 1px solid #29364b;
    border-radius: 17px;
    padding: 18px;
    margin-bottom: 15px;
    animation: messageAppear 0.45s ease-out both;
    transition: border-color 0.3s, box-shadow 0.3s;
}

[data-testid="stChatMessage"]:hover {
    border-color: #6675d9;
    box-shadow: 0 5px 25px rgba(99, 102, 241, 0.12);
}

/* CHAT INPUT */

[data-testid="stChatInput"] {
    background: #151c29;
    border: 1px solid #394660;
    border-radius: 17px;
    transition: all 0.3s ease;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #818cf8;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.22);
}

/* INPUTS */

.stTextArea textarea,
.stTextInput input {
    background: #151c29;
    color: white;
    border-radius: 10px;
}

/* TYPING INDICATOR */

.typing-indicator {
    display: flex;
    gap: 7px;
    padding: 16px;
}

.typing-indicator span {
    height: 9px;
    width: 9px;
    background: #a5b4fc;
    border-radius: 50%;
    animation: typing 1s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
    animation-delay: 0.15s;
}

.typing-indicator span:nth-child(3) {
    animation-delay: 0.3s;
}

@keyframes typing {
    0%, 60%, 100% {
        transform: translateY(0);
        opacity: 0.4;
    }
    30% {
        transform: translateY(-9px);
        opacity: 1;
    }
}

/* STATUS */

.status-card {
    background: #171f2e;
    border: 1px solid #344158;
    border-radius: 12px;
    padding: 14px;
    font-size: 13px;
    color: #cbd5e1;
}

.online {
    color: #4ade80;
    font-weight: 700;
}

.offline {
    color: #fb7185;
    font-weight: 700;
}

/* SIDEBAR ANIMATION */

@keyframes sidebarAppear {
    from {
        opacity: 0;
        transform: translateX(-15px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

[data-testid="stSidebar"] {
    animation: sidebarAppear 0.5s ease-out;
}

/* DIVIDER */

hr {
    border-color: #29364b !important;
}

/* RESPONSIVE */

@media(max-width: 768px) {
    .welcome-title {
        font-size: 27px;
    }

    .main-heading {
        font-size: 29px;
    }

    .block-container {
        padding-left: 15px;
        padding-right: 15px;
    }
}

/* REDUCED MOTION */

@media(prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "chats" not in st.session_state:

    chat_id = str(uuid.uuid4())

    st.session_state.chats = {
        chat_id: {
            "title": "New Chat",
            "messages": []
        }
    }

    st.session_state.active_chat_id = chat_id

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

if "top_p" not in st.session_state:
    st.session_state.top_p = 0.9


# =========================================================
# OLLAMA CONNECTION
# =========================================================

def get_models():

    try:
        response = requests.get(TAGS_API, timeout=3)
        response.raise_for_status()

        return [
            model["name"]
            for model in response.json().get("models", [])
        ]

    except requests.RequestException:
        return []


# =========================================================
# GENERATE RESPONSE
# =========================================================

def generate_response(
    conversation,
    model,
    temperature,
    top_p,
    system_prompt
):

    request_messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    request_messages.extend(conversation)

    payload = {
        "model": model,
        "messages": request_messages,
        "stream": True,
        "options": {
            "temperature": temperature,
            "top_p": top_p
        }
    }

    with requests.post(
        CHAT_API,
        json=payload,
        stream=True,
        timeout=(10, 300)
    ) as response:

        response.raise_for_status()

        for line in response.iter_lines():

            if not line:
                continue

            data = json.loads(line)

            if data.get("error"):
                raise RuntimeError(data["error"])

            token = data.get(
                "message", {}
            ).get("content", "")

            if token:
                yield token


# =========================================================
# CREATE NEW CHAT
# =========================================================

def create_new_chat():

    chat_id = str(uuid.uuid4())

    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": []
    }

    st.session_state.active_chat_id = chat_id


# =========================================================
# MODEL DISCOVERY
# =========================================================

models = get_models()
ollama_online = bool(models)

if DEFAULT_MODEL not in models and ollama_online:
    models.insert(0, DEFAULT_MODEL)

if not models:
    models = [DEFAULT_MODEL]


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="brand-icon">🤖</div>
    <div class="brand-name">MiniGPT</div>
    <div class="brand-description">
        Your personal AI workspace
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    if st.button("＋  New Chat", use_container_width=True):
        create_new_chat()
        st.rerun()

    st.markdown("### Recent Conversations")

    for chat_id, chat in reversed(
        list(st.session_state.chats.items())
    ):

        label = chat["title"][:28]

        if chat_id == st.session_state.active_chat_id:
            label = "●  " + label

        if st.button(
            label,
            key=f"history_{chat_id}",
            use_container_width=True
        ):
            st.session_state.active_chat_id = chat_id
            st.rerun()

    st.divider()

    st.markdown("### ⚙️ Model Settings")

    model_name = st.selectbox(
        "Language Model",
        models,
        index=models.index(DEFAULT_MODEL)
        if DEFAULT_MODEL in models else 0
    )

    temperature = st.slider(
        "Temperature",
        0.0, 1.5,
        st.session_state.temperature,
        0.1
    )

    st.session_state.temperature = temperature

    top_p = st.slider(
        "Top-P",
        0.1, 1.0,
        st.session_state.top_p,
        0.05
    )

    st.session_state.top_p = top_p

    with st.expander("Advanced System Instructions"):

        system_prompt = st.text_area(
            "Assistant Behavior",
            value=st.session_state.system_prompt,
            height=170
        )

        st.session_state.system_prompt = system_prompt

        if st.button("Reset Prompt"):
            st.session_state.system_prompt = DEFAULT_SYSTEM_PROMPT
            st.rerun()

    st.divider()

    st.markdown("### Runtime Status")

    if ollama_online:

        st.markdown(f"""
        <div class="status-card">
            <span class="online">● Connected</span><br><br>
            Runtime: Ollama<br>
            Model: {model_name}<br>
            Available models: {len(models)}
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="status-card">
            <span class="offline">● Disconnected</span><br><br>
            Start Ollama to use MiniGPT.
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    if st.button(
        "🗑️ Delete Current Chat",
        use_container_width=True
    ):

        active_id = st.session_state.active_chat_id

        del st.session_state.chats[active_id]

        if not st.session_state.chats:
            create_new_chat()
        else:
            st.session_state.active_chat_id = next(
                reversed(st.session_state.chats)
            )

        st.rerun()


# =========================================================
# ACTIVE CONVERSATION
# =========================================================

active_chat_id = st.session_state.active_chat_id
current_chat = st.session_state.chats[active_chat_id]
messages = current_chat["messages"]


# =========================================================
# MAIN HEADER
# =========================================================

col1, col2 = st.columns([5, 1])

with col1:

    st.markdown(
        '<div class="main-heading">MiniGPT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-subheading">'
        'Intelligent conversations. Powered by local AI.'
        '</div>',
        unsafe_allow_html=True
    )

with col2:

    if ollama_online:
        st.markdown(
            '<p style="color:#4ade80;text-align:right;'
            'padding-top:15px;">● Online</p>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<p style="color:#fb7185;text-align:right;'
            'padding-top:15px;">● Offline</p>',
            unsafe_allow_html=True
        )


# =========================================================
# WELCOME SCREEN
# =========================================================

if not messages:

    st.markdown("""
    <div class="welcome-container">

        <div class="welcome-icon">✨</div>

        <div class="welcome-title">
            What can I help you with?
        </div>

        <div class="welcome-description">
            Ask anything. Explore ideas. Learn something new.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<p style="color:#a5b4c7;font-size:13px;'
        'font-weight:600;">EXPLORE WITH MINIGPT</p>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💡  Explain Generative AI",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Explain Generative AI with a practical example."
            )
            st.rerun()

        if st.button(
            "🐍  Learn Python",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Teach me Python programming from the basics."
            )
            st.rerun()

    with col2:

        if st.button(
            "🧠  Understand RAG",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Explain Retrieval Augmented Generation with an example."
            )
            st.rerun()

        if st.button(
            "⚡  Explore AI Agents",
            use_container_width=True
        ):
            st.session_state.pending_prompt = (
                "Explain AI agents and their working with an example."
            )
            st.rerun()


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =========================================================
# USER INPUT
# =========================================================

prompt = st.chat_input("Message MiniGPT...")

pending_prompt = st.session_state.pending_prompt
st.session_state.pending_prompt = None

user_prompt = prompt or pending_prompt


# =========================================================
# GENERATE AI ANSWER
# =========================================================

if user_prompt:

    if not ollama_online:

        st.error("Ollama is offline. Please start Ollama.")

    else:

        current_chat["messages"].append({
            "role": "user",
            "content": user_prompt
        })

        if current_chat["title"] == "New Chat":
            current_chat["title"] = user_prompt[:35]

        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):

            typing_placeholder = st.empty()

            typing_placeholder.markdown("""
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
            """, unsafe_allow_html=True)

            try:

                answer = st.write_stream(
                    generate_response(
                        conversation=current_chat["messages"],
                        model=model_name,
                        temperature=temperature,
                        top_p=top_p,
                        system_prompt=st.session_state.system_prompt
                    )
                )

                typing_placeholder.empty()

                if answer:

                    current_chat["messages"].append({
                        "role": "assistant",
                        "content": answer
                    })

                else:

                    current_chat["messages"].pop()
                    st.warning("Empty response from the model.")

            except requests.exceptions.ConnectionError:

                current_chat["messages"].pop()
                typing_placeholder.empty()

                st.error("Cannot connect to Ollama.")

            except requests.exceptions.Timeout:

                current_chat["messages"].pop()
                typing_placeholder.empty()

                st.error("Request timed out. Try again.")

            except Exception as error:

                current_chat["messages"].pop()
                typing_placeholder.empty()

                st.error(f"Something went wrong: {error}")

        st.rerun()
