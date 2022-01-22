import streamlit as st
import requests
import json
import time

API_URL = "https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-emotion"
headers = {"Authorization": f"Bearer {rAplzyQGYLwcFPzUfSqVpGvRdvvXHrmfOitDsopymDDjoxtaOIEfDMeFALNMdDaNuQNIoPZfutTtqBCMlcRsDACtBUoHTsiPFsrQagnPmqyzKbJLAMBBTJTgLNpcvpOZ}"}

notes = []

def mood_inference(note):
    data = {"inputs": note}
    response = requests.post(API_URL, json=data, headers=headers)
    mood = response.json()

    notes.append(note)
    pass


st.sidebar.title("Better.me ©")

st.write("What's on your mind today?")
note = st.text_area("", value="...", max_chars=512, )
if st.button("Click here to add note"):
    mood_inference(note)

