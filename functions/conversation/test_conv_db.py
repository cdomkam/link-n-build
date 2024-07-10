import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../")

from conversation_db import set_conv
from database import get_uid
import requests
import dotenv

from google.auth.transport.requests import Request
from google.oauth2 import id_token

CURRENT_DIR=os.path.dirname(os.path.abspath(__file__)) + "/.."

dotenv.load_dotenv(dotenv_path="keys/keys.env")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CURRENT_DIR + os.environ["GEM_KEYS_FUNCTION"]

comments = [
    "What's a hobby or interest you have that not many people know about?",
    "If you could travel anywhere in the world, where would you go and why?",
    "What's the best book you've read recently, and what did you enjoy about it?",
    "What kind of music do you enjoy, and do you have a favorite song or artist?",
    "What's your favorite way to spend a weekend or a day off?",
    "Do you have any favorite movies or TV shows that you could watch over and over?",
    "What's one of the most memorable experiences you've ever had?",
    "If you could have dinner with any three people, dead or alive, who would they be and why?",
    "What's a personal goal or dream you're currently working towards?",
    "What's something you're passionate about and why does it matter to you?"
]

responses = [
    "Not many people know that I enjoy stargazing. I often take weekend trips out of the city to find the best spots for watching the night sky.",
    "I would love to travel to Japan. The blend of traditional culture and cutting-edge technology fascinates me, and I’m particularly interested in experiencing the local cuisine, visiting historical temples, and exploring the bustling cities like Tokyo and Kyoto.",
    "The best book I’ve read recently is 'Dune' by Frank Herbert. I enjoyed the intricate world-building, the complex characters, and the exploration of political and ecological themes that are still relevant today.",
    "I enjoy a variety of music genres, but I have a special fondness for indie pop. One of my favorite artists is Florence + The Machine, and my favorite song by them is 'Dog Days Are Over' because it’s uplifting and energizing.",
    "My favorite way to spend a weekend is to start with a morning run along the waterfront, followed by a visit to a local art exhibition. In the afternoon, I enjoy having a relaxed lunch with friends and spending some quiet time reading a good science fiction novel.",
    "I could watch 'Inception' over and over again because I love the mind-bending plot and stunning visuals. For TV shows, I’m a big fan of 'Black Mirror' for its thought-provoking take on technology and society.",
    "One of the most memorable experiences I’ve ever had was hiking the Inca Trail to Machu Picchu. The breathtaking landscapes, the sense of history, and the physical challenge made it an unforgettable adventure.",
    "I would love to have dinner with Steve Jobs, for his visionary approach to technology and design; Jane Goodall, for her groundbreaking work in primatology and conservation; and J.K. Rowling, to discuss her creative process and the impact of the Harry Potter series on literature and culture.",
    "I’m currently working towards becoming a Chief Marketing Officer (CMO). I’m focusing on expanding my leadership skills, gaining more experience in strategic planning, and building a strong professional network.",
    "I’m passionate about mentorship for young women in tech and marketing. It matters to me because I believe in empowering the next generation of female leaders and helping them navigate the challenges of the industry. I want to create opportunities for women to succeed and drive positive change in the tech world."
]

def get_id_token(function_url: str):
    # Generate a custom token for a specific UID
    auth_req = Request()
    token = id_token.fetch_id_token(auth_req, function_url)
    return token

def create_conv_data():
    '''
        Creates Conversation data in fireatore
    '''
      
    user_id = get_uid()
    for c, r in zip(comments, responses):
        conv_id = get_uid()
        data = {
            "user_id": user_id,
            "name": "Emily Johnson",
            "username":"eJohnson",
            "comment":c,
            "response":r,
            "conversation_id":conv_id
        }
        set_conv(data=data)
        ... 

def test_conv_batch():
    '''Test Conversation uploading in Batch'''
    function_url = "http://localhost:5001/gemini-team/us-central1/add_conversation_batch"
    data = {
        "user_id":"c1dbf4a1-b2af-4423-9c07-2d9a98806ff5",
        "comments":comments,
        "responses":responses
    }
    
    token = get_id_token(function_url = function_url)
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': 'application/json'
    }
    
    response = requests.post(function_url, headers=headers, json=data)
    
    if response.status_code == 200:
        print('function call succeeded:', response.json())
    else:
        print('function call failed:', response.text)
if __name__=="__main__":
    # create_conv_data()
    test_conv_batch()