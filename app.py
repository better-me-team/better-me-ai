import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import numpy as np
from random import randint
import altair as alt
from collections import Counter
import time
from resources import choose_resources, choose_support


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
                ("Today I woke up, and didnt want to get out of bed. I just sort of laied there. This made me feel bad.", "sadness", datetime(2020, 12, 15)),
                ("This afternoon, I ate a big meal. This made me feel good, I would like to eat more.", "joy", datetime(2020, 12, 15)),
                ("It was hard for me to sleep yesterday, I had a girl on my mind.", "love", datetime(2020, 12, 16)),
                ("This morning, I got up before my alarm. I was excited to get out of bed!", "joy", datetime(2020, 12, 16)),
                ("Uber gave me a free meal today. I wonder why.", "surprise", datetime(2020, 12, 16)),
                ("I couldnt fall asleap yesterday. I just stared at the cealing.", "anger", datetime(2020, 12, 17)),
                ("This morning I woke up with a horrible hedache. Motrin didn't help.", "anger", datetime(2020, 12, 17)),
                ("I havent written a post recently. Its a good habit I should get back into.", "anger", datetime(2020, 12, 20)),
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

            # Default widget values
            # "text": "",
            # "slider": 0,
            # "checkbox": False,
            # "radio": "Hello",
            # "selectbox": "Hello",
            # "multiselect": ["Hello", "Everyone"],
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
        password = st.text_input('Password')

        if st.button('Login'):
            st.session_state.page = "Journal"
            # page_journal()

        st.write('Not a member? Sign up here')


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
        mood = res[0]['generated_text']
        date = datetime.now()
        st.info(f"Your mood report -- {mood} {mood_to_emoji(mood)}")
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

    col0, col1 = st.columns(2)

    counter = Counter(map(lambda x: x[1], st.session_state.get("notes", [])))
    mood_list = ["anger", "fear", "joy", "love", "sadness", "surprise"]
    mood_colors = ["red", "yellow", "green", "pink", "blue", "white"]

    mood_counts = pd.DataFrame({
        'Moods': mood_list,
        'Counts': [counter[mood] for mood in mood_list]
    })

    def mood_bar_graph():
        mood_counts_graph = alt.Chart(mood_counts).mark_bar().encode(
            x='Moods',
            y='Counts',
            color=alt.Color('Moods', scale=alt.Scale(domain=mood_list, range=mood_colors))
        )

        st.altair_chart(
            mood_counts_graph,
            use_container_width=True,
        )

    def mood_pie_graph():
        mood_counts_graph = alt.Chart(mood_counts).mark_arc().encode(
            theta=alt.Theta(field="Counts", type="quantitative"),
            color=alt.Color('Moods', scale=alt.Scale(domain=mood_list, range=mood_colors))
        )

        st.altair_chart(
            mood_counts_graph,
            use_container_width=True,
        )

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

    def mood_line_graph():
        mood_line_graph = pd.DataFrame(
            line_graph_frequencies,
            columns=mood_list
        )

        st.line_chart(mood_line_graph)

    with col0:
        mood_bar_graph()

    with col1:
        mood_pie_graph()

    mood_line_graph()

    # with col0:
    #     start_year = st.selectbox("Start Year", [2021, 2022])
    #     start_day = st.slider("Start Day", 0, 365)
    #     
    # with col1:
    #     end_year = st.selectbox("End Year", [2021, 2022])
    #     end_day = st.slider("End Day", 0, 365)


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
