import streamlit as st
import requests
from datetime import datetime, time
from random import randint
from collections import Counter
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import hashlib
import sqlite3
from model_loading import *

from resources import choose_resources, choose_support


# Login & Security

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


# DB for Passwords

conn = sqlite3.connect('data.db')
c = conn.cursor()

# suicide_model = load_model()
# suicide_model.eval()


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT UNIQUE, password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


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
                ("Today I woke up, and didnt want to get out of bed. I just sort of laid there. This made me feel bad.",
                 "sadness", datetime(2020, 12, 15)),
                ("This afternoon, I ate a big meal. This made me feel good, I would like to eat more.", "joy",
                 datetime(2020, 12, 15)),
                ("It was hard for me to sleep yesterday, I had a girl on my mind.", "love", datetime(2020, 12, 16)),
                ("This morning, I got up before my alarm. I was excited to get out of bed!", "joy",
                 datetime(2020, 12, 16)),
                ("Uber gave me a free meal today. I wonder why.", "surprise", datetime(2020, 12, 16)),
                ("I couldnt fall asleap yesterday. I just stared at the cealing.", "anger", datetime(2020, 12, 17)),
                (
                "This morning I woke up with a horrible hedache. Motrin didn't help.", "anger", datetime(2020, 12, 17)),
                ("I havent written a post recently. Its a good habit I should get back into.", "anger",
                 datetime(2020, 12, 20)),
                ("WHY AM I SO STUPID. I failed a quiz today.", "anger", datetime(2020, 12, 21)),
                ("I cant stop thinking about that quiz. I studied so hard.", "sadness", datetime(2020, 12, 21)),
                ("Quiz still on my mind...", "sadness", datetime(2020, 12, 21)),
                ("I finally understand the material for my class!", "joy", datetime(2020, 12, 22)),
                ("Today was a beautiful day", "joy", datetime(2020, 12, 22)),
                ("I look forward to tomorrow", "joy", datetime(2020, 12, 22)),
                ("I spoke to a girl today", "love", datetime(2020, 12, 24)),
                ("I cant decide weather or not to message her...", "love", datetime(2020, 12, 24)),
                ("What a day", "surprise", datetime(2020, 12, 26)),
            ],
            "placeholder_text": "..."

        })

        # FAKE DATA GENERATOR
        mood_list = ["anger", "fear", "joy", "love", "sadness", "surprise"]
        weights = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 4, 6: 4, 7: 4, 8: 4, 9: 4, 10: 4, 11: 4, 12: 2, 13: 2, 14: 2, 15: 1,
                   16: 3, 16: 3, 17: 5, 18: 1, 19: 2}
        for i in range(100):
            st.session_state.notes.append(("Test Note: " + str(i), mood_list[weights[randint(0, 19)]],
                                           datetime(2021, 1 + ((i // 30) % 12), 1 + (i % 27), 0, 0, 0)))

    # page = "Home"

    with st.sidebar:
        st.title("better.me")
        if st.button("🏠     Home"): st.session_state.page = "Home"
        if st.button("📝     Journal"): st.session_state.page = "Journal"
        if st.button("📕     Previous Journals"): st.session_state.page = "Previous Journals"
        if st.button("📊     Analytics"): st.session_state.page = "Analytics"
        if st.button("📚     Recommendations"): st.session_state.page = "Resources"

    pages[st.session_state.page]()


def page_home():
    with st.container():
        st.title("🏠 Home")
        '''
        ##### Welcome to Better.Me. Please login below to access your personal AI powered diary.
        '''
        username = st.text_input('Username')
        password = st.text_input("Password", type="password")

        if st.button('Login'):
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username, check_hashes(password, hashed_pswd))
            if result:
                st.success("Logged In as {}".format(username))
                st.session_state.page = "Journal"
                page_journal()
            else:
                st.warning("Incorrect Username/Password")

        st.write('Not a member? Sign up from the button below')

        if st.button('Sign Me Up'):
            page_signup()


def page_signup():
    with st.container():

        new_username = st.text_input('New username')
        new_password = st.text_input("New password", type="password")

        if st.button('Sign Up'):
            if new_username or new_password is None:
                st.warning("Please input a username and/or password!")
            create_usertable()
            try:
                add_userdata(new_username, make_hashes(new_password))
                st.success("You have successfully created a valid Account")
                st.session_state.page = "Journal"
                page_journal()
            except Exception as e:
                st.warning("Username already exists")


def page_journal():
    st.title("📝 Write a note")
    API_URL = "https://api-inference.huggingface.co/models/mrm8488/t5-base-finetuned-emotion"
    API_TOKEN = "rAplzyQGYLwcFPzUfSqVpGvRdvvXHrmfOitDsopymDDjoxtaOIEfDMeFALNMdDaNuQNIoPZfutTtqBCMlcRsDACtBUoHTsiPFsrQagnPmqyzKbJLAMBBTJTgLNpcvpOZ"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def mood_to_emoji(mood):
        return {'sadness': '😢', 'joy': '😂', 'fear': '😱', 'anger': '😡', 'love': '😍', 'surprise': '😲'}[mood]

    def mood_inference(note):
        data = {"inputs": note}
        st.session_state.placeholder_text = note
        res = requests.post(API_URL, json=data, headers=headers).json()
        try:
            mood = res[0]['generated_text']
            date = datetime.now()
            st.info(f"Your mood report -- {mood} {mood_to_emoji(mood)}")
        except KeyError:
            st.warning("We're sorry! No meaningful mood analysis could be completed 😢.")
        # suicide_pred = pred(mood, suicide_model)
        #if suicide_pred == 1:
        #   st.warning(
        #       "We're so sorry that you are going through this. Help is available! Speak with someone today at +1 833-456-4566. \n Asking for help can be hard. That’s why we offer a safe place to talk - any time, in your own way. If you are having thoughts of suicide, you don’t have to face them alone. We are available if you need a safe and judgement free place to talk. Our responders are here to listen to you, support you, and keep you safe.")
        # notes.append(note)
        st.session_state.notes.append((note, mood, date))
        return mood

    st.write("What's on your mind today?")
    note = st.text_area("", placeholder=st.session_state.placeholder_text, max_chars=256)
    if st.button("Click here to add the note"):
        mood = mood_inference(note)
        while not mood: time.sleep(1)

        with st.container():
            p1, p2, p3 = choose_resources(mood, 3)
            c1, c2, c3 = st.columns(3)
            with c1:
                st.header(p1.title)
                st.write(p1.description)
                st.markdown("[Learn More](%s)" % p1.url, unsafe_allow_html=True)

            with c2:
                st.header(p2.title)
                st.write(p2.description)
                st.markdown("[Learn More](%s)" % p2.url, unsafe_allow_html=True)

            with c3:
                st.header(p3.title)
                st.write(p3.description)
                st.markdown("[Learn More](%s)" % p3.url, unsafe_allow_html=True)


def page_previous_journals():
    st.title("📕 Previous journals")

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

    for i in range(0, len(st.session_state.notes), 3):
        with st.container():
            col0, col1, col2 = st.columns(3)
            col_map = {0: col0, 1: col1, 2: col2}
            for j in range(i, min(i + 3, len(st.session_state.notes))):
                with col_map[j % 3]:
                    sample_journal(st.session_state.notes[j])

            st.markdown('---')


def page_analytics():
    st.title("📊 Analytics")

    counter = Counter(map(lambda x: x[1], st.session_state.get("notes", [])))
    mood_list = ["anger", "fear", "joy", "love", "sadness", "surprise"]
    mood_colors = ["red", "yellow", "green", "pink", "blue", "white"]

    mood_counts = pd.DataFrame({
        'Moods': mood_list,
        'Counts': [counter[mood] for mood in mood_list]
    })

    fig = make_subplots(rows=1, cols=2, subplot_titles=("Mood count -- bar", "Mood count -- pie"),
                        specs=[[{"type": "xy"}, {"type": "domain"}]], horizontal_spacing=0.1)
    fig.add_trace(go.Bar(x=mood_counts['Moods'], y=mood_counts['Counts']), row=1, col=1)
    fig.add_trace(go.Pie(values=mood_counts['Counts'], labels=mood_counts['Moods']), row=1, col=2)
    fig.layout.update(width=800, margin=dict(l=0))
    st.write(fig)

    earliest_date = min(map(lambda x: x[2], st.session_state.get("notes", [])))
    latest_date = max(map(lambda x: x[2], st.session_state.get("notes", [])))
    date_iterator = pd.date_range(earliest_date, latest_date, freq='W')

    line_graph_frequencies = []
    for date in date_iterator:
        line_graph_frequencies.append([0, 0, 0, 0, 0, 0])
        for note in st.session_state.get("notes", []):
            if note[2].date() <= date:
                line_graph_frequencies[-1][mood_list.index(note[1])] += 1
    for i in range(len(line_graph_frequencies) - 1, 0, -1):
        for j in range(6):
            line_graph_frequencies[i][j] -= line_graph_frequencies[i - 1][j]

    mood_line_graph = pd.DataFrame(
        line_graph_frequencies,
        columns=mood_list
    )
    mood_line_graph['Weeks'] = range(1, len(line_graph_frequencies) + 1)
    fig = px.line(mood_line_graph, x='Weeks', y=mood_list)
    fig.layout.update(width=800, margin=dict(l=0))
    st.write(fig)


def page_resources():
    st.title("📚 Resources")
    col1, col2, col3 = st.columns(3)

    # TODO: Change based on analytics page
    mood = "anger"

    p1, p2, p3 = choose_resources(mood, 3)

    with col1:
        st.header(p1.title)
        st.write(p1.description)
        st.markdown("[Learn More](%s)" % p1.url, unsafe_allow_html=True)

    with col2:
        st.header(p2.title)
        st.write(p2.description)
        st.markdown("[Learn More](%s)" % p2.url, unsafe_allow_html=True)

    with col3:
        st.header(p3.title)
        st.write(p3.description)
        st.markdown("[Learn More](%s)" % p3.url, unsafe_allow_html=True)

    st.markdown("---")
    st.title("Recommended Support")

    col4, col5, col6 = st.columns(3)

    s1, s2, s3 = choose_support(0), choose_support(1), choose_support(2)
    with col4:
        st.header(s1.title)
        st.write(s1.description)
        st.markdown("[Learn More](%s)" % s1.url, unsafe_allow_html=True)

    with col5:
        st.header(s2.title)
        st.write(s2.description)
        st.markdown("[Learn More](%s)" % s2.url, unsafe_allow_html=True)

    with col6:
        st.header(s3.title)
        st.write(s3.description)
        st.markdown("[Learn More](%s)" % s3.url, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
