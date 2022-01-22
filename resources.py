import streamlit as st

st.title("RESOURCES TEST PAGE")

# generate three columns
col1, col2, col3 = st.columns(3)


# Generate a class of articles and resources
class Resource:
    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url

    # Generate a function to display the resource

p1 = Resource("Python", "Python is a programming language", "https://www.python.org/")
p2 = Resource("Streamlit", "Streamlit is a web application framework", "https://streamlit.io/")
p3 = Resource("Pandas", "Pandas is a data analysis library", "https://pandas.pydata.org/")


def display():
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

display()