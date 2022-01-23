from links import *
import random


class Resource:
    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url


class Support:
    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url


def choose_resources(mood, ammount):
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

    nums = set()
    while len(nums) < 3:
        nums.add(random.randint(0, 4))

    return [
        Resource(resources[num][0], resources[num][1], resources[num][2])
        for num in nums
    ]


def choose_support(num):
    supports = (
        ("Student Wellness Hub", "McGill offers mental health and wellness services to students.",
         "https://www.mcgill.ca/wellness-hub/"),
        ("Access Advisors", "An Access Advisor can help you navigate the services offered by the Student Wellness Hub.",
         "https://www.mcgill.ca/access-advisors/"),
        ("Counsellors", "At your first session, you'll be matched with a Counsellor who will work with you to better "
                        "understand the challenges that you're facing.",
         "https://www.mcgill.ca/wellness-hub/hub-clinical-services/hub-clinicians/counsellors#About"),
    )
    return Resource(supports[num][0], supports[num][1], supports[num][2])
