from random import random
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import requests
import json

from telebot.types import Message

import time
import threading
import telebot
from telebot import types
import time
from datetime import datetime
import schedule

bot_client = telebot.TeleBot(token='5700392822:AAFC9oLvp0-HmcbREdYEy7eEAo8rLaZEyy8')
ADMIN_CHAT_ID = 5700392822
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

client = gspread.authorize(creds)

sheet = client.open('API Python').sheet1

col_mat = sheet.col_values(1)
col_vid = sheet.col_values(2)
#print(col_vid)

@bot_client.message_handler(commands=['start'])
def start(message: Message):
    bot_client.send_message(message.chat.id, f'Привет, {str(message.chat.first_name)}!\n'
                                            'Я бот, который поможет тебе изучить программирование на языке Python.\n'
                                            'Напиши /help, если хочешь получить видео-лекции или материалы для изучения\n'
                                            'Напиши /begin, если хочешь, чтобы я напоминал тебе о продолжении обучения\n')

@bot_client.message_handler(commands=['help'])
def handle_start_help(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    # bot_client.send_message(message.chat.id, col_vid, reply_markup=keyboard)
    video_button = types.InlineKeyboardButton(text='Видео-Лекции', callback_data='Video')
    mat_button = types.InlineKeyboardButton(text='Дополнительные Материалы', callback_data='Material')
    keyboard.add(video_button, mat_button)
    bot_client.send_message(message.chat.id, 'Чтобы получить видео-лекции нажми на кнопку "Видео-Лекции".\n'
                                             'Чтобы получить дополнительные материалы нажми на кнопку "Дополнительные Материалы".\n', reply_markup=keyboard)

@bot_client.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'Video':
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                vid1_button = types.InlineKeyboardButton(text='Введение в Python', url=col_vid[1])
                vid2_button = types.InlineKeyboardButton(text='Установка среды разработки', url=col_vid[2])
                vid3_button = types.InlineKeyboardButton(text='Базовые операции в языке Python', url=col_vid[3])
                vid4_button = types.InlineKeyboardButton(text='Переменные и типы данных', url=col_vid[4])
                vid5_button = types.InlineKeyboardButton(text='Условные операторы', url=col_vid[5])
                vid6_button = types.InlineKeyboardButton(text='Циклы и операторы в них (for, while)', url=col_vid[6])
                vid7_button = types.InlineKeyboardButton(text='Списки (list). Функции и их методы', url=col_vid[7])
                keyboard.add(vid1_button, vid2_button, vid3_button, vid4_button, vid5_button, vid6_button, vid7_button)
                bot_client.send_message(call.message.chat.id, 'Советую тебе смотреть видео-лекции по порядку, чтобы ты ни в чем не запутался\n'
                                                              'Удачи!\n', reply_markup=keyboard)
                #print(col_vid[3])
            elif call.data == 'Material':
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                mat1_button = types.InlineKeyboardButton(text='Онлайн компилятор Python', url=col_mat[1])
                mat2_button = types.InlineKeyboardButton(text='Самоучитель', url=col_mat[2])
                keyboard.add(mat1_button, mat2_button)
                bot_client.send_message(call.message.chat.id, 'Это материалы, которые тебе могут понадобится в процессе твоего обучения\n'
                                                              'Удачи!\n', reply_markup=keyboard)
            bot_client.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выбери, что тебе нужно.',reply_markup=None)
            bot_client.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                             text="Это твой выбор!")
    except Exception as e:
        print(repr(e))

@bot_client.message_handler(commands=['begin'])
def begin(message: Message):
    bot_client.send_message(message.chat.id, 'Настрой меня, чтобы я напоминал тебе о продолжении твоего обучения.')
    bot_client.send_message(message.chat.id, 'Введи время, в которое ты хочешь, чтобы я присылал уведомление.\n'
                                             'Например: 12:00, 03:00, 23:00\n')

@bot_client.message_handler(content_types=['text'])
def vremyapolzovatelya(message):
    vremya = message.text
    while True:
        now = datetime.now()
        now = str(now)
        timestrvalue = now[11:16]
        if timestrvalue == vremya:
            bot_client.send_message(message.chat.id, 'Пора повторить Python!')
            time.sleep(86200)
            continue



bot_client.polling(none_stop=True)




