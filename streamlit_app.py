import streamlit as st
import nltk
nltk.download('punkt_tab')
from chatbot import predict_tag, get_response

st.set_page_config(page_title="RampageBot", page_icon="🤖")

st.title(":material/newspaper: RampageBot")
st.markdown("Ask me anything about **The Rampage**!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    tag = predict_tag(prompt)
    reply = get_response(tag)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
