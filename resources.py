import streamlit as st

# ==========[ PAGE STRUCTURE ]========== #
st.title("RESOURCES TEST PAGE")
# generate three columns
col1, col2, col3 = st.columns(3)

# Generate a class of articles and resources
class Resource:
    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url

# anger, fear, joy, love, sadness, surprise
anger_resources = (
    ("Happify", "Happify is a web application that helps you manage your mental health", "https://happify.io/"),
    ("How to Meditate", "How to Meditate is a website that teaches you how to meditate",
     "https://www.mindful.org/how-to-meditate/"),
    ("Running", "Running can lift your mood and help you feel more equipped to confront your anger",
     "https://www.self.com/story/rage-run"),
    ("Meditation", "Meditation can help you feel more calm and relaxed", "https://www.mindful.org/meditation/"),
    ("Anger Management Methods", "Anger Management Methods is a website that teaches you how to manage your anger",
     "https://www.self.com/article/anger-management-methods"),
)

fear_resources = (
    ("How to overcome fear and anxiety",
     "How to overcome fear and anxiety is a website that teaches you how to overcome fear and anxiety",
     "https://www.nhsinform.scot/healthy-living/mental-wellbeing/fears-and-phobias/ten-ways-to-fight-your-fears"),
    ("Breathign techniques", "Try these breathing techniques to calm your mind",
     "https://www.mentalhealth.org.uk/publications/overcome-fear-anxiety"),
    ("Overcome fear", "Here are 5 ways to overcome fear and setbacks",
     "https://www.tonyrobbins.com/stories/unleash-the-power/overcoming-fear-in-5-steps/"),
    ("14 ways to overcome fear", "14 ways to overcome fear",
     "https://www.forbes.com/sites/joshsteimle/2016/01/04/14-ways-to-conquer-fear/"),
)

joy_resources = (
    ("How to be happy", "How to be happy is a website that teaches you how to be happy",
     "https://www.self.com/article/how-to-be-happy"),

)

love_resources = (


)

sadness_resources = (

)

surprise_resources = (

)


def choose_resources(mood):

    # choose a random resource from the list of resources
    if mood == "anger":
        resources = anger_resources
    elif mood == "fear":
        resources = fear_resources
    elif mood == "joy":
        resources = joy_resources
    elif mood == "love":
        resources = love_resources
    elif mood == "sadness":
        resources = sadness_resources
    elif mood == "surprise":
        resources = surprise_resources

    global p1, p2, p3
    p1 = Resource(resources[0][0], resources[0][1], resources[0][2])
    p2 = Resource(resources[1][0], resources[1][1], resources[1][2])
    p3 = Resource(resources[2][0], resources[2][1], resources[2][2])


def display_resources():
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


if __name__ == '__main__':
    choose_resources("fear")
    display_resources()
