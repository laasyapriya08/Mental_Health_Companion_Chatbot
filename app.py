import streamlit as st
import json
import uuid
from pathlib import Path

from config import APP_NAME, APP_TAGLINE
from services.gemini_service import gemini_service


# =================================================
# PAGE CONFIGURATION
# =================================================

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🧠",
    layout="wide"
)


# =================================================
# CHAT STORAGE FILE
# =================================================

CHAT_FILE = Path("chat_history.json")


# =================================================
# LOAD CHAT HISTORY
# =================================================

def load_chat_history():

    if CHAT_FILE.exists():

        try:

            with open(
                CHAT_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception:

            return []

    return []


# =================================================
# SAVE CHAT HISTORY
# =================================================

def save_chat_history():

    try:

        with open(
            CHAT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                st.session_state.chat_history,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception:

        pass


# =================================================
# SESSION STATE
# =================================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = (
        load_chat_history()
    )


if "messages" not in st.session_state:

    st.session_state.messages = []


if "current_chat_title" not in st.session_state:

    st.session_state.current_chat_title = (
        "New Chat"
    )


if "current_chat_id" not in st.session_state:

    st.session_state.current_chat_id = (
        str(uuid.uuid4())
    )


# =================================================
# CREATE CHAT TITLE
# =================================================

def create_chat_title(messages):

    for message in messages:

        if message["role"] == "user":

            text = message["content"].strip()

            if len(text) > 35:

                return text[:35] + "..."

            return text

    return "New Chat"


# =================================================
# SAVE / UPDATE CURRENT CHAT
# =================================================

def sync_current_chat():

    if not st.session_state.messages:

        return


    title = create_chat_title(
        st.session_state.messages
    )


    st.session_state.current_chat_title = (
        title
    )


    chat_found = False


    for chat in st.session_state.chat_history:

        if (
            chat["id"]
            == st.session_state.current_chat_id
        ):

            chat["title"] = title

            chat["messages"] = (
                st.session_state.messages.copy()
            )

            chat_found = True

            break


    if not chat_found:

        st.session_state.chat_history.append(
            {
                "id": (
                    st.session_state.current_chat_id
                ),

                "title": title,

                "messages": (
                    st.session_state.messages.copy()
                )
            }
        )


    save_chat_history()


# =================================================
# NEW CHAT
# =================================================

def new_chat():

    # Save current conversation
    sync_current_chat()


    # Create fresh chat
    st.session_state.messages = []

    st.session_state.current_chat_title = (
        "New Chat"
    )


    st.session_state.current_chat_id = (
        str(uuid.uuid4())
    )


# =================================================
# CLEAR CURRENT CHAT
# =================================================

def clear_current_chat():

    current_id = (
        st.session_state.current_chat_id
    )


    # Remove current chat from history
    st.session_state.chat_history = [

        chat

        for chat
        in st.session_state.chat_history

        if chat["id"] != current_id
    ]


    # Clear current conversation
    st.session_state.messages = []


    st.session_state.current_chat_title = (
        "New Chat"
    )


    st.session_state.current_chat_id = (
        str(uuid.uuid4())
    )


    save_chat_history()


# =================================================
# LOAD PREVIOUS CHAT
# =================================================

def load_chat(index):

    selected_chat = (
        st.session_state.chat_history[index]
    )


    st.session_state.messages = (
        selected_chat["messages"].copy()
    )


    st.session_state.current_chat_title = (
        selected_chat["title"]
    )


    st.session_state.current_chat_id = (
        selected_chat["id"]
    )


# =================================================
# DELETE CHAT
# =================================================

def delete_chat(index):

    deleted_chat = (
        st.session_state.chat_history[index]
    )


    deleted_id = deleted_chat["id"]


    del st.session_state.chat_history[index]


    # If current chat is deleted
    if (
        deleted_id
        == st.session_state.current_chat_id
    ):

        st.session_state.messages = []

        st.session_state.current_chat_title = (
            "New Chat"
        )


        st.session_state.current_chat_id = (
            str(uuid.uuid4())
        )


    save_chat_history()


# =================================================
# SIDEBAR
# =================================================

with st.sidebar:

    st.title("🧠 MindMate")

    st.caption(APP_TAGLINE)

    st.divider()


    # NEW CHAT

    if st.button(

        "➕ New Chat",

        use_container_width=True

    ):

        new_chat()

        st.rerun()


    # CLEAR CURRENT CHAT

    if st.button(

        "🗑️ Clear Current Chat",

        use_container_width=True

    ):

        clear_current_chat()

        st.rerun()


    st.divider()


    # PREVIOUS CHATS

    st.subheader(
        "💬 Previous Chats"
    )


    if not st.session_state.chat_history:

        st.caption(
            "No previous chats yet."
        )


    else:

        # Latest chats first

        for index in reversed(

            range(
                len(
                    st.session_state.chat_history
                )
            )

        ):

            chat = (
                st.session_state.chat_history[index]
            )


            col1, col2 = st.columns(
                [5, 1]
            )


            # LOAD CHAT

            with col1:

                if st.button(

                    f"💬 {chat['title']}",

                    key=f"chat_{index}",

                    use_container_width=True

                ):

                    load_chat(index)

                    st.rerun()


            # DELETE CHAT

            with col2:

                if st.button(

                    "🗑️",

                    key=f"delete_{index}"

                ):

                    delete_chat(index)

                    st.rerun()


# =================================================
# MAIN PAGE
# =================================================

st.title("🧠 MindMate")

st.caption(APP_TAGLINE)


# =================================================
# WELLNESS DISCLAIMER
# =================================================

st.info(

    "MindMate is a supportive mental wellness "
    "companion. It is not a replacement for a "
    "doctor, therapist, counselor, or emergency "
    "service."

)


# =================================================
# DISPLAY CHAT MESSAGES
# =================================================

for message in st.session_state.messages:

    with st.chat_message(

        message["role"]

    ):

        st.markdown(

            message["content"]

        )


# =================================================
# CHAT INPUT
# =================================================

user_message = st.chat_input(

    "Share what's on your mind..."

)


# =================================================
# GENERATE AI RESPONSE
# =================================================

if user_message:


    # STORE USER MESSAGE

    st.session_state.messages.append(

        {

            "role": "user",

            "content": user_message

        }

    )


    # DISPLAY USER MESSAGE

    with st.chat_message("user"):

        st.markdown(
            user_message
        )


    # GENERATE AI RESPONSE

    with st.chat_message("assistant"):

        with st.spinner(

            "MindMate is listening..."

        ):

            response = (
                gemini_service.generate_response(
                    user_message
                )
            )


        st.markdown(
            response
        )


    # STORE AI RESPONSE

    st.session_state.messages.append(

        {

            "role": "assistant",

            "content": response

        }

    )


    # SAVE CHAT PERMANENTLY

    sync_current_chat()