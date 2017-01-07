# -*- coding: utf-8 -*-
import config
import telebot
import json
import requests
import urllib
import random
import time
import datetime
from dbhelper import DBHelper
from apscheduler.schedulers.background import BackgroundScheduler


bot = telebot.TeleBot(config.token)
db = DBHelper()
reminder_scheduler = BackgroundScheduler()
reminder_scheduler.start()


def random_time():
    return random.randrange(48, 72, 4)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    text = "YO i’m willdo\nsometimes i write about things you’d like to complete instead of sitting in telegram"
    bot.send_message(message.chat.id, text)
    start_time = datetime.datetime.now() + datetime.timedelta(hours=random_time())
    reminder_scheduler.add_job(remind, 'cron', hour=str(random_time()), args=[message.chat.id], next_run_time=start_time)


@bot.message_handler(commands=['yo'])
def list_everything(message):
    items = db.get_items(message.chat.id)
    text = "\n".join(items)
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def repeat_all_messages(message):
    text = message.text
    chat_id = message.chat.id
    items = db.get_items(chat_id)
    if text in items:
        db.delete_item(text, chat_id)
        bot.send_message(message.chat.id, "yo " + text + "\n" + "CHECK")
    else:
        db.add_item(text, chat_id)
        items = db.get_items(chat_id)
        text = "\n".join(items)
        bot.send_message(message.chat.id, text + "\n" + "IN THE LIST")


# Handles all other formats
@bot.message_handler(content_types=['document', 'audio', 'photo', 'sticker', 'video', 'voice', 'location', 'contact', 'new_chat_member', 'left_chat_member', 'pinned_message'])
def handle_the_rest(message):
    bot.reply_to(message, "yo i understand plain dumb text only")


# Handles all text messages that match the regular expression
@bot.message_handler(regexp="SOME_REGEXP")
def handle_message(message):
    bot.reply_to(message, "yo i understand plain dumb text only")


def remind(chat_id):
    items = db.get_items(chat_id)
    item = random.choice(items)
    additional_text = "by the way, someone wanted to "
    text = additional_text + item
    bot.send_message(chat_id, text)
    # reminder_scheduler.add_job(remind, 'cron', hour=str(random_time()), replace_existing=True, args=[chat_id])


if __name__ == '__main__':
    db.setup()
    bot.polling(none_stop=True)