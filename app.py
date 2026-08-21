import streamlit as st
from openai import OpenAI

# --- APP CONFIG ---
st.set_page_config(page_title="TOEFL 2026 Prep", page_icon="🎓")

# --- UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stTextArea textarea { font-size: 16px !format; }
    .score-box { background-color: #e1f5fe; padding: 20px; border-radius: 10px; border: 1px solid #01579b; }
    </style>
    """, unsafe_allow_html=True)

st.title("TOEFL iBT 2026 Writing Practice")
st.caption("New Format: Build a Sentence | Email Writing | Academic Discussion")

# --- SIDEBAR: API SETTINGS ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter OpenAI API Key to enable AI Scoring", type="password")
    st.info("The AI predicts your score based on the 1.0 - 6.0 Band Scale used in the 2026 Rubric.")

# --- SCORING LOGIC ---
def get_ai_score(task_type, user_input, prompt_context):
    if not api_key:
        return "⚠️ Please enter an API Key in the sidebar to get a score prediction."
    
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"""You are an official ETS TOEFL grader for the 2026 format. 
                Evaluate the response for a {task_type} task. 
                Use the 1.0 to 6.0 Band Scale. 
                Criteria: 1. Grammar Accuracy, 2. Vocabulary Range, 3. Task Fulfillment, 4. Cohesion.
                Provide the score clearly then a brief feedback summary."""},
                {"role": "user", "content": f"Prompt: {prompt_context}\n\nStudent Response: {user_input}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- TASK SELECTION ---
tab1, tab2, tab3 = st.tabs(["Task 1: Sentence", "Task 2: Email", "Task 3: Discussion"])

# --- TASK 1: BUILD A SENTENCE ---
with tab1:
    st.subheader("Build a Sentence")
    st.write("Rearrange the following to form a grammatically correct sentence:")
    st.code("although / the / was / difficult / exam / passed / all / the / students")
    t1_input = st.text_input("Your Answer:", key="t1")
    if st.button("Check Task 1"):
        correct = "although the exam was difficult all the students passed"
        if t1_input.lower().strip().replace(".", "") == correct:
            st.success("Perfect! Band 6.0")
        else:
            st.error(f"Correction: Although the exam was difficult, all the students passed.")

# --- TASK 2: WRITE AN EMAIL ---
with tab2:
    st.subheader("Write an Email (7 Minutes)")
    context_2 = "You are a student. Write an email to your Professor (Dr. Aris) explaining that you will be late for the lab session because of a flat tire. Ask if you can join the afternoon group instead."
    st.info(context_2)
    t2_input = st.text_area("Write 100-120 words:", height=200, key="t2")
    st.write(f"Word Count: {len(t2_input.split())}")
    
    if st.button("Score my Email"):
        with st.spinner("Analyzing against 2026 Rubrics..."):
            result = get_ai_score("Email Writing", t2_input, context_2)
            st.markdown(f"<div class='score-box'>{result}</div>", unsafe_allow_html=True)

# --- TASK 3: ACADEMIC DISCUSSION ---
with tab3:
    st.subheader("Academic Discussion (10 Minutes)")
    context_3 = """Professor: 'Should governments spend more money on exploring outer space or on protecting the environment here on Earth?' 
    Claire: 'Environment is urgent; we can't live elsewhere yet.' 
    Andrew: 'Space exploration leads to technological breakthroughs that help Earth.'"""
    st.write(context_3)
    t3_input = st.text_area("Write 100+ words (Contribute a new perspective):", height=250, key="t3")
    st.write(f"Word Count: {len(t3_input.split())}")

    if st.button("Score my Discussion"):
        with st.spinner("Analyzing against 2026 Rubrics..."):
            result = get_ai_score("Academic Discussion", t3_input, context_3)
            st.markdown(f"<div class='score-box'>{result}</div>", unsafe_allow_html=True)