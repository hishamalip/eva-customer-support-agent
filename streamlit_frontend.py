# Import required libraries
import streamlit as st
from vector_store import FlowerShopVectorStore

# Configure the Streamlit page with wide layout and custom title/icon
st.set_page_config(layout="wide", page_title="Flower Shop Chatbot", page_icon="🌻")
left_column, middle_column, right_column = st.columns(3, border=True)

# Initialize the vector store instance for querying FAQ and inventory data
vector_store = FlowerShopVectorStore()

# Initialize session state for message history
if "message_history" not in st.session_state:
    st.session_state.message_history = [{"content": "Hi, I'm Eva! A flower shop assistant. How can I assist you today?", "type": "assistant"}]

# Left column contains collection selection and chat controls
with left_column:
    # Radio button to choose which collection to query (FAQs or Inventory)
    collection_choice = st.radio("Select Collection: ", ["FAQs", "Inventory"], key="collection_choice")

    # Clear button to reset the message history and start a fresh conversation
    if st.button("❌ Clear", key="clear_chat"):
        st.session_state.message_history = [{"content": "Hi, I'm Eva! A flower shop assistant. How can I assist you today?", "type": "assistant"}]


# Display the chat interface in the middle column
with middle_column:
    st.header("🌻 Eva")

    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Query the appropriate collection based on user selection
        if collection_choice == "FAQs":
            related_questions = vector_store.query_faqs(user_input)
        if collection_choice == "Inventory":
            related_questions = vector_store.query_inventory(user_input)

        # Add user message and assistant response to the message history
        st.session_state.message_history.append({"content": user_input, "type": "user"})
        st.session_state.message_history.append({"content": related_questions, "type": "assistant"})

    # Display all messages in the chat interface (in reverse order to show newest first)
    for message in (st.session_state.message_history)[::-1]:
        # Create a chat message container for each message
        message_box = st.chat_message(message['type'])
        # Render the message content as markdown
        message_box.markdown(message["content"])


# Display the message history in the right column
with right_column:
    # Show the raw message history data for debugging/transparency
    st.header("Message History:")
    st.text(st.session_state.message_history)


