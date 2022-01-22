import streamlit as st


def main():
    pages = {
        "Home": page_home,
        "Settings": page_settings,
    }

    if "page" not in st.session_state:
        st.session_state.update({
            # Default page
            "page": "Home",

            # Radio, selectbox and multiselect options
            "options": ["Hello", "Everyone", "Happy", "Streamlit-ing"],

            # Default widget values
            "text": "",
            "slider": 0,
            "checkbox": False,
            "radio": "Hello",
            "selectbox": "Hello",
            "multiselect": ["Hello", "Everyone"],
        })

    with st.sidebar:
        page = st.radio("Select your page", tuple(pages.keys()))

    pages[page]()


def page_home():
    st.write(f"""
    # Settings values
    - **Input**: {st.session_state.text}
    - **Slider**: `{st.session_state.slider}`
    - **Checkbox**: `{st.session_state.checkbox}`
    - **Radio**: {st.session_state.radio}
    - **Selectbox**: {st.session_state.selectbox}
    - **Multiselect**: {", ".join(st.session_state.multiselect)}
    """)


def page_settings():
    st.title("Change settings")

    st.text_input("Input", key="text")
    st.slider("Slider", 0, 10, key="slider")
    st.checkbox("Checkbox", key="checkbox")
    st.radio("Radio", st.session_state["options"], key="radio")
    st.selectbox("Selectbox", st.session_state["options"], key="selectbox")
    st.multiselect("Multiselect", st.session_state["options"], key="multiselect")


if __name__ == "__main__":
    main()
