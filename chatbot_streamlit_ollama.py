import streamlit as st
import ollama

st.set_page_config(page_title="Free AI Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Free AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = "llama3.2"

with st.sidebar:
    st.header("Settings")
    available_models = ["llama3.2", "mistral", "phi3", "gemma2"]
    selected_model = st.selectbox(
        "Choose a model",
        available_models,
        index=available_models.index(st.session_state.model),
    )
    st.session_state.model = selected_model

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    try:
        with st.spinner("Thinking..."):
            response = ollama.chat(
                model=st.session_state.model,
                messages=st.session_state.messages,
            )

        answer = response["message"]["content"]

        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception as e:
        st.error("Could not connect to Ollama locally.")
        st.info("Please install Ollama from https://ollama.com/ and make sure it is running before starting the app.")
        st.code("Try this in your terminal:\nollama pull llama3.2")