import telebot
from telebot import types
import os
import random 
import time

bot = telebot.TeleBot("1543078251:AAHCkuKqo_0cjDUJe-AxS5mK7ViTukwCeLY")
if not os.path.exists('voice/'):
    os.makedirs('voice/')

markup = types.ReplyKeyboardMarkup(row_width=1)
itembtn1 = types.KeyboardButton('👨🏼‍💻 Начать обучение')
itembtn2 = types.KeyboardButton('👨🏾‍🏫 Начать изучение')
markup.add(itembtn1, itembtn2)

stopmarkup = types.ReplyKeyboardMarkup(row_width=1)
stopbtn = types.KeyboardButton('🛑 Stop')
stopmarkup.add(stopbtn)

clientsWord = {}
clientsStopStatus = {}

imageList = ['а.jpg','б.jpg','в.jpg','г.jpg','д.jpg','е.jpg','ё.jpg','ж.jpg','з.jpg','и.jpg','й.jpg','к.jpg','л.jpg','м.jpg','н.jpg','о.jpg','п.jpg','р.jpg','с.jpg','т.jpg','у.jpg','ф.jpg','х.jpg','ц.jpg','ч.jpg', 'ш.jpg' , 'щ.jpg', 'ъ.jpg','ы.jpg','ь.jpg','э.jpg','ю.jpg','я.jpg']
voiceList = ['а.ogg','б.ogg','в.ogg','г.ogg','д.ogg','е.ogg','ё.ogg','ж.ogg','з.ogg','и.ogg','й.ogg','к.ogg','л.ogg','м.ogg','н.ogg','о.ogg','п.ogg','р.ogg','с.ogg','т.ogg','у.ogg','ф.ogg','х.ogg','ц.ogg','ч.ogg','ш.ogg','щ.ogg','ъ.ogg','ы.ogg','ь.ogg','э.ogg','ю.ogg','я.ogg']
alphabet = ['а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я']
# current_number = 30

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    global clientsWord, clientsStopStatus

    clientsWord[chat_id] = 0
    clientsStopStatus[chat_id] = 0

    if not os.path.exists('voice/' + str(chat_id)):
        os.makedirs('voice/' + str(chat_id))

    start_msg = """Этот бот научит вашего ребенка алфавиту
Начать изучение - бот начнет присылать картинку буквы и голос.
Начать обучение - бот запомнит ваши голосовые сообщения."""

    bot.send_message(chat_id, start_msg  ,reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    chat_id = message.chat.id
    global clientsWord, clientsStopStatus

    if message.text == '👨🏾‍🏫 Начать изучение':
        if not os.path.exists('voice/' + str(chat_id) + '/а.ogg'):
            bot.send_message(chat_id, "У вас нет записей, начните обучение бота.", reply_markup=markup)
            return

        for i in range(33):
            if clientsStopStatus[chat_id] == 0:
                photo = open('words/' + imageList[i], 'rb')
                bot.send_photo(chat_id, photo)
                time.sleep(1)

                audio = open('voice/' + str(chat_id) + '/' + voiceList[i], 'rb')
                bot.send_voice(chat_id, audio, reply_markup=stopmarkup)
                time.sleep(5)
                
                clientsWord[chat_id] += 1
            else:
                clientsStopStatus[chat_id] = 0
                break

    elif message.text == '👨🏼‍💻 Начать обучение':
        bot.send_message(chat_id, 'A', reply_markup=types.ReplyKeyboardRemove(selective=False))
        clientsWord[chat_id] = 0

    elif message.text == '🛑 Stop':
        clientsStopStatus[chat_id] = 1
        bot.send_message(chat_id, 'Есть стоп', reply_markup=markup)
        
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    chat_id = message.chat.id
    global clientsWord
    
    if clientsWord[chat_id] <= 31:
        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open('voice/' + str(chat_id) + '/' + voiceList[clientsWord[chat_id]],'wb') as new_file:
            new_file.write(downloaded_file)

        clientsWord[chat_id] += 1
        bot.send_message(chat_id, alphabet[clientsWord[chat_id]].upper())
    else:
        endmsg = 'Бот сохранил ваш голосовой алфавит.'
        bot.send_message(chat_id, endmsg, reply_markup=markup)

bot.polling()