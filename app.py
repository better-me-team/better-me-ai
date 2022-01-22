import streamlit as st
import requests
import json
from datetime import datetime

API_URL = "https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-emotion"
API_TOKEN = "rAplzyQGYLwcFPzUfSqVpGvRdvvXHrmfOitDsopymDDjoxtaOIEfDMeFALNMdDaNuQNIoPZfutTtqBCMlcRsDACtBUoHTsiPFsrQagnPmqyzKbJLAMBBTJTgLNpcvpOZ"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

notes = []

def mood_inference(note):
    data = {"inputs": note}
    res = requests.post(API_URL, json=data, headers=headers).json()
    mood = res[0]['generated_text']
    st.info(f"Your mood report -- {mood} {mood_to_emoji(mood)}")
    notes.append((note, mood, datetime.now()))

def mood_to_emoji(mood):
    return {'sadness': '😢', 'joy': '😂', 'fear': '😱', 'anger': '😡', 'disgust': '😤', 'surprise': '😲'}[mood]

def update_past_notes():
    for i in range(0, len(notes), 3):
        col1, col2, col3 = st.columns(3)
        with col1:
            note, mood, date = notes[i]
            with st.container():
                if st.button(f"{date.year}-{date.month}-{date.day} {mood_to_emoji(mood)}"):
                    display_note(note)

        try:
            with col2:
                note, mood, date = notes[i+1]
                with st.container():
                    if st.button(f"{date.year}-{date.month}-{date.day} {mood_to_emoji(mood)}"):
                        display_note(note)

            with col3:
                note, mood, date = notes[i+2]
                with st.container():
                    if st.button(f"{date.year}-{date.month}-{date.day} {mood_to_emoji(mood)}"):
                        display_note(note)

        except IndexError:
            pass



st.sidebar.title("Better.me ©")

# heading
'''
# What's on your mind today?
'''

note = st.text_area("", value="...", max_chars=512)
if st.button("Click here to add note"):
    mood_inference(note)
    update_past_notes()

'''
# View previous notes
'''

def display_note(note):
    with st.spinner():
        st.container
