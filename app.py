from slackbot.bot import Bot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

def main():
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Arbitrium Test').sheet1

    data = sheet.get_all_values()
    index = 1
    print(data[0])
    print(data[1])
    print(data[index][random.randint(0, len(data[index]) - 1)])

    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()
