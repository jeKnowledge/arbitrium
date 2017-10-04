from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from oauth2client.service_account import ServiceAccountCredentials
import os
from urllib.request import FancyURLopener
import re
import json
import gspread
import random
import time
import slackbot_settings


class MyOpener(FancyURLopener):
    version = 'My new User-Agent'


@listen_to('take me drunk im home', re.IGNORECASE)
def restaurante(message):
    message.react('beer')
    res = get_random(0)
    process(res)


@listen_to('jeK fit?', re.IGNORECASE)
def atividade(message):
    message.react('runner')
    res = get_random(1)
    process(res)


@listen_to('jeK fat?', re.IGNORECASE)
def restaurante(message):
    message.react('fork_and_knife')
    res = get_random(2)
    process(res)


@listen_to('Movie pls', re.IGNORECASE)
def movie(message):
    #message.react('clapper')
    myopener = MyOpener()
    movies = myopener.open("https://api.themoviedb.org/3/movie/top_rated?api_key=c8b4056e98d6d3065ed391c8dc1832a2&language=en-US&page=1").read().decode('utf8')
    movies = json.loads(movies)["results"]
    random_numbers = get_random_numbers(19)
    process([movies[random_numbers[0]]["title"], movies[random_numbers[1]]["title"], movies[random_numbers[2]]["title"]])


def get_random(index):
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Arbitrium Test').sheet1
    data = sheet.get_all_values()
    while '' in data[index]:
        data[index].remove('')
    random_numbers = get_random_numbers(len(data[index]) - 1)
    res = [data[index][random_numbers[0]], data[index][random_numbers[1]], data[index][random_numbers[2]]]
    return res


def process(res):
    post_message_as_slackbot("React to choose!! @channel", 0)
    first_ts = post_message_as_slackbot(res[0], 1)
    second_ts = post_message_as_slackbot(res[1], 1)
    third_ts = post_message_as_slackbot(res[2], 1)
    time.sleep(30)

    activities_indexes = get_most_voted([get_number_of_reactions(first_ts), get_number_of_reactions(second_ts), get_number_of_reactions(third_ts)])
    if len(activities_indexes) == 0:
        post_message_as_slackbot("You didn't vote. Shame. I choose " + res[random.randint(0, 2)], 0)

    elif len(activities_indexes) == 1:
        post_message_as_slackbot("The most voted option was " + res[activities_indexes[0]], 0)

    else:
        text = res[activities_indexes[0]]
        for i in range(1, len(activities_indexes)):
            text += " and " + res[activities_indexes[i]]
        random_choice = res[activities_indexes[random.randint(0, len(activities_indexes) - 1)]]
        post_message_as_slackbot("TIE between " + text + ". So I choose: " + random_choice, 0)


def get_random_numbers(limit):
    numbers = []
    while len(numbers) != 3:
        number = random.randint(0, limit)
        if number not in numbers:
            numbers.append(number)
    return numbers


def post_message_as_slackbot(message, return_ts):
    myopener = MyOpener()
    message_sent = myopener.open("http://slack.com/api/chat.postMessage?token=" + slackbot_settings.API_TOKEN + "&channel=C7AULM2BW&text=" + message + "&as_user=true").read()
    if return_ts:
        timestamp = json.loads(message_sent.decode('utf8'))["message"]["ts"]
        return timestamp


def get_number_of_reactions(timestamp):
    myopener = MyOpener()
    message_sent = myopener.open("https://slack.com/api/reactions.get?token=" + slackbot_settings.API_TOKEN + "&channel=C7AULM2BW&timestamp=" + timestamp + "&pretty=1").read()
    try:
        reactions = json.loads(message_sent.decode('utf8'))["message"]["reactions"]
        number_of_reactions = 0
        for i in range(len(reactions)):
            number_of_reactions += reactions[i]["count"]
        return number_of_reactions
    except:
        return 0


def get_most_voted(options):
    maximum_votes = 1
    most_voted_options = []
    for i in range(len(options)):
        if options[i] > maximum_votes:
            maximum_votes = options[i]
            most_voted_options = [i]
        elif options[i] == maximum_votes:
            most_voted_options.append(i)
    return most_voted_options


def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
