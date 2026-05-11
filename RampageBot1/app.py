import streamlit as st
import chatbot
import time
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Customer Support Bot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stChatMessage {
        padding: 10px;
        border-radius: 10px;
    }
    .chat-header {
        text-align: center;
        padding: 10px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm your customer support assistant. How can I help you today?"
    })

if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0

# Header with styling
st.markdown('<div class="chat-header">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🤖 Customer Support Bot")
    st.caption("Your AI-powered customer service assistant")
st.markdown('</div>', unsafe_allow_html=True)

# Main chat interface
chat_container = st.container()

with chat_container:
    # Display chat history
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
            st.markdown(message["content"])

            # Add timestamp for messages (optional)
            if "timestamp" in message:
                st.caption(f"_{message['timestamp']}_")

# Chat input at the bottom
with st.container():
    st.markdown("---")
    if prompt := st.chat_input("Type your message here...", key="chat_input"):
        # Add user message
        timestamp = time.strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })

        # Check for quit commands
        if prompt.lower().strip() in {"quit", "exit", "bye"}:
            response = "Goodbye! Have a great day. 👋"
            st.session_state.should_stop = True
        else:
            # Show typing indicator (Streamlit doesn't have native typing indicator)
            with st.spinner("Bot is thinking..."):
                time.sleep(0.5)  # Simulate thinking time

                # Get prediction from chatbot module
                tag = chatbot.predict_tag(prompt)
                response = chatbot.get_response(tag)

                # Increment conversation counter
                st.session_state.conversation_count += 1

        # Add bot response
        timestamp = time.strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": timestamp,
            "tag": tag if 'tag' in locals() else None
        })

        # Rerun to update the chat display
        st.rerun()

# Sidebar with information and controls
with st.sidebar:
    st.header("📊 Chat Statistics")

    # Calculate stats
    user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
    bot_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Your Messages", user_messages)
    with col2:
        st.metric("Bot Responses", bot_messages)

    st.metric("Total Conversations", st.session_state.conversation_count)

    # Controls
    st.header("⚙️ Controls")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.conversation_count = 0
        # Add welcome message back
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm your customer support assistant. How can I help you today?"
        })
        st.rerun()

    if st.button("📥 Export Chat"):
        # Convert chat to DataFrame
        chat_data = []
        for msg in st.session_state.messages:
            chat_data.append({
                "Role": msg["role"],
                "Message": msg["content"],
                "Timestamp": msg.get("timestamp", "")
            })
        df = pd.DataFrame(chat_data)

        # Convert to CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Chat History",
            data=csv,
            file_name="chat_history.csv",
            mime="text/csv"
        )

    # Confidence threshold slider
    st.header("🎯 Settings")
    confidence_threshold = st.slider(
        "Response Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.1,
        step=0.05,
        help="Lower values accept less confident matches"
    )

    # Example queries section
    st.header("💡 Try These Questions")

    example_queries = {
        "Account Help": [
            "How do I reset my password?",
            "I can't log into my account"
        ],
        "Order Support": [
            "Where is my order?",
            "I want to return an item"
        ],
        "General Info": [
            "What are your business hours?",
            "How can I contact support?"
        ]
    }

    for category, queries in example_queries.items():
        with st.expander(category):
            for query in queries:
                if st.button(query, key=f"example_{query}"):
                    # Simulate user sending this message
                    timestamp = time.strftime("%H:%M:%S")
                    st.session_state.messages.append({
                        "role": "user",
                        "content": query,
                        "timestamp": timestamp
                    })

                    with st.spinner("Generating response..."):
                        time.sleep(0.5)
                        tag = chatbot.predict_tag(query, threshold=confidence_threshold)
                        response = chatbot.get_response(tag)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response,
                            "timestamp": timestamp,
                            "tag": tag
                        })

                        st.session_state.conversation_count += 1
                    st.rerun()

    # About section
    st.header("ℹ️ About")
    st.markdown("""
    This chatbot uses:
    - **TF-IDF** for text vectorization
    - **Cosine Similarity** for matching
    - **NLTK** for text preprocessing
    - **Streamlit** for the interface

    The bot matches your query to the closest
    pattern in its training data and returns
    an appropriate response.
    """)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <p>Powered by Streamlit & TF-IDF • Version 1.0.0</p>
    </div>
    """,
    unsafe_allow_html=True
)
