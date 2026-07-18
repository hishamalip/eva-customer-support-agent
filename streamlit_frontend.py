import streamlit as st
from vector_store import FlowerShopVectorStore

st.set_page_config(layout="wide", page_title="Flower Shop Chatbot", page_icon="🌻")
left_column, middle_column, right_column = st.columns(3, border=True)
vector_store = FlowerShopVectorStore()

# Initialize session state for message history
if "message_history" not in st.session_state:
    st.session_state.message_history = [{"content": "Hi, I'm Eva! A flower shop assistant. How can I assist you today?", "type": "assistant"}]

# Clear button to reset the message history
with left_column:
    collection_choice = st.radio("Select Collection: ", ["FAQs", "Inventory"], key="collection_choice")

    if st.button("❌ Clear", key="clear_chat"):
        st.session_state.message_history = [{"content": "Hi, I'm Eva! A flower shop assistant. How can I assist you today?", "type": "assistant"}]


# Display the chat interface in the middle column
with middle_column:
    st.header("🌻 Eva")

    user_input = st.chat_input("Type your message here...")

    if user_input:
        if collection_choice == "FAQs":
            related_questions = vector_store.query_faqs(user_input)
        if collection_choice == "Inventory":
            related_questions = vector_store.query_inventory(user_input)

        st.session_state.message_history.append({"content": user_input, "type": "user"})
        st.session_state.message_history.append({"content": related_questions, "type": "assistant"})

    for message in (st.session_state.message_history)[::-1]:
        # st.write(message["content"])
        message_box = st.chat_message(message['type'])
        message_box.markdown(message["content"])


# Display the message history in the right column
with right_column:
    st.header("Message History:")
    st.text(st.session_state.message_history)


