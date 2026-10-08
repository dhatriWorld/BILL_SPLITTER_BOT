import asyncio
from google import genai
from google.genai import types
import streamlit as st 

from telegram import Bot

from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE, SUMMARY_REQUEST_PROMPT

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key = GEMINI_API_KEY) 

@st.cache_resource
def get_telegram_bot():
    return Bot(token=TELEGRAM_BOT_TOKEN)


telegram_bot = get_telegram_bot() 
gemini_client = get_gemini_client()
MODEL_NAME = "gemini-3.5-flash"

def send_telegram(chat_id, text):
    try:
        asyncio.run(
            telegram_bot.send_message(
                chat_id=chat_id,
                text=text
            )
        )
        return True, "Message sent successfully"
    except Exception as error:
        return False, str(error)
    

def render_message(message):
    with st.chat_message(message["role"]):
        if message["kind"] == "text":
            st.write(message["content"])
        elif message["kind"] == "image":
            st.image(message["content"])

def add_message(role, kind, content):
    st.session_state.messages.append({"role": role, "kind": kind, "content": content})
    render_message(st.session_state.messages[-1])

def ask_gemini(parts):
    try:
        return st.session_state.chat.send_message(parts).text
    except Exception as error:
        return f"Sorry, something went wrong: {error}" 

#step 1: Onboarding(username and phone)
if 'onboarded' not in st.session_state:
    st.title("SplitBot - Quick Bill Splitter")
    st.caption("Upload a photo of your receipt or bill, and SplitBot will help you split it among friends.")

    with st.form("onboarding_form"):
        name = st.text_input("Enter your name:")
        telegram_chat_id = st.text_input( 
            "Enter your Telegram chat ID:",
            placeholder="e.g. 987654321",
            help="Start your Telegram bot and enter the chat ID associated with your conversation."
        )
        submitted = st.form_submit_button("Start Splitting")

    if submitted:
        if not name.strip() or not telegram_chat_id.strip():
            st.warning("Please enter both your name and Telegram chat ID to proceed.")
        else:
            st.session_state.name = name.strip()
            try:
                st.session_state.telegram_chat_id = int(telegram_chat_id.strip())
            except ValueError:
                st.error("Please enter a valid Telegram chat ID.")
                st.stop()
            #activate my ai
            st.session_state.chat = gemini_client.chats.create(
                model = MODEL_NAME,
                config = types.GenerateContentConfig(system_instruction = SYSTEM_PROMPT)
            )
            st.session_state.messages = [] 
            st.session_state.onboarded = True 
            st.rerun()
    st.stop()

#create a chat interface 

header_col, button_col = st.columns([5,2], vertical_alignment = "center")
with header_col:
    st.title("SplitBot - Quick Bill Splitter")

with button_col:
    send_disabled = len(st.session_state.messages) <= 1
    if st.button("Send to Telegram", disabled=send_disabled, use_container_width=True):
        with st.spinner("Generating final summary..."):
            summary = ask_gemini([SUMMARY_REQUEST_PROMPT])

        success, info = send_telegram(
            st.session_state.telegram_chat_id,
            summary
        )

        if success:
            st.success("Summary sent to Telegram Successfully!")
        else:
            st.error(f"Failed to send summary to Telegram: {info}")

st.caption(f"Logged in as: {st.session_state.name} - updates go to Telegram") 

if not st.session_state.messages:
    add_message("assistant","text", WELCOME_MESSAGE_TEMPLATE.format(name = st.session_state.name))
else:
    for message in st.session_state.messages:
        render_message(message) 

user_input = st.chat_input(
    "Ask a question or upload a receipt image", 
    accept_file = True, 
    file_type = ["jpg","jpeg","png"], ) 

if user_input:
    photo = user_input.files[0] if user_input.files else None
    text = user_input.text 
    parts = [] 

    if photo is not None:
        photo_bytes = photo.getvalue()
        add_message("user","image", photo_bytes)
        parts.append(types.Part.from_bytes(data=photo_bytes, mime_type=photo.type))
    if text:
        add_message("user","text",text)
        parts.append(text)
    elif photo is not None:
        parts.append("Please read the receipt and split the bill accordingly.")

    with st.spinner("Processing..."):
        answer = ask_gemini(parts)
    add_message("assistant","text", answer)
