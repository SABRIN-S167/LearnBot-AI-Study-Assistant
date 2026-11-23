import os
import re
import random
import streamlit as st

st.set_page_config(page_title="LearnBot | AI Study Assistant", page_icon="🎓", layout="wide")

st.markdown("""
<style>
:root { --ink:#172033; --muted:#64748b; --line:#e7eaf0; }
.block-container {max-width: 1120px; padding-top: 2rem; padding-bottom: 3rem;}
.hero {padding: 1.5rem 1.7rem; border:1px solid var(--line); border-radius:20px;
       background:linear-gradient(120deg,#f0f5ff,#f7f2ff);}
.hero h1 {margin:0; color:#172033; font-size:2.35rem;}
.hero p {color:#53627a; margin:.45rem 0 0 0; font-size:1.03rem;}
div[data-testid="stMetric"] {background:#fff; border:1px solid var(--line); padding:14px; border-radius:14px;}
.stButton>button {border-radius:10px; min-height:2.7rem;}
.small-note {color:#64748b;font-size:.88rem;}
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []
if "quiz" not in st.session_state:
    st.session_state.quiz = None

def get_ai_response(prompt, api_key, model):
    if not api_key:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=model, contents=prompt)
        return response.text or "The AI returned an empty response. Please try again."
    except Exception as exc:
        return f"AI request failed: {exc}\n\nCheck your internet connection, API key, model name and Google AI Studio usage limits."

def demo_answer(question, level):
    q = question.strip().lower()
    if "photosynthesis" in q:
        return ("Photosynthesis is the process by which green plants prepare food using sunlight. "
                "Chlorophyll captures light energy. The plant uses carbon dioxide and water to make glucose and releases oxygen.\n\n"
                "**Simple equation:** Carbon dioxide + Water + Light energy → Glucose + Oxygen.\n\n"
                "**Example:** A plant kept in sunlight can make food in its leaves.")
    if "database" in q or "dbms" in q:
        return ("A **database** is an organized collection of related data. A **DBMS** (Database Management System) "
                "is software used to create, store, retrieve and manage that data.\n\n"
                "**Example:** A college database can store student IDs, names, departments and marks.\n\n"
                "**Why it is useful:** It reduces unnecessary duplication and makes data easier to search and update.")
    if "algorithm" in q:
        return ("An **algorithm** is a finite sequence of clear steps used to solve a problem.\n\n"
                "**Example – finding the larger of two numbers:**\n1. Read A and B.\n2. Compare A and B.\n"
                "3. Display the larger value.\n4. Stop.\n\nA good algorithm should be clear, finite and effective.")
    return (f"Let's understand **{question.strip()}** at a {level.lower()} level.\n\n"
            "1. **Meaning:** Start by identifying the main concept and the problem it solves.\n"
            "2. **How it works:** Break the concept into smaller steps and understand what happens at each step.\n"
            "3. **Example:** Connect the idea to a familiar real-world or classroom example.\n"
            "4. **Remember:** Write the definition, key points and one example in your own words.\n\n"
            "*Demo mode is using a sample explanation. Add a Gemini API key in the sidebar for a real, topic-specific AI answer.*")

def simple_summary(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s for s in sentences if len(s.split()) > 4]
    if not sentences:
        return "Please paste a little more text so I can create a summary."
    chosen = sentences[:min(5, len(sentences))]
    return "### Quick summary\n" + "\n".join(f"- {s}" for s in chosen) + "\n\n**Key idea:** Review the main terms and examples in the original notes."

def build_quiz_prompt(notes, count, level):
    return f"""Create {count} multiple-choice study questions from these notes.
Difficulty: {level}. Use only facts supported by the notes.
For each question provide four options labelled A-D, then the correct answer and a one-sentence explanation.
Make the questions distinct and student-friendly.
NOTES:
{notes}"""

def demo_quiz(notes, count):
    words = [w.strip(".,:;()[]{}").lower() for w in re.findall(r'\b[A-Za-z][A-Za-z-]{4,}\b', notes)]
    words = list(dict.fromkeys([w for w in words if w not in {"which","there","their","these","those","about","because","through","should","would","could"}]))
    if not words:
        words = ["concept", "process", "system"]
    questions = []
    for i in range(count):
        answer = words[i % len(words)].capitalize()
        questions.append({
            "q": f"Which term appears in your notes and should be revised?",
            "options": [answer, "Not mentioned", "Unrelated topic", "None of these"],
            "answer": answer,
            "why": f"“{answer}” is present in the text you supplied. Demo questions are simple revision prompts, not a full assessment."
        })
    return questions

with st.sidebar:
    st.title("⚙️ Settings")
    st.caption("Choose how LearnBot responds.")
    api_key = st.text_input("Gemini API key", type="password", help="Optional. Used only during this app session; do not share it.")
    model = st.selectbox("Gemini model", ["gemini-3.8-flash", "gemini-2.5-flash"], index=0)
    if api_key:
        st.success("Gemini key entered for this session.")
    else:
        st.info("Demo mode is active. Add a key to enable live AI.")
    st.divider()
    st.markdown("**Privacy note**")
    st.caption("Your pasted notes are processed in this app. With Gemini enabled, the prompt is sent to Google to generate a response. Avoid entering confidential or personal information.")
    st.markdown("[Get a Gemini API key](https://aistudio.google.com/app/apikey)")

st.markdown("""
<div class="hero">
<h1>🎓 LearnBot</h1>
<p>Your friendly AI study assistant — understand topics, simplify notes and practise with quizzes.</p>
</div>
""", unsafe_allow_html=True)
st.write("")
m1, m2, m3 = st.columns(3)
m1.metric("Study tools", "4", "Ask • Explain • Summarize • Quiz")
m2.metric("Mode", "Live AI" if api_key else "Demo", "Gemini connected" if api_key else "No API key needed")
m3.metric("Built for", "Students", "Simple explanations")

tab1, tab2, tab3, tab4 = st.tabs(["💬 Ask & Explain", "📝 Summarize Notes", "🧠 Create a Quiz", "📚 Study Planner"])

with tab1:
    st.subheader("Ask a study question")
    st.caption("Ask for a definition, step-by-step explanation, comparison or worked example.")
    level = st.select_slider("Explanation level", options=["Beginner", "School level", "College level", "Exam-ready"], value="College level")
    question = st.text_area("Your question", placeholder="Example: Explain the difference between stack and queue with an example.", height=115, key="ask_q")
    if st.button("Generate explanation", type="primary", key="ask_btn"):
        if not question.strip():
            st.warning("Enter a question first.")
        else:
            prompt = f"""You are LearnBot, a patient college study tutor. Explain this topic at {level} level.
Use clear headings, simple language, accurate definitions, numbered steps where useful, and one practical example.
If it is a programming or mathematics topic, include a small correct example. Do not invent facts.
Question: {question}"""
            with st.spinner("Preparing your explanation..."):
                answer = get_ai_response(prompt, api_key, model) if api_key else None
                if answer is None:
                    answer = demo_answer(question, level)
            st.session_state.history.insert(0, (question, answer))
    if st.session_state.history:
        st.markdown("#### Explanation")
        st.markdown(st.session_state.history[0][1])
        with st.expander("Previous questions"):
            for old_q, old_a in st.session_state.history[1:]:
                st.markdown(f"**Q: {old_q}**")
                st.markdown(old_a)

with tab2:
    st.subheader("Turn long notes into revision points")
    notes = st.text_area("Paste your lesson notes here", height=240, placeholder="Paste text from your notes or textbook...")
    col_a, col_b = st.columns([1, 1])
    with col_a:
        summary_style = st.selectbox("Summary style", ["Bullet-point notes", "Short paragraph", "Exam revision"])
    with col_b:
        summary_length = st.selectbox("Detail", ["Short", "Medium", "Detailed"], index=1)
    if st.button("Summarize notes", type="primary"):
        if not notes.strip():
            st.warning("Paste your notes first.")
        else:
            prompt = f"""Summarize these student notes as {summary_style}, with {summary_length.lower()} detail.
Preserve all important concepts, definitions, formulas, examples and headings. Do not add unsupported facts.
Use clear, exam-friendly language.
NOTES:\n{notes}"""
            with st.spinner("Summarizing..."):
                result = get_ai_response(prompt, api_key, model) if api_key else None
                if result is None:
                    result = simple_summary(notes)
            st.markdown(result)
            st.download_button("Download summary (.txt)", result, file_name="learnbot_summary.txt", mime="text/plain")

with tab3:
    st.subheader("Create a practice quiz")
    quiz_notes = st.text_area("Paste notes for quiz questions", height=190, placeholder="Paste a topic or lesson here...")
    c1, c2 = st.columns(2)
    with c1:
        quiz_count = st.slider("Number of questions", 3, 10, 5)
    with c2:
        quiz_level = st.selectbox("Quiz difficulty", ["Easy", "Moderate", "Challenging"])
    if st.button("Create quiz", type="primary"):
        if not quiz_notes.strip():
            st.warning("Paste notes before creating a quiz.")
        else:
            if api_key:
                prompt = build_quiz_prompt(quiz_notes, quiz_count, quiz_level) + "\nFormat clearly with question numbers and answer key at the end."
                with st.spinner("Creating your quiz..."):
                    quiz_text = get_ai_response(prompt, api_key, model)
                st.session_state.quiz = {"text": quiz_text}
            else:
                st.session_state.quiz = {"questions": demo_quiz(quiz_notes, quiz_count)}
    if st.session_state.quiz:
        if "text" in st.session_state.quiz:
            st.markdown(st.session_state.quiz["text"])
        else:
            st.info("Demo quiz: these are simple note-based revision prompts. Connect Gemini for meaningful topic-specific MCQs.")
            score = 0
            for idx, item in enumerate(st.session_state.quiz["questions"], 1):
                choice = st.radio(f"{idx}. {item['q']}", item["options"], key=f"quiz_{idx}")
                if st.button(f"Check answer {idx}", key=f"check_{idx}"):
                    if choice == item["answer"]:
                        st.success("Correct!")
                    else:
                        st.warning(f"Suggested answer: {item['answer']}")
                    st.caption(item["why"])

with tab4:
    st.subheader("Make a simple study plan")
    subjects = st.text_input("Subjects or topics", placeholder="Example: DBMS, Python, Compiler Design")
    available = st.number_input("Study time per day (hours)", min_value=0.5, max_value=12.0, value=2.0, step=0.5)
    days = st.slider("Plan length (days)", 1, 14, 7)
    if st.button("Create study plan", type="primary"):
        if not subjects.strip():
            st.warning("Enter at least one subject.")
        else:
            prompt = f"""Create a realistic {days}-day student study plan for these subjects: {subjects}.
The student has {available} hours per day. Give a daily table with focused sessions, short breaks,
revision and practice. Keep workload balanced and include a final review."""
            with st.spinner("Planning your study time..."):
                plan = get_ai_response(prompt, api_key, model) if api_key else None
            if plan:
                st.markdown(plan)
            else:
                items = [x.strip() for x in subjects.split(",") if x.strip()]
                per = available / max(1, len(items))
                st.info("Demo plan — a simple rotation. Add Gemini for a tailored plan.")
                for day in range(days):
                    subject = items[day % len(items)]
                    st.markdown(f"**Day {day+1}: {subject}** — {per:.1f} hr study, 15 min break, then 20 min active recall/revision.")

st.divider()
st.markdown("<p class='small-note'>LearnBot is a student project starter. Always verify important academic answers with your textbook or faculty notes.</p>", unsafe_allow_html=True)
