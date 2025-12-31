import streamlit as st
import json
from gtts import gTTS
import tempfile

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="University Help Desk Bot",
    page_icon="🎓",
    layout="wide"   # helps alignment
)

# =========================
# LOAD KNOWLEDGE BASE
# =========================
with open("knowledge.json", "r", encoding="utf-8") as file:
    knowledge = json.load(file)

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
# FUNCTIONS
# =========================
def get_answer(question):
    question = question.lower()
    for item in knowledge:
        for keyword in item["keywords"]:
            if keyword in question:
                return item["answer"]
    return "❌ Sorry, I can only help with university-related queries."

def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# =========================
# SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

if "current_query" not in st.session_state:
    st.session_state.current_query = ""

# =========================
# HEADER (LEFT ALIGNED)
# =========================
st.title("🎓 University Help Desk Chatbot")
st.markdown("Ask a question or click from the FAQs below.")

# =========================
# FAQ DISPLAY (NO SELECT BOX)
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
    st.audio(audio, format="audio/mp3")
    st.markdown("---")
