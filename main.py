#this file is responsible for bot operation (commands, scheduled delivery of message)

import reddit
import telebot
import os
import schedule
from replit import db
from threading import Thread
from time import sleep
from keep_alive import keep_alive

teleToken = os.environ['TOKEN']
bot = telebot.TeleBot(teleToken)

#qotd = reddit.get_qotd() + "\n\n" + reddit.qotd_trans()
print(reddit.get_qotd() + "\n\n" + reddit.qotd_trans())


def schedule_checker():
    while True:
      schedule.run_pending()
      sleep(1)
      
def send_vopros():
  for chatName in db.keys():
    try:
      bot.send_message(db[chatName], reddit.get_qotd())# + "\n\n" + reddit.qotd_trans())
    except:
      pass

schedule.every().day.at("09:00").do(send_vopros) #replit timezone -3 from mine

Thread(target=schedule_checker).start() 
keep_alive()

@bot.message_handler(commands=['start'])
def start(message):
  chat_name = str(message.chat.title)
  if chat_name not in db.keys():
    db[chat_name] = message.chat.id
    bot.send_message(message.chat.id, "Чат добавлен в рассылку")
  else:
    bot.send_message(message.chat.id, "Уже выполнено")

@bot.message_handler(commands=['stop'])
def stop(message):
  chat_name = str(message.chat.title)
  if chat_name in db.keys():
    del db[chat_name]
    bot.send_message(message.chat.id, "Чат убран из рассылки")
  else:
    bot.send_message(message.chat.id, "Чат не в рассылке")

@bot.message_handler(commands=['help'])
def help(message):
  bot.send_message(message.chat.id, "Каждый день я буду задавать вопрос с \nr/AskReddit\nКоманды:\n/start - добавить чат в рассылку вопроса дня.\n/vopros - показать вопрос дня.\n/help - показать это сообщение.")

@bot.message_handler(commands=['vopros'])
def vopros(message):
  #bot.send_message(message.chat.id, reddit.get_qotd() + "\n\n" + reddit.qotd_trans()) это с переводом
  bot.send_message(message.chat.id, reddit.get_qotd())

@bot.message_handler(content_types=['text'])
def pizda(message):
  if message.text.lower() == "да":
    bot.reply_to(message, "Пизда")
    
  


bot.polling(none_stop=True, interval=0)



#sometimes replit autoupdates packages and installs wrong package, this is fix:
#pip3 uninstall telebot
#pip3 uninstall PyTelegramBotAPI
#pip3 install pyTelegramBotAPI
#pip3 install --upgrade pyTelegramBotAPI

#pip install googletrans==4.0.0-rc1