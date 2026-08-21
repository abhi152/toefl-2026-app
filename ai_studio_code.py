import streamlit as st
import google.generativeai as genai

# --- APP CONFIG ---
st.set_page_config(page_title="TOEFL 2026 Writing Lab", page_icon="🎓")

# --- SIDEBAR: API SETTINGS ---
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    st.markdown("[Get a Free Key Here](https://aistudio.google.com/app/apikey)")
    st.info("Using Gemini 1.5 Flash (Free Tier). This model predicts your score based on the 2026 ETS Writing Rubrics.")

# --- SCORING LOGIC (GEMINI) ---
def get_gemini_score(task_type, user_input, prompt_context):
    if not api_key:
        return "⚠️ Please enter your Google API Key in the sidebar to get a score."
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        grading_prompt = f"""
        You are an official ETS TOEFL grader for the new 2026 Writing format.
        Evaluate the following {task_type} response.
        
        RUBRIC (Band Scale 1.0 - 6.0):
        - 6.0 (Distinguished): Flawless grammar, high-level vocabulary, fully addresses all prompt requirements.
        - 5.0 (Accomplished): Strong flow, minor errors that don't obscure meaning, good transitions.
        - 3.0-4.0 (Developing): Relevant but simple sentences, some repetitive vocabulary, mechanical errors.
        - 1.0-2.0 (Limited): Frequent errors, fails to address the prompt properly.

        PROMPT CONTEXT: {prompt_context}
        STUDENT RESPONSE: {user_input}

        Provide the output in this format:
        ### Predicted Band Score: [Score/6.0]
        **Grammar & Vocabulary:** [Feedback]
        **Task Fulfillment:** [Feedback]
        **Suggestions for Improvement:** [Advice]
        """
        
        response = model.generate_content(grading_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# --- UI INTERFACE ---
st.title("TOEFL iBT 2026 Writing Simulator")
st.caption("Updated for the January 2026 Format Changes")

tab1, tab2, tab3 = st.tabs(["Task 1: Build a Sentence", "Task 2: Write an Email", "Task 3: Academic Discussion"])

# --- TASK 1: BUILD A SENTENCE ---
with tab1:
    st.subheader("Task 1: Build a Sentence")
    st.write("Rearrange the phrases to form a correct academic sentence:")
    st.code("due to / the / the / was / flight / canceled / heavy / snow")
    t1_input = st.text_input("Type the full sentence:", key="t1")
    if st.button("Check Sentence"):
        correct = "the flight was canceled due to the heavy snow"
        if t1_input.lower().strip().replace(".", "") == correct:
            st.success("Correct! Band: 6.0")
        else:
            st.error(f"Incorrect. Correct: The flight was canceled due to the heavy snow.")

# --- TASK 2: WRITE AN EMAIL ---
with tab2:
    st.subheader("Task 2: Write an Email (7 Minutes)")
    context_2 = "Scenario: Write an email to your professor, Dr. Elena, asking for a summary of the lecture you missed last Tuesday. Explain that you had a technical issue with your internet. Mention your interest in the topic of 'Micro-Economics'."
    st.info(context_2)
    t2_input = st.text_area("Write 100-120 words:", height=200, key="t2")
    word_count2 = len(t2_input.split())
    st.write(f"Word Count: {word_count2}")
    
    if st.button("Score Email"):
        with st.spinner("Gemini AI is grading..."):
            result = get_gemini_score("Email Writing", t2_input, context_2)
            st.markdown(result)

# --- TASK 3: ACADEMIC DISCUSSION ---
with tab3:
    st.subheader("Task 3: Academic Discussion (10 Minutes)")
    context_3 = """Professor: 'Do you think social media has a positive or negative impact on young people's social skills?'
    Student A (Sarah): 'I think it's positive because it allows us to stay connected 24/7.'
    Student B (John): 'I disagree. It replaces real face-to-face interaction with shallow emojis.'"""
    st.write(context_3)
    t3_input = st.text_area("Write 100+ words (Contribute a new perspective):", height=250, key="t3")
    word_count3 = len(t3_input.split())
    st.write(f"Word Count: {word_count3}")

    if st.button("Score Discussion"):
        with st.spinner("Gemini AI is grading..."):
            result = get_gemini_score("Academic Discussion", t3_input, context_3)
            st.markdown(result)