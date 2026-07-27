import streamlit as st
from chatbot import app
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from tools import CUSTOMER_DATABASE, ORDERS_DATABASE

# Configure the Streamlit page with wide layout and custom title/icon
st.set_page_config(layout="wide", page_title="Eva", page_icon="🌻")

# Initialize session state for message history
if "message_history" not in st.session_state:
    st.session_state.message_history = [AIMessage(content="Hi, I'm Eva! A flower shop assistant. How can I assist you today?")]


# --- 1. HEADER ---
col1, col2 = st.columns([7, 1])
with col1:
    st.title("🌻 Eva")
    st.caption("Flower Shop Customer Support Agent")
with col2:
    if st.button("❌ Clear History"):
        st.session_state.message_history = [AIMessage(content="Hi, I'm Eva! A flower shop assistant. How can I assist you today?")]


# --- BODY ---
chat_box = st.container(height=375) # Provided height to make the section scrollable
with chat_box:
    for message in st.session_state.message_history:
        if not message:
            continue
        # For the tool calls, message contents would be empty, skip it
        if hasattr(message, 'content') and not message.content:
            continue
        # Skip ToolMessage objects (internal tool outputs) - Entire LLM outputs
        if isinstance(message, ToolMessage):
            continue
        # Skip messages with dict/list content (raw tool outputs)
        if isinstance(message.content, (dict, list)):
            continue
        # Skip messages that look like JSON
        content = str(message.content)
        if content.strip().startswith('{') or content.strip().startswith('['):
            continue

        role = "assistant" if isinstance(message, AIMessage) else "user"
        st.chat_message(role).markdown(message.content)


# --- FOOTER ---
user_input = st.chat_input("Type your message here...")
if user_input:
    # Add to history
    st.session_state.message_history.append(HumanMessage(content=user_input))

    # Display user message immediately
    with chat_box:
        st.chat_message("user").markdown(user_input)

        # Show spinner while thinking
        with st.spinner("Eva is thinking..."):
            response = app.invoke({"messages": st.session_state.message_history})
            # Update history with AI response
            st.session_state.message_history = response["messages"]

    # Trigger rerun to show AI response
    st.rerun()
