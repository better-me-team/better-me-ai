from links import *
import random

class Resource:
    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url


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

    # random number between 0 and 4
    num = random.randint(0, 4)

    return Resource(resources[num][0], resources[num][1], resources[num][2])
