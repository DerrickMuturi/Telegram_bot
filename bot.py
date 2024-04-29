import os
import telebot
import requests
import logging

BOT_TOKEN = os.environ.get('BOT_TOKEN') # GETTING TOKEN FROM ENVIRONMENT VARIABLES
bot = telebot.TeleBot(BOT_TOKEN) #CREATING A BOT INSTANCE FROM TELEBOT CLASS


# handle the incomeing /start / hello commands
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    logging.debug('Received start/hello command')
    bot.reply_to(message, 'Habari, how are you doing?')

# handle all incoming text message
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)




#using hororscope api 
def get_daily_horoscope(sign: str, day: str) -> dict:
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params ={"sign": sign, "data": day}
    response = requests.get(url, params)

    return response.json()

# Asks user for their zodiac signs
@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    logging.debug('received horoscope command')
    text = "What's your zodiac sign?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)


#ask for the day
def day_handler(message):
    logging.debug('received zodiac sign')
    sign  = message.text
    text = "What day do you want to know?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, or a date in format YYYY-MM-DD."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, fetch_horoscope, sign.capitalize()
    )

#fetch horoscope based on input
def fetch_horoscope(message, sign):
    logging.debug("Received day for scope")
    try:
        day = message.text
        horoscope = get_daily_horoscope(sign, day)
        data = horoscope["data"]
        horoscope_message = f'*Horoscope: * {data["horoscope_data"]}\\n*Sign: * {sign}\\n*Day:*  {data["date"]}'
        bot.send_message(message.chat.id, "Here's your horoscope!")
        bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")
    except Exception as e:
        print(f"Oops! An error ocurred: {e}")
        

# start the bot and keep it running
bot.infinity_polling()