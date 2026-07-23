import streamlit as st
from vector_store import FlowerShopVectorStore
from chatbot import app
from langchain_core.messages import AIMessage, HumanMessage
from tools import CUSTOMER_DATABASE

# Configure the Streamlit page with wide layout and custom title/icon
st.set_page_config(layout="wide", page_title="Flower Shop Chatbot", page_icon="🌻")
left_column, middle_column, right_column = st.columns(3, border=True)

# Initialize the vector store instance for querying FAQ and inventory data
vector_store = FlowerShopVectorStore()

# Initialize session state for message history
if "message_history" not in st.session_state:
    st.session_state.message_history = [AIMessage(content="Hi, I'm Eva! A flower shop assistant. How can I assist you today?")]

# Left column contains collection selection and chat controls
with left_column:
    # Clear button to reset the message history and start a fresh conversation
    if st.button("❌ Clear", key="clear_chat"):
        st.session_state.message_history = [AIMessage(content="Hi, I'm Eva! A flower shop assistant. How can I assist you today?")]


# Display the chat interface in the middle column
with middle_column:
    st.header("🌻 Eva")

    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message and assistant response to the message history
        st.session_state.message_history.append(HumanMessage(content=user_input))

        response = app.invoke({
            "messages": st.session_state.message_history
        })

        st.session_state.message_history = response["messages"]

    # Display all messages in the chat interface (in reverse order to show newest first)
    for message in (st.session_state.message_history)[::-1]:
        if isinstance(message, AIMessage):
            message_box = st.chat_message("assistant")
        else:
            message_box = st.chat_message("user")

        message_box.markdown(message.content)    # Render the message content as markdown


# Display the message history in the right column
with right_column:
    st.title('customers database')
    st.write(CUSTOMER_DATABASE)
