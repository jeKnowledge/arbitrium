import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_TOKEN = os.environ.get("API_TOKEN")
DEFAULT_REPLY = "Sorry but I didn't understand you"
PLUGINS = [
    'slackbot.plugins',
]

HELP_TRIGGER = 'help'
HELP_MESSAGE = "WRITE\ntake me drunk im home - restaurants for parties\njeK fit? - activities for make jeK fit\njeK fat? - restaurants for make jeK dat\nmovie? - movies from spread\nbest movies pls - best movies today\nThen you have an hour to vote. I will say who won."

MESSAGES = [
    ['take me drunk im home', 'beer', 0],
    ['jeK fit?', 'runner', 1],
    ['jeK fat?', 'fork_and_knife', 2],
    ['movie?', 'clapper', 3]
]

BEST_MOVIES_MESSAGE = 'best movies pls'
