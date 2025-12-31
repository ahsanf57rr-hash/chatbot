import streamlit as st
import json
import tempfile
import os

# =========================
# SAFE TTS IMPORT
# =========================
try:
    from gtts import gTTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

# =========================
# TTS FUNCTION
# =========================
def text_to_speech(text):
    if not TTS_AVAILABLE:
        return None
    try:
        tts = gTTS(text=text, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        st.warning(f"Text-to-Speech error: {e}")
        return None

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="University Help Desk Bot",
    page_icon="🎓",
    layout="wide"
)

# =========================
# LOAD KNOWLEDGE BASE SAFELY
# =========================
knowledge = []
knowledge_file_path = "knowledge.json"

if not os.path.exists(knowledge_file_path):
    st.error(f"knowledge.json file not found at {knowledge_file_path}")
else:
    try:
        with open(knowledge_file_path, "r", encoding="utf-8") as file:
            knowledge = json.load(file)
    except json.JSONDecodeError as e:
        st.error(f"Error decoding knowledge.json: {e}")
    except Exception as e:
        st.error(f"Unexpected error loading knowledge.json: {e}")

# =========================
# EXAMPLE QUESTIONS
# =========================
example_questions = {
    "Admissions": [
        "What is the admission process for undergraduate programs?",
        "What documents are required for admission?",
        "When do admissions usually open?"
    ],
    "Fees": [
        "What are the semester fee details?",
        "Are there any scholarships available?",
        "How can I pay my fees?"
    ],
    "Hostel": [
        "How can I apply for a hostel?",
        "What facilities are provided in hostels?",
        "What are the hostel rules?"
    ],
    "Academics": [
        "What is the grading policy?",
        "What is the attendance requirement?",
        "How can I register for courses?"
    ],
    "Library": [
        "What are the library timings?",
        "How many books can a student borrow?",
        "Are there digital resources available?"
    ]
}

# =========================
# ANSWER FUNCTION
# =========================
def get_answer(question):
    if not knowledge:
        return "❌ Knowledge base is not loaded. Please check knowledge.json."
    question = question.lower()
    for item in knowledge:
        for keyword in item.get("keywords", []):
            if keyword.lower() in question:
                return item.get("answer", "❌ No answer available.")
    return "❌ Sorry, I can only help with university-related queries."

# =========================
# SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

if "current_query" not in st.session_state:
    st.session_state.current_query = ""

# =========================
# HEADER
# =========================
st.title("🎓 University Help Desk Chatbot")
st.markdown("Ask a question or click from the FAQs below.")

# =========================
# FAQ DISPLAY
# =========================
st.subheader("💡 Frequently Asked Questions")

for category, questions in example_questions.items():
    with st.expander(category, expanded=False):
        cols = st.columns(3)
        for i, q in enumerate(questions):
            if cols[i % 3].button(q, key=f"{category}_{i}"):
                st.session_state.current_query = q
                st.rerun()

# =========================
# TEXT INPUT
# =========================
st.subheader("✍ Ask Your Question")

query = st.text_input(
    "Type here:",
    value=st.session_state.current_query
)

if st.button("Send") and query.strip():
    answer = get_answer(query)
    audio = text_to_speech(answer)
    st.session_state.history.append((query, answer, audio))
    st.session_state.current_query = ""

# =========================
# CHAT HISTORY
# =========================
st.subheader("💬 Chat History")

for q, a, audio in reversed(st.session_state.history):
    st.markdown(f"**🧑 You:** {q}")
    st.markdown(f"**🤖 Bot:** {a}")
    if audio:
        st.audio(audio, format="audio/mp3")
    st.markdown("---")
