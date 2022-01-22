import streamlit as st
import requests
import json
import time

# API_URL = "https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-emotion"
# headers = {"Authorization": f"Bearer {rAplzyQGYLwcFPzUfSqVpGvRdvvXHrmfOitDsopymDDjoxtaOIEfDMeFALNMdDaNuQNIoPZfutTtqBCMlcRsDACtBUoHTsiPFsrQagnPmqyzKbJLAMBBTJTgLNpcvpOZ}"}

def main():
    pages = {
        "Home": page_home,
        "Journal": page_journal,
        "Analytics": page_analytics,
    }
    
    if "page" not in st.session_state:
        st.session_state.update({
            # Default page
            "page": "Home",
            
            # Notes already made for demo
            "notes": [
                "This is the first note you have ever made",
                "This is your second note, congrats!",
                "Note 3",
                "You see where this is going"
            ]
            
            # Default widget values
            # "text": "",
            # "slider": 0,
            # "checkbox": False,
            # "radio": "Hello",
            # "selectbox": "Hello",
            # "multiselect": ["Hello", "Everyone"],
        })
        
    page = "Home"

    with st.sidebar:
        st.title("Better.me ©")
        if st.button("Home"): page = "Home"
        if st.button("Journal"): page = "Journal"
        if st.button("Analytics"): page = "Analytics"
        
    pages[page]()


def page_home():
    st.title("Home")


def page_journal():
    def mood_inference(note):
        data = {"inputs": note}
        response = requests.post(API_URL, json=data, headers=headers)
        mood = response.json()
    
        notes.append(note)
        pass
    
    st.write("What's on your mind today?")
    note = st.text_area("", value="...", max_chars=512, )
    if st.button("Click here to add note"):
        mood_inference(note)
        

def page_analytics():
    st.title("Analytics")


if __name__ == "__main__":
    main()
