import streamlit as st
from langchain_community.llms import Ollama

llm = Ollama(model="llama3")  # or your chosen model
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from pypdf import PdfReader

# Initialize LLM

st.write("🔄 Model loading...")
llm = Ollama(model="llama3.2:1b")
st.write("✅ Model loaded.")

st.set_page_config(page_title="Resume Coach", layout="wide")
st.title("🧾 Resume Builder + Job Coach")

menu = st.sidebar.selectbox(
    "Select an option",  # This is the required label
    ["Mock Interview Chatbot"]  # These are the options
)

# ────────────────────────────────────────────────────────────────
if menu == "Mock Interview Chatbot":
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.markdown("### 🎙️ Mock Interview for Any Role")
    user_input = st.text_input("You (Candidate):", key="interview_input")

    if st.button("Send") and user_input:
        conversation = "\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.chat_history])
        prompt = PromptTemplate(
            input_variables=["conversation", "user_input"],
            template="""
            You're simulating a mock interview. Continue the following interview. Ask one new question 
            or give constructive feedback.

            Interview so far:
            {conversation}

            Candidate's latest response:
            {user_input}
            """
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        reply = chain.run(conversation=conversation, user_input=user_input)

        st.session_state.chat_history.append((user_input, reply))

    for i, (question, reply) in enumerate(st.session_state.chat_history):
        st.markdown(f"**You:** {question}")
        st.markdown(f"**Coach:** {reply}")