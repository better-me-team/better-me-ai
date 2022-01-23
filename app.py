import streamlit as st
import requests
import json
from datetime import datetime

from resources import choose_resources


def main():
    pages = {
        "Home": page_home,
        "Journal": page_journal,
        "Previous Journals": page_previous_journals,
        "Analytics": page_analytics,
        "Resources": page_resources,
    }

    if "page" not in st.session_state:
        st.session_state.update({
            # Default page
            "page": "Home",

            # Notes already made for demo
            "notes": [
                ("This is the first note you have ever made", "joy", "2020-01-01"),
                ("This is your second note, congrats!", "love", "2020-01-02"),
                ("Note 3", "sadness", "2020-01-03"),
                ("You see where this is going", "anger", "2020-01-04"),
            ],
            "placeholder_text": "..."

            # Default widget values
            # "text": "",
            # "slider": 0,
            # "checkbox": False,
            # "radio": "Hello",
            # "selectbox": "Hello",
            # "multiselect": ["Hello", "Everyone"],
        })

    # page = "Home"

    with st.sidebar:
        st.title("Better.me ©")
        if st.button("Home"): st.session_state.page = "Home"
        if st.button("Journal"): st.session_state.page = "Journal"
        if st.button("Previous Journals"): st.session_state.page = "Previous Journals"
        if st.button("Analytics"): st.session_state.page = "Analytics"
        if st.button("Resources"): st.session_state.page = "Resources"

    pages[st.session_state.page]()


def page_home():
    st.title("Home")


def page_journal():
    API_URL = "https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-emotion"
    API_TOKEN = "rAplzyQGYLwcFPzUfSqVpGvRdvvXHrmfOitDsopymDDjoxtaOIEfDMeFALNMdDaNuQNIoPZfutTtqBCMlcRsDACtBUoHTsiPFsrQagnPmqyzKbJLAMBBTJTgLNpcvpOZ"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def mood_to_emoji(mood):
        return {'sadness': '😢', 'joy': '😂', 'fear': '😱', 'anger': '😡', 'disgust': '😤', 'surprise': '😲'}[mood]

    def mood_inference(note):
        data = {"inputs": note}
        st.session_state.placeholder_text = note
        res = requests.post(API_URL, json=data, headers=headers).json()
        mood = res[0]['generated_text']
        date = datetime.now()
        st.info(f"Your mood report -- {mood} {mood_to_emoji(mood)}")
        # notes.append(note)
        st.session_state.notes.append((note, mood, f"{date.year}-{date.month}-{date.day}"))

    st.write("What's on your mind today?")
    note = st.text_area("", placeholder=st.session_state.placeholder_text, max_chars=512)
    if st.button("Click here to add note"):
        mood_inference(note)


def page_previous_journals():
    st.title("Previous journals")

    mood_box = {
        "anger": st.error,
        "fear": st.warning,
        "joy": st.success,
        "love": st.error,
        "sadness": st.info,
        "surprise": st.success,
    }

    def sample_journal(note):
        text, mood, date = note
        st.header(date)
        st.write(text)
        mood_box[mood](mood)

    col0, col1, col2 = st.columns(3)
    col_map = {0: col0, 1: col1, 2: col2}

    for i, note in enumerate(st.session_state.get("notes", [])):
        with col_map[i % 3]:
            sample_journal(note)
            st.markdown('---')


def page_analytics():
    st.title("Analytics")


def page_resources():

    st.title("Resources")
    col1, col2, col3 = st.columns(3)

    # TODO: Change based on analytics page
    mood = "anger"

    p1 = choose_resources(mood)
    p2 = choose_resources(mood)
    p3 = choose_resources(mood)

    with col1:
        st.header(p1.title)
        st.write(p1.description)
        st.markdown("<a href=\"p1.url\"> Learn More </a>", unsafe_allow_html=True)

    with col2:
        st.header(p2.title)
        st.write(p2.description)
        st.markdown("<a href=\"p1.url\"> Learn More </a>", unsafe_allow_html=True)

    with col3:
        st.header(p3.title)
        st.write(p3.description)
        st.markdown("<a href=\"p3.url\"> Learn More </a>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
