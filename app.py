from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from oauth2client.service_account import ServiceAccountCredentials
import urllib.request
import re
import json
import gspread
import random


@listen_to('take me drunk im home', re.IGNORECASE)
def restaurante(message):
    res = get_random(0)
    message.reply(res[0])
    message.reply(res[1])
    message.reply(res[2])
    message.react('beer')


@listen_to('jeK fit?', re.IGNORECASE)
def atividade(message):
    res = get_random(1)
    message.reply(res[0])
    message.reply(res[1])
    message.reply(res[2])
    message.react('runner')


@listen_to('jeK fat?', re.IGNORECASE)
def restaurante(message):
    res = get_random(2)
    message.reply(res[0])
    message.reply(res[1])
    message.reply(res[2])
    message.react('fork_and_knife')


@listen_to('Movie pls', re.IGNORECASE)
def movie(message):
    movies = urllib.request.urlopen("https://api.themoviedb.org/3/movie/top_rated?api_key=c8b4056e98d6d3065ed391c8dc1832a2&language=en-US&page=1").read().decode('utf8')
    movies = json.loads(movies)["results"]
    random_numbers = get_random_numbers(19)
    message.reply(movies[random_numbers[0]]["title"])
    message.reply(movies[random_numbers[1]]["title"])
    message.reply(movies[random_numbers[2]]["title"])
    message.react('clapper')


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


def get_random_numbers(limit):
    numbers = []
    while len(numbers) != 3:
        number = random.randint(0, limit)
        if number not in numbers:
            numbers.append(number)
    return numbers


def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
