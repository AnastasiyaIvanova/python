import telebot
import requests
import json
from snowballstemmer import RussianStemmer
# from nltk.stem.snowball import SnowballStemmer 
from telebot import types


url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20190802T184906Z.bfee2f9836fc5c5d.008b565919518289762b30ba21dc53c229137b2b%20'
url1 = 'https://api.thecatapi.com/v1/images/search'

bot = telebot.TeleBot('954730655:AAFzrEOjkDFddoGCBh_NBxTIKYUgRmQ1SSQ')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_sticker(message.chat.id, 'CAADAgADFAADNm7hDP_mhkgh4R8VFgQ')
    bot.send_message(message.chat.id, 'Введите /help')

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/translate':
        bot.send_message(message.from_user.id, "Введи текст")
        bot.register_next_step_handler(message, get_name)
    elif message.text == '/fun':
        keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard2.row('Рандомный котик')
        msg = bot.send_message(message.from_user.id, 'Нажми Рандомный котик', reply_markup=keyboard2)
        bot.register_next_step_handler(msg, get_cat)
    elif message.text == 'Рандомный котик':
        bot.register_next_step_handler(message, get_cat)
    elif message.text == '/stem':
        bot.send_message(message.from_user.id, "Введи текст на русском")
        bot.register_next_step_handler(message, get_stem)
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'Чтобы перевести текст введите /translate \nЧтобы развлечься введите /fun \nДля получения основания слова введите /stem')
    else:
        bot.send_message(message.from_user.id, 'Напиши /help')

def get_name(message):
    global textTrans
    textTrans = message.text

    keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard1.row('en-ru', 'ru-en')
    msg = bot.send_message(message.from_user.id, 'Выбери язык', reply_markup=keyboard1)
    bot.register_next_step_handler(msg, doTrans)

def doTrans(message):
    data = ({'text': textTrans, 'lang': message.text})
    res = requests.post(url, data = data)
    trans = json.loads(res.text)
    bot.send_message(message.from_user.id, trans['text'][0])

def get_cat(message):
    # headers["x-api-key"] = 
    res = requests.get(url1)
    cat = json.loads(res.text)
    
    picture = '<a href="' + cat[0]['url'] + '">kitty</a>'
    bot.send_message(message.from_user.id, picture, parse_mode="HTML")

def get_stem(message):
    

# stemmer = SnowballStemmer("russian") 
# stemmer.stem("Василий")

    bot.send_message(message.from_user.id, RussianStemmer().stemWord(message.text))

bot.polling(none_stop=True, interval=0)