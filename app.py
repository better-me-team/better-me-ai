import streamlit as st
import requests
import json
import datetime

# API_URL = "https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-emotion"
# headers = {"Authorization": f"Bearer {rAplzyQGYLwcFPzUfSqVpGvRdvvXHrmfOitDsopymDDjoxtaOIEfDMeFALNMdDaNuQNIoPZfutTtqBCMlcRsDACtBUoHTsiPFsrQagnPmqyzKbJLAMBBTJTgLNpcvpOZ}"}

def main():
    pages = {
        "Home": page_home,
        "Journal": page_journal,
        "Previous Journals": page_previous_journals,
        "Analytics": page_analytics,
    }
    
    if "page" not in st.session_state:
        st.session_state.update({
            # Default page
            "page": "Home",
            
            # Notes already made for demo
            "notes": [
                ("This is the first note you have ever made", "joy", datetime.datetime(2020, 1, 1, 0, 0)),
                ("This is your second note, congrats!", "love", datetime.datetime(2020, 1, 2, 0, 0)),
                ("Note 3", "sadness", datetime.datetime(2020, 1, 3, 0, 0)),
                ("You see where this is going", "anger", datetime.datetime(2020, 1, 4, 0, 0)),
            ],
            
            # Some user data that we would eventually manage with backend
            # user_data": {
            #     "name": "Users name",
            #     "Created_Date": "2020-01-01",
            # }
            
            # Default widget values
            # "text": "",
            "start_year": 2021,
            # "checkbox": False,
            # "radio": "Hello",
            # "selectbox": "Hello",
            # "multiselect": ["Hello", "Everyone"],
        })
        
    with st.sidebar:
        st.title("Better.me ©")
        if st.button("Home"): page = "Home"
        if st.button("Journal"): page = "Journal"
        if st.button("Previous Journals"): page = "Previous Journals"
        if st.button("Analytics"): page = "Analytics"
        
    pages[st.session_state.page]()


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
        

def page_previous_journals():

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
        st.header(date.date())
        st.write(text)
        mood_box[mood](mood)
        st.title("Previous journals")

    col0, col1, col2 = st.columns(3)
    col_map = {0: col0, 1: col1, 2: col2}

    for i, note in enumerate(st.session_state.get("notes", [])):
        with col_map[i % 3]:
            sample_journal(note)
            st.markdown('---')
        

def page_analytics():
    st.title("Analytics")
    col0, col1 = st.columns(2)
    
    with col0:
        st.selectbox("Start year", range(2021, 2022), key="start_year")
        start_day = st.slider("Start day", 0, 365)

    with col1:
        end_year = st.selectbox("End year", range(2021, 2022))
        end_day = st.slider("End day", 0, 365)
    

    

if __name__ == "__main__":
    main()
