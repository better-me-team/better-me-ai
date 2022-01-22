import streamlit as st

notes = []

def mood_checker(note):
    notes.append(note)
    pass


st.sidebar.title("Better.me ©")

st.write("What's on your mind today?")
note = st.text_area("", value="...", max_chars=512, )
if st.button("Click here to add note"):
    mood_checker(note)

