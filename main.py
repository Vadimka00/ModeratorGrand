import telebot
from telebot import types
from telebot import TeleBot
import sqlite3
from datetime import datetime  # Для записи времени
import sys
import schedule
import time
import threading
import json
from random import choice
import requests
import logging
import re
import emoji
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os, sys
from requests.exceptions import ConnectionError, ReadTimeout
import random
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

bot = telebot.TeleBot("6971843804:AAHe5i1mA2j5cRSrCoJnG8UyBEpxBCYjX6k")

# Создаем пул потоков
executor = ThreadPoolExecutor(max_workers=500)

# Определение путей к базам данных
db_paths = {
    "active_chats.db": "/app/dbs/active_chats.db",
    "ad.db": "/app/dbs/ad.db",
    "chat_data.db": "/app/dbs/chat_data.db",
    "database.db": "/app/dbs/database.db",
    "fuck.db": "/app/dbs/fuck.db",
    "good.db": "/app/dbs/good.db",
    "messages.db": "/app/dbs/messages.db",
    "rules.db": "/app/dbs/rules.db",
    "spam.db": "/app/dbs/spam.db",
}

def connect_to_db(db_name):
    """Подключение к базе данных по имени"""
    if db_name in db_paths:
        conn = sqlite3.connect(db_paths[db_name])
        return conn
    else:
        raise ValueError(f"Database '{db_name}' not found in paths")

allowed_users = [1858164732, 1720624205, 547955786, 1947291534, 5808500962]
prod_users = [1858164732, 5808500962]
# Функция для чтения файла JSON
def read_json_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Чтение данных из файла
data = read_json_file('text_language.json')
# Проверка, существует ли чат в базе данных active_chats.db
# Функция для сохранения сообщения в базе данных

def chat_exists(chat_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM active_chats WHERE recipient_id = ? OR sender_id = ?''', (chat_id, chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Функция для получения языка пользователя из базы данных
def get_user_language(chat_id):
    conn = connect_to_db('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM users WHERE user_id=?", (chat_id,))
    language = cursor.fetchone()
    conn.close()
    # Если язык не найден, устанавливаем значение по умолчанию 'rus'
    if language is None:
        return 'en'
    else:
        return language[0]

# Обработчик команды "/start" - начало
@bot.message_handler(commands=['start'])
def start(message):
    print("Получена команда /start")  # Добавляем вывод в консоль для отслеживания выполнения команды

    # Проверка, что сообщение отправлено в личном чате
    if message.chat.type != "private":
        print("Команда /start не была отправлена в личном чате, игнорируем")  # Добавляем вывод в консоль
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    print("Чат ID:", chat_id)  # Добавляем вывод в консоль для отслеживания чат ID
    print("ID пользователя:", user_id)  # Добавляем вывод в консоль для отслеживания ID пользователя

    # Проверяем, существует ли пользователь в базе данных active_chats.db
    if chat_exists(chat_id):
        print("Пользователь уже существует")  # Добавляем вывод в консоль

    print("Подключаемся к базе данных и выполняем начальные действия...")  # Добавляем вывод в консоль

    # Подключаемся к базе данных SQLite и выполняем начальные действия
    connection, cursor, user = initialize_database(user_id)

    if user:
        language = user[1]
        prefix = user[2]
        if prefix is None:
            send_prefix_buttons(language, chat_id)
        else:
            start_text = data['start_text'][language]['1']
            start_text += data['start_text'][language]['2']
            start_text += data['start_text'][language]['3']
            start_text += data['start_text'][language]['4']
            start_text += data['start_text'][language]['5']
            start_text += data['start_text'][language]['6']
            start_text += data['start_text'][language]['7']
            start_text += data['start_text'][language]['8']
            start_text += data['start_text'][language]['9']
            start_text += data['start_text'][language]['10']
            send_buttons(chat_id, language, start_text, user_id)
    else:
        language_text = data['language_text']['1'] + "\n\n" + data['language_text']['2']
        send_language_selection(chat_id, language_text)
        print("Новый пользователь")  # Добавляем вывод в консоль

    cursor.close()
    connection.close()

    print("Обработка команды /start завершена\n")  # Добавляем вывод в консоль для отслеживания завершения обработки


@bot.message_handler(func=lambda message: message.text.startswith('/start GRANDMain'), content_types=['text'])
def start_param(message):
    # Проверка, что сообщение отправлено в личном чате
    if message.chat.type != "private":
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    # Проверяем, существует ли пользователь в базе данных active_chats.db
    if chat_exists(chat_id):
        print("Пользователь уже существует")

    # Подключаемся к базе данных SQLite и выполняем начальные действия
    connection, cursor, user = initialize_database(user_id)

    if user:
        language = user[1]
        prefix = user[2]
        if prefix is None:
            send_prefix_buttons(language, chat_id)
        else:
            start_text = data['start_text'][language]['1']
            start_text += data['start_text'][language]['2']
            start_text += data['start_text'][language]['3']
            start_text += data['start_text'][language]['4']
            start_text += data['start_text'][language]['5']
            start_text += data['start_text'][language]['6']
            start_text += data['start_text'][language]['7']
            start_text += data['start_text'][language]['8']
            start_text += data['start_text'][language]['9']
            start_text += data['start_text'][language]['10']
            send_buttons(chat_id, language, start_text, user_id)
    else:
        language_text = data['language_text']['1'] + "\n\n" + data['language_text']['2']
        send_language_selection(chat_id, language_text)
        print(f"[{datetime.now()}] Новый пользователь)")

    cursor.close()
    connection.close()


    # Функция для подключения к базе данных /start
def initialize_database(user_id):
    connection = connect_to_db('database.db')
    cursor = connection.cursor()

    # Создаем таблицу users, если её нет
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (user_id INTEGER PRIMARY KEY, language TEXT, prefix TEXT DEFAULT NULL)''')

    # Проверяем, есть ли пользователь уже в базе
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    return connection, cursor, user
# Обработчик команды "/start" - конец

# Обработчик установки префикса - начало
def send_prefix_buttons(language, chat_id):
    prefix_text = data['prefix_text'][language]['1']
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if language == "rus":
        p_yes_button = types.KeyboardButton("Да! 🎉")
        p_no_button = types.KeyboardButton("Нет. 😕")
    else: 
        p_yes_button = types.KeyboardButton("Yeah! 🎉")
        p_no_button = types.KeyboardButton("Nope. 😕")
    keyboard.add(p_no_button, p_yes_button)
    bot.send_message(chat_id, prefix_text, reply_markup=keyboard)

# Функция для обновления префикса пользователя в базе данных
def update_user_prefix(user_id, prefix):
    # Подключаемся к базе данных SQLite
    connection = connect_to_db('database.db')
    cursor = connection.cursor()

    try:
        # Обновляем префикс в базе данных
        cursor.execute("UPDATE users SET prefix = ? WHERE user_id = ?", (prefix, user_id))
        connection.commit()
        print(f"[{datetime.now()}] Новый префикс у ID {user_id} Выбранный: {prefix}")

        # Получаем язык пользователя
        cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
        language_stats = cursor.fetchone()
        language = language_stats[0] if language_stats else None
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении префикса: {e}")
        language = None
    finally:
        cursor.close()
        connection.close()

    return language

# Функция для обновления префикса чата, созданного указанным пользователем
def update_chat_prefix(user_id, prefix):
    # Подключаемся к базе данных SQLite
    connection = connect_to_db('chat_data.db')
    cursor = connection.cursor()

    try:
        # Обновляем префикс в таблице chats
        cursor.execute("UPDATE chats SET prefix = ? WHERE creator_id = ?", (prefix, user_id))
        connection.commit()
        print(f"Префикс в чатах, созданных пользователем {user_id}, обновлен: {prefix}")
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении префикса в таблице chats: {e}")
    finally:
        cursor.close()
        connection.close()

# Обработчик нажатия кнопок "Да! 🎉" или "Нет. 😕"
@bot.message_handler(func=lambda message: message.text in ["Да! 🎉", "Yeah! 🎉", "Нет. 😕", "Nope. 😕"])
def stats_button_handler(message):
    # Проверка, что сообщение отправлено в личном чате с ботом
    if message.chat.type == "private":
        chat_id = message.chat.id
        user_id = message.from_user.id

        # Определение значения префикса в зависимости от выбранной кнопки
        prefix = "grand" if message.text in ["Да! 🎉", "Yeah! 🎉"] else "free"

        # Обновляем префикс пользователя и получаем его язык
        language = update_user_prefix(user_id, prefix)
        update_chat_prefix(user_id, prefix)

        if language:
            # Формируем текст стартового сообщения
            start_text = data['start_text'][language]['1']
            start_text += data['start_text'][language]['2']
            start_text += data['start_text'][language]['3']
            start_text += data['start_text'][language]['4']
            start_text += data['start_text'][language]['5']
            start_text += data['start_text'][language]['6']
            start_text += data['start_text'][language]['7']
            start_text += data['start_text'][language]['8']
            start_text += data['start_text'][language]['9']
            start_text += data['start_text'][language]['10']

            # Отправляем сообщение с кнопками
            send_buttons(chat_id, language, start_text, user_id)

# Обработчик установки префикса - конец

def send_buttons(chat_id, language, text, user_id):
    connection, cursor, user = initialize_database(chat_id)
    prefix = user[2]
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    if prefix is None:
            send_prefix_buttons(language, chat_id)
    else:
        if language == 'rus':
            stats_button = types.KeyboardButton("📊 Профиль")
            referrals_button = types.KeyboardButton("💎 Награда")
            language_ru_button = types.KeyboardButton("🌎 Язык")
            settings_ru_button = types.KeyboardButton("⚙️ Настройки")
            support_ru_button = types.KeyboardButton("🛠 Помощь")
            grand_ru_button = types.KeyboardButton("💠 G-бонус")
            keyboard.add(stats_button, referrals_button, language_ru_button, settings_ru_button, support_ru_button, grand_ru_button)
            if prefix == "free":
                sotrud_button = types.KeyboardButton("📢 Сотрудничество")
                keyboard.add(sotrud_button)            
            # Если пользователь имеет права администратора
            if user_id in allowed_users:
                bd_button = types.KeyboardButton("🌐 База")
                staff_commands_button = types.KeyboardButton("📝 Команды")
                info_button = types.KeyboardButton("👁‍🗨 Info")
                if user_id in prod_users:
                    ad_button = types.KeyboardButton("📢 Реклама")
                    keyboard.add(bd_button, staff_commands_button, info_button, ad_button)
                else:
                    keyboard.add(bd_button, staff_commands_button, info_button)
            bot.send_message(chat_id, text, reply_markup=keyboard)
        elif language == 'en':
            keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
            stats_button = types.KeyboardButton("📊 Statistics")
            referrals_button = types.KeyboardButton("💎 Rewards")
            language_en_button = types.KeyboardButton("🌎 Language")
            settings_en_button = types.KeyboardButton("⚙️ Settings")
            support_en_button = types.KeyboardButton("🛠 Support")
            grand_en_button = types.KeyboardButton("💠 G-bonus")
            keyboard.add(stats_button, referrals_button, language_en_button, settings_en_button, support_en_button, grand_en_button)

            # Если пользователь имеет права администратора
            if user_id in allowed_users:
                bd_button = types.KeyboardButton("🌐 База")
                staff_commands_button = types.KeyboardButton("📝 Команды")
                info_button = types.KeyboardButton("👁‍🗨 Info")
                if user_id in prod_users:
                    ad_button = types.KeyboardButton("📢 Реклама")
                    keyboard.add(bd_button, staff_commands_button, info_button, ad_button)
                else:
                    keyboard.add(bd_button, staff_commands_button, info_button)
            bot.send_message(chat_id, text, reply_markup=keyboard)

# Обработчик выбора языка - начало
def send_language_selection(chat_id, language_text):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    ru_button = types.KeyboardButton("🇷🇺 Русский")
    us_button = types.KeyboardButton("🇺🇸 English")
    keyboard.add(ru_button, us_button)

    bot.send_message(chat_id, language_text, reply_markup=keyboard)        

@bot.message_handler(func=lambda message: message.text == "🇷🇺 Русский")
def stats_button_handler(message):
    # Проверка, что сообщение отправлено в личном чате с ботом
    if message.chat.type == "private":
        chat_id = message.chat.id
        user_id = message.from_user.id
        language = "rus"
        # Подключаемся к базе данных SQLite
        connection = connect_to_db('database.db')
        cursor = connection.cursor()

        # Создаем таблицу users, если её нет
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                        (user_id INTEGER PRIMARY KEY, language TEXT, prefix TEXT DEFAULT NULL)''')

        print(f"[{datetime.now()}] Таблица 'users' создана (если не существовала)")

        # Проверяем, есть ли пользователь уже в базе
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            # Если у пользователя уже есть выбранный язык и он не "rus", обновляем его на "rus"
            if user[1] != 'rus':
                cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
                connection.commit()
            text = data['language_text']['rus']
            print(f"[{datetime.now()}] Успешная активация пользователя с ID {user_id}. Язык обновлен: rus")
        else:
            # Добавляем нового пользователя в базу
            cursor.execute("INSERT INTO users (user_id, language) VALUES (?, ?)", (user_id, 'rus'))
            connection.commit()
            text = data['start_text'][language]['1']
            text += data['start_text'][language]['2']
            text += data['start_text'][language]['3']
            text += data['start_text'][language]['4']
            text += data['start_text'][language]['5']
            text += data['start_text'][language]['6']
            text += data['start_text'][language]['7']
            text += data['start_text'][language]['8']
            text += data['start_text'][language]['9']
            text += data['start_text'][language]['10']
            print(f"[{datetime.now()}] Новый пользователь с ID {user_id}. Выбранный язык: rus")
        send_buttons(chat_id, language, text, user_id)

        cursor.close()
        connection.close()

@bot.message_handler(func=lambda message: message.text == "🇺🇸 English")
def stats_button_handler(message):
    # Проверка, что сообщение отправлено в личном чате с ботом
    if message.chat.type == "private":
        chat_id = message.chat.id
        user_id = message.from_user.id
        language = "en"
        # Подключаемся к базе данных SQLite
        connection = connect_to_db('database.db')
        cursor = connection.cursor()

        # Создаем таблицу users, если её нет
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                        (user_id INTEGER PRIMARY KEY, language TEXT, prefix TEXT DEFAULT NULL)''')

        print(f"[{datetime.now()}] Таблица 'users' создана (если не существовала)")

        # Проверяем, есть ли пользователь уже в базе
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            # Если у пользователя уже есть выбранный язык и он не "rus", обновляем его на "rus"
            if user[1] != 'en':
                cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (language, user_id))
                connection.commit()
            text = data['language_text']['en']
            print(f"[{datetime.now()}] Успешная активация пользователя с ID {user_id}. Язык обновлен: en")
        else:
            # Добавляем нового пользователя в базу
            cursor.execute("INSERT INTO users (user_id, language) VALUES (?, ?)", (user_id, 'en'))
            connection.commit()
            text = data['start_text'][language]['1']
            text += data['start_text'][language]['2']
            text += data['start_text'][language]['3']
            text += data['start_text'][language]['4']
            text += data['start_text'][language]['5']
            text += data['start_text'][language]['6']
            text += data['start_text'][language]['7']
            text += data['start_text'][language]['8']
            text += data['start_text'][language]['9']
            text += data['start_text'][language]['10']
            print(f"[{datetime.now()}] Новый пользователь с ID {user_id}. Выбранный язык: en")
        send_buttons(chat_id, language, text, user_id)
        cursor.close()
        connection.close()


@bot.message_handler(func=lambda message: message.text in ["🌎 Язык", "🌎 Language"])
def language_buttons_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            user_language = get_user_language(chat_id)
            if user_language == "en":
                text = data['language_text']['2']
            else:
                text = data['language_text']['1']
            send_language_selection(chat_id, text)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'Язык':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{message.from_user.username if message.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

        
# Обработчик выбора языка при первом запуске  - конец

# Обработчик STAFF-команд - начало

# Функция для получения информации из базы данных по chat_id
def get_chat_info(chat_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM chats WHERE chat_id=?", (chat_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        conn.close()
        raise e

#Функция получения id по username в чате
def get_user_by_username(username):
    conn = connect_db()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_username = ?", (username, ))
        result = cursor.fetchone()
        if result:
            return result[0]  # Возвращаем ID пользователя
        else:
            return None
    except Exception as e:
        print(f"Error getting user ID by username: {e}")
        return None
    finally:
        conn.close()

# Функция для отображения инлайн-клавиатуры с кнопками групп
def show_user_group_buttons(chat_id):
    try:
        conn, cursor = create_connection()
        cursor.execute("SELECT DISTINCT chat_id, chat_name FROM users WHERE user_id=?", (chat_id,))
        groups = cursor.fetchall()
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton("Вся статистика", callback_data=f"all_user_stats__{chat_id}"))
        for group in groups:
            keyboard.row(types.InlineKeyboardButton(group[1], callback_data=f"groupuser_{group[0]}_{chat_id}"))
        conn.close()  # Закрытие соединения с базой данных
        return keyboard
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при отображение списка групп пользователя':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{chat_id.from_user.username if chat_id.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

# Обработчик нажатия на кнопки инлайн-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data.startswith(('groupuser_')))
def group_stats_callback(call):
    try:
        user_id = call.data.split("_")[-1]
        chat_id = call.data.split("_")[-2]
        button_pressed = call.data
        
        current_language = get_user_language(user_id)
        language = current_language

        group_id = int(call.data.replace('groupuser_', '').split('_')[0])
        conn, cursor = create_connection()
        cursor.execute("SELECT chat_name, SUM(message_count), SUM(bonus_count), SUM(word_count), SUM(warn_count) FROM users WHERE chat_id=? AND user_id=?", (group_id, user_id))
        group_stats = cursor.fetchone()
        if group_stats:
            group_stats_message = f"Статистика пользователя из <b>{group_stats[0]}</b>:\n\n💬 Всего сообщений: <b>{group_stats[1]}</b>\n💠 Всего бонусов: <b>{group_stats[2]}</b>\n📝 Всего слов: <b>{group_stats[3]}</b>\n⚠️ Всего предупреждений: <b>{group_stats[4]}</b>\n"
            keyboard = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton("⬅️ Назад", callback_data=f"back_profile_to_user_groups_{user_id}")
            keyboard.add(back_button)
            bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=group_stats_message, reply_markup=keyboard, parse_mode='HTML')
        else:
            bot.send_message(chat_id=call.from_user.id, text=f"Упс! У тебя еще нет статистики.🚀")

        conn.close()
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '{button_pressed}':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Кнопка: {button_pressed}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

# Обработчик нажатия на кнопки инлайн-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data.startswith(('all_user_stats_')))
def group_stats_callback(call):
    try:
        user_id = call.data.split("_")[-1]
        button_pressed = call.data
        
        current_language = get_user_language(user_id)
        language = current_language
        conn, cursor = create_connection()
        cursor.execute("SELECT SUM(message_count), SUM(bonus_count), SUM(word_count), SUM(warn_count) FROM users WHERE user_id=?", (user_id,))
        user_stats = cursor.fetchone()
        if user_stats:  # Если пользователь присутствует в группе
            total_stats_message = f"Общая статистика пользователя:\n\n💬 Всего сообщений: <b>{user_stats[0]}</b>\n💠 Всего GRAND бонусов: <b>{user_stats[1]}</b>\n📝 Всего слов: <b>{user_stats[2]}</b>\n⚠️ Всего предупреждений: <b>{user_stats[3]}</b>\n"
            keyboard = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton("⬅️ Назад", callback_data=f"back_profile_to_user_groups_{user_id}")
            keyboard.add(back_button)
            bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=total_stats_message, reply_markup=keyboard, parse_mode='HTML')
        else:
            bot.send_message(chat_id=call.from_user.id, text=f"Упс! У тебя еще нет статистики.🚀")

        conn.close()
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '{button_pressed}':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {user_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Кнопка: {button_pressed}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

# Обработчик нажатия на кнопки инлайн-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data.startswith(('back_profile_to_user_groups_')))
def group_stats_callback(call):
    try:
        user_id = call.data.split("_")[-1]
        language, prefix = get_prof_info(user_id)
        chat_rows = get_creators_info(user_id)
        username = get_username_info(user_id)
        if prefix == "grand":
            prefix_text = "💠"
        else:
            prefix_text = "◽️" 
        if language == "rus":
            language_text = "🇷🇺"
        else:
            language_text = "🇺🇸"
        if chat_rows:
            text = f"Статистика @{username} ({language_text}) ({prefix_text})\nСоздатель:\n"
            for chat_id, chat_name in chat_rows:
                text += f"<code>{chat_id}</code> ({chat_name})\n"
        else:
            text = f"Статистика @{username} ({language_text}) ({prefix_text})"
        keyboard = show_user_group_buttons(user_id)
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=keyboard, parse_mode="HTML")
    except Exception as e:
        error_message = (
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {user_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

# Функция для получения языка пользователя из базы данных
def get_username_info(user_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_username FROM users WHERE user_id=?", (user_id,))
    username = cursor.fetchone()  # Добавляем присвоение значений
    conn.close()
    return username[0]  # Возвращаем язык и префикс

# Функция для получения языка пользователя из базы данных
def get_creators_info(user_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id, chat_name FROM creators WHERE creator_id=?", (user_id,))
    creator_rows = cursor.fetchall()  # Fetch all rows
    conn.close()
    if creator_rows:
        return creator_rows
    else:
        return None

# Функция для получения языка пользователя из базы данных
def get_prof_info(user_id):
    conn = connect_to_db('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT language, prefix FROM users WHERE user_id=?", (user_id,))
    language, prefix = cursor.fetchone()  # Добавляем присвоение значений
    conn.close()
    return language, prefix  # Возвращаем язык и префикс

def null_update_users():
    # Подключение к базе данных
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    
    # Обновление всех значений в таблице users на 0
    cursor.execute('''UPDATE users
                      SET message_count = 0,
                          bonus_count = 0,
                          word_count = 0,
                          reactions_count = 0,
                          warn_count = 0''')
    
    # Сохранение изменений
    conn.commit()
    # Закрытие соединения
    conn.close()

def null_update_chats():
    # Подключение к базе данных
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    
    # Обновление всех значений в таблице users на 0
    cursor.execute('''UPDATE chats
                      SET message_count = 0,
                          bonus_count = 0,
                          word_count = 0,
                          reactions_count = 0,
                          warn_count = 0''')
    
    # Сохранение изменений
    conn.commit()
    # Закрытие соединения
    conn.close()

def null_update_creators():
    # Подключение к базе данных
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    
    # Обновление всех значений в таблице users на 0
    cursor.execute('''UPDATE creators
                      SET message_count = 0,
                          bonus_count = 0,
                          word_count = 0,
                          reactions_count = 0,
                          warn_count = 0''')
    
    # Сохранение изменений
    conn.commit()
    # Закрытие соединения
    conn.close()

# Обработчик команды /close
@bot.message_handler(commands=['update'])
def close_command(message):
    if message.from_user and message.from_user.id in allowed_users:
        null_update_users()
        null_update_chats()
        null_update_creators()
    else:
        bot.reply_to(message, "Недоступно для тебя")

# Обработчик команды /support
@bot.message_handler(commands=['support'])
def add_support_entry(message):
    if message.from_user and message.from_user.id in allowed_users:
        args = message.text.split()
        if len(args) != 3:
            bot.reply_to(message, "Подсказка: /support support_id @support_name")
            return

        support_id = args[1]
        support_name = args[2]

        # Подключение к базе данных
        conn = connect_to_db('chat_data.db')
        cursor = conn.cursor()

        # Создание таблицы support, если её ещё нет
        cursor.execute('''CREATE TABLE IF NOT EXISTS support
                        (support_id INTEGER PRIMARY KEY,
                        support_name TEXT,
                        support_balance INTEGER,
                        like INTEGER DEFAULT 0,
                        dislike INTEGER DEFAULT 0,
                        code TEXT)''')

        # Генерация кода
        code = generate_code()

        # Добавление новой записи
        cursor.execute("INSERT INTO support (support_id, support_name, support_balance, code) VALUES (?, ?, ?, ?)", (support_id, support_name, 0, code))

        # Сохранение изменений и закрытие соединения
        conn.commit()
        conn.close()

        # Отправка сообщения пользователю в личный чат
        bot.send_message(support_id, f"{support_name}, Поздравляем! Вас добавили в команду технической поддержки. Ваш код доступа: {code}")

        bot.reply_to(message, f"{support_name} - Добавлен в Support! Код доступа: {code}")
    else:
        bot.reply_to(message, "Недоступно для тебя")

# Обработчик команды /close
@bot.message_handler(commands=['close'])
def close_command(message):
    if message.from_user and message.from_user.id in allowed_users:
        # Проверяем, был ли передан аргумент после команды /close
        if len(message.text.split()) > 1:
            sender_id = message.text.split()[1]
            chat_id = sender_id
            user_id = message.from_user.id
            recipient_id = get_recipient(user_id)
            recipient_id_to = recipient_id
            sender_id_to = sender_id
            language = "rus"
            language_user = get_sender_language(sender_id)
            sender_keyboard = send_new_buttons_sender_id_to(language_user, sender_id_to)
            recipient_keyboard = send_new_buttons_sender_id_to(language, recipient_id_to)
            bot.send_message(recipient_id_to, f"Вы завершили чат с {sender_id_to} ✅",reply_markup=recipient_keyboard)
            if language_user == "rus":
                bot.send_message(sender_id_to, f"👋 Специалист не дождался вашей оценки и принудительно отключил чат! Благодарим за обращение!", reply_markup=sender_keyboard)
            else:
                bot.send_message(sender_id_to, f"👋 Specialist didn't wait for your assessment and forcibly disconnected the chat! We thank you for your appeal!", reply_markup=sender_keyboard)
            increment_like_count(recipient_id)
            delete_chat(sender_id)
        else:
            bot.reply_to(message, "Пример /close 77236482")
    else:
        bot.reply_to(message, "Недоступно для тебя")

# Обработчик команды /police
@bot.message_handler(commands=['police'])
def handle_police_command(message):
    if message.from_user and message.from_user.id in allowed_users:
        if len(message.text.split()) == 2:
            # Получаем аргумент (ID пользователя)
            user_id = message.text.split()[1]

            # Удаляем пользователя из таблицы "police"
            delete_user_from_police(user_id)

            # Отправляем сообщение об успешном удалении
            bot.reply_to(message, f"C ID {user_id} успешно сняты ограничения")
        else:
            # Если аргумент отсутствует, отправляем сообщение об ошибке
            bot.reply_to(message, " Используй /police user_id")
    else:
        bot.reply_to(message, "Недоступно для тебя")

def delete_user_from_police(user_id):
    connection = connect_to_db('chat_data.db')
    cursor = connection.cursor()

    # Удаляем пользователя из таблицы
    cursor.execute("""
        DELETE FROM police
        WHERE sender_id = ?
    """, (user_id,))

    connection.commit()
    connection.close()


# Обработчик команды /iuser
@bot.message_handler(commands=['iuser'])
def send_chat_info(message):
    try:
        if message.from_user and message.from_user.id in allowed_users:
            # Проверяем, что сообщение содержит аргумент
            if len(message.text.split()) != 2:
                bot.reply_to(message, 'Пожалуйста, укажи только один аргумент - @username.')
                return
            # Получаем chat_id из аргумента
            username = message.text.split()[1].lstrip('@')
            user_id = get_user_by_username(username)
            if user_id is None:
                bot.reply_to(message, f"Пользователь @{username} не найден.")
                return
            language, prefix = get_prof_info(user_id)
            chat_rows = get_creators_info(user_id)
            if prefix == "grand":
                prefix_text = "💠"
            else:
                prefix_text = "◽️" 
            if language == "rus":
                language_text = "🇷🇺"
            else:
                language_text = "🇺🇸"
            if chat_rows:
                text = f"Статистика @{username} ({language_text}) ({prefix_text})\nСоздатель:\n"
                for chat_id, chat_name in chat_rows:
                    text += f"<code>{chat_id}</code> ({chat_name})\n"
            else:
                text = f"Статистика @{username} ({language_text}) ({prefix_text})"
            keyboard = show_user_group_buttons(user_id)
            bot.reply_to(message, text, reply_markup=keyboard, parse_mode="HTML")
        else:
            bot.reply_to(message, "Недоступно для тебя")
    except Exception as e:
        error_message = f"Произошла ошибка при выполнении команды. Ошибка: {e}"
        bot.reply_to(message, error_message)

# Функция для получения информации из базы данных по chat_id
def get_chat_users(chat_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_id, user_username FROM users WHERE chat_id=?", (chat_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        conn.close()
        raise e

# Обработчик команды /chatusers
@bot.message_handler(commands=['chatusers'])
def send_chat_users(message):
    try:
        if message.from_user and message.from_user.id in allowed_users:
            # Проверяем, что сообщение содержит аргумент
            if len(message.text.split()) != 2:
                bot.reply_to(message, 'Пожалуйста, укажи только один аргумент - chat_id.')
                return
            # Получаем chat_id из аргумента
            chat_id = message.text.split()[1]
            
            # Получение информации о пользователях чата из базы данных
            user_info = get_chat_users(chat_id)
            if user_info:
                # Формируем список строк с информацией о пользователях
                user_list = [f"ID: <code>{user[0]}</code>(@{user[1]})" if user[1] else f"ID: <code>{user[0]}</code>" for user in user_info]
                # Разбиваем список на части для отправки
                chunk_size = 50  # Максимальное количество пользователей в одном сообщении
                chunks = [user_list[i:i + chunk_size] for i in range(0, len(user_list), chunk_size)]
                for chunk in chunks:
                    # Формируем строку с информацией о пользователе для данной части
                    users_response = ",   ".join(chunk)
                    bot.reply_to(message, f"Список пользователей чата с ID {chat_id}:\n{users_response}", parse_mode="HTML")
            else:
                bot.reply_to(message, f"Пользователи чата с ID {chat_id} не найдены.")
        else:
            bot.reply_to(message, "Недоступно для тебя")
    except Exception as e:
        # Обработка ошибок
        bot.reply_to(message, f"Произошла ошибка при выполнении команды.")




# Функция для получения информации из базы данных по chat_id
def get_chat_info(chat_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM chats WHERE chat_id=?", (chat_id,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        conn.close()
        raise e

# Обработчик команды /infoB
@bot.message_handler(commands=['ichat'])
def send_chat_info(message):
    try:
        if message.from_user and message.from_user.id in allowed_users:
            # Проверяем, что сообщение содержит аргумент
            if len(message.text.split()) != 2:
                bot.reply_to(message, 'Пожалуйста, укажи только один аргумент - chat_id.')
                return
            # Получаем chat_id из аргумента
            chat_id = message.text.split()[1]
            
            # Получение информации о чате из базы данных
            chat_info = get_chat_info(chat_id)
            if chat_info:
                # Отправляем информацию в чат
                for row in chat_info:
                    if row[32] == "grand":
                        prefix = "💠"
                    else:
                        prefix = "◽️" 
                    if row[4] == "rus":
                        language = "🇷🇺"
                    else:
                        language = "🇺🇸"
                    if row[18] == "on":
                        seton = "✅"
                    else:
                        seton = "❌"
                    if row[15] == "on":
                        prof = "✅"
                    else:
                        prof = "❌"
                    if row[19] == "on":
                        mat = "✅"
                    else:
                        mat = "❌"
                    if row[20] == "on":
                        flood = "✅"
                    else:
                        flood = "❌"
                    if row[30] == "on":
                        link = "✅"
                    else:
                        link = "❌"
                    if row[17] == "on":
                        sup = "✅"
                    else:
                        sup = "❌"
                    if row[13] == "on_earn":
                        earn = "✅"
                    else:
                        earn = "❌"

                    response = f"<code>{row[0]}</code> ({row[1]}) ({prefix})\n\nСоздатель: <code>{row[2]}</code> (@{row[3]})\nЯзык: {language} 🙎: {row[5]}\n💬: {row[6]}\n💠: {row[7]}\n📝: {row[8]}\n⚠️: {row[10]}\n🎯: {row[11]}\nЗаработок: {earn}\nПроф общение: {prof}\nСпам: {seton}\nМат: {mat}\nФлуд: {flood}\nСсылки: {link}\nSUP режим: {sup}\nКоэф Grand: {row[16]}\nПриветствие: {row[14]}"
                bot.reply_to(message, response, parse_mode="HTML")
            else:
                bot.reply_to(message, f"Информация о чате с ID {chat_id} не найдена.")
        else:
            bot.reply_to(message, "Недоступно для тебя")
    except Exception as e:
        # Обработка ошибок
        bot.reply_to(message, f"Произошла ошибка при выполнении команды.")

    # Функция для обновления значения указанного столбца для указанного чата
def update_creator_column(creator_id, chat_id, column_name, new_value):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE creators SET {column_name}=? WHERE creator_id=? AND chat_id=?", (new_value, creator_id, chat_id))
        conn.commit()
        conn.close()
    except Exception as e:
        conn.close()
        raise e

# Обработчик команды /upchat
@bot.message_handler(commands=['upcreator'])
def update_chat_column_handler(message):
    try:
        if message.from_user and message.from_user.id in allowed_users:
            # Проверяем, что сообщение содержит аргументы
            if len(message.text.split()) != 5:
                bot.reply_to(message, 'Пожалуйста, укажи три аргумента - creator_id, chat_id название столбца и новое значение.')
                return
            
            # Получаем chat_id, название столбца и новое значение из аргументов
            creator_id = message.text.split()[1]
            chat_id = message.text.split()[2]
            column_name = message.text.split()[3]
            new_value = message.text.split()[4]
            
            # Обновляем значение столбца в базе данных
            update_creator_column(creator_id, chat_id, column_name, new_value)
            
            bot.reply_to(message, f"Для {creator_id} и чата {chat_id} значения {column_name} обновлено на {new_value}")
        else:
            bot.reply_to(message, "Недоступно для тебя")
    except Exception as e:
        # Обработка ошибок
        bot.reply_to(message, f"Произошла ошибка при выполнении команды.")

    # Функция для обновления значения указанного столбца для указанного чата
def update_user_column(user_id, chat_id, column_name, new_value):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE users SET {column_name}=? WHERE user_id=? AND chat_id=?", (new_value, user_id, chat_id))
        conn.commit()
        conn.close()
    except Exception as e:
        conn.close()
        raise e

# Обработчик команды /upchat
@bot.message_handler(commands=['upuser'])
def update_chat_column_handler(message):
    try:
        if message.from_user and message.from_user.id in allowed_users:
            # Проверяем, что сообщение содержит аргументы
            if len(message.text.split()) != 5:
                bot.reply_to(message, 'Пожалуйста, укажи три аргумента - user_id, chat_id название столбца и новое значение.')
                return
            
            # Получаем chat_id, название столбца и новое значение из аргументов
            user_id = message.text.split()[1]
            chat_id = message.text.split()[2]
            column_name = message.text.split()[3]
            new_value = message.text.split()[4]
            
            # Обновляем значение столбца в базе данных
            update_user_column(user_id, chat_id, column_name, new_value)
            
            bot.reply_to(message, f"Для {user_id} в чате {chat_id} значения {column_name} обновлено на {new_value}")
        else:
            bot.reply_to(message, "Недоступно для тебя")
    except Exception as e:
        # Обработка ошибок
        bot.reply_to(message, f"Произошла ошибка при выполнении команды.")

    # Функция для обновления значения указанного столбца для указанного чата
def update_chat_column(chat_id, column_name, new_value):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE chats SET {column_name}=? WHERE chat_id=?", (new_value, chat_id))
        conn.commit()
        conn.close()
    except Exception as e:
        conn.close()
        raise e

# Обработчик команды /upchat
@bot.message_handler(commands=['upchat'])
def update_chat_column_handler(message):
    try:
        if message.from_user and message.from_user.id in allowed_users:
            # Проверяем, что сообщение содержит аргументы
            if len(message.text.split()) != 4:
                bot.reply_to(message, 'Пожалуйста, укажи три аргумента - chat_id, название столбца и новое значение.')
                return
            
            # Получаем chat_id, название столбца и новое значение из аргументов
            chat_id = message.text.split()[1]
            column_name = message.text.split()[2]
            new_value = message.text.split()[3]
            
            # Обновляем значение столбца в базе данных
            update_chat_column(chat_id, column_name, new_value)
            
            bot.reply_to(message, f"Для {chat_id} значения {column_name} обновлено на {new_value}")
        else:
            bot.reply_to(message, "Недоступно для тебя")
    except Exception as e:
        # Обработка ошибок
        bot.reply_to(message, f"Произошла ошибка при выполнении команды.")

# Функция для обновления значения указанного столбца для указанного пользователя
def gift_grand(user_id, coef):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    try:
        # Выбираем случайный chat_id для отправки сообщения
        cursor.execute("SELECT chat_id FROM users WHERE user_id = ?", (user_id,))
        chat_ids = cursor.fetchall()
        random_chat_id = random.choice(chat_ids)[0]
        
        # Получаем текущее значение grand_count для пользователя
        cursor.execute("SELECT bonus_count FROM users WHERE user_id = ? AND chat_id = ?", (user_id, random_chat_id))
        current_grand_count = cursor.fetchone()[0]
        
        # Добавляем новый коэффициент к текущему значению
        new_grand_count = current_grand_count + coef
        
        # Обновляем значение grand_count в базе данных для указанного пользователя и chat_id
        cursor.execute("UPDATE users SET bonus_count = ? WHERE user_id = ? AND chat_id = ?", (new_grand_count, user_id, random_chat_id))
        conn.commit()
        
        # Выбираем случайный chat_name для отправки сообщения
        cursor.execute("SELECT chat_name FROM users WHERE user_id = ? AND chat_id = ?", (user_id, random_chat_id))
        chat_name = cursor.fetchone()[0]
        
        conn.close()
        
        return chat_name
    except Exception as e:
        conn.close()
        raise e

# Обработчик команды /gift
@bot.message_handler(commands=['gift'])
def update_chat_column_handler(message):
    try:
        if message.from_user and message.from_user.id in allowed_users:
            args = message.text.split()
            if len(args) != 3:
                bot.reply_to(message, 'Пожалуйста, укажи имя пользователя и сумму подарка.')
                return
            
            # Получаем имя пользователя и коэффициент из аргументов
            username = args[1].lstrip('@')
            try:
                coef = float(args[2])
            except ValueError:
                bot.reply_to(message, 'Коэффициент должен быть числом.')
                return
            
            # Получаем user_id по имени пользователя
            user_id = get_user_by_username(username)
            if user_id is None:
                bot.reply_to(message, 'Пользователь не найден.')
                return
            
            language = get_user_language(user_id)
            
            # Обновляем значение столбца в базе данных для указанного пользователя
            chat_name = gift_grand(user_id, coef)
            
        # Отправляем сообщение по user_id
            try:
                # Обновляем значение столбца в базе данных для указанного пользователя
                chat_name = gift_grand(user_id, coef)
                
                # Определяем текст сообщения в зависимости от языка
                if language == "rus":
                    text = f"Привет! 🎁 Ты получил подарок от сообщества GRAND TIME в размере 💠 {coef} G-бонусов! 🌟 Начисление в статистике \"{chat_name}\""
                else:
                    text = f"Hello! 🎁 You have received a gift from the GRAND TIME community in the amount of 💠 {coef} G-bonuses! 🌟 Accrual in the statistics \"{chat_name}\""
                
                # Отправляем сообщение пользователю
                bot.send_message(chat_id=user_id, text=text)
                bot.reply_to(message, f"Отправлено!")
            except Exception as e:
                bot.reply_to(message, f"Не удалось отправить сообщение о подарке!")
        else:
            bot.reply_to(message, "Недоступно для тебя")
    except Exception as e:
        # Обработка ошибок
        bot.reply_to(message, f"Произошла ошибка при выполнении команды. {e}")



    # Функция для обновления значения указанного столбца для указанного чата
def update_coef(coef):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE chats SET grand_count = ?", (coef,))
        conn.commit()
        conn.close()
    except Exception as e:
        conn.close()
        raise e

# Обработчик команды /upcoef
@bot.message_handler(commands=['upcoef'])
def update_chat_column_handler(message):
    try:
        if message.from_user and message.from_user.id in allowed_users:
            args = message.text.split()
            if len(args) != 2:
                bot.reply_to(message, 'Пожалуйста, укажи новый коэфициент - число.')
                return
            
            # Проверяем, что второй аргумент является дробным числом
            try:
                coef = float(args[1])
            except ValueError:
                bot.reply_to(message, 'Коэффициент должен быть числом.')
                return
            
            # Получаем chat_id, название столбца и новое значение из аргументов
            
            # Обновляем значение столбца в базе данных
            update_coef(coef)
            
            bot.reply_to(message, f"Новый коэфициент {coef} для всех групп успешно обновлен!")
        else:
            bot.reply_to(message, "Недоступно для тебя")
    except Exception as e:
        # Обработка ошибок
        bot.reply_to(message, f"Произошла ошибка при выполнении команды.")



# Функция для добавления значения в таблицу book
def add_to_book_en(value):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO book_en (value) VALUES (?)''', (value,))
    conn.commit()
    conn.close()

# Обработчик команды /bookadd
@bot.message_handler(commands=['bookadden'])
def handle_book_add_command(message):
    if message.from_user and message.from_user.id in allowed_users:
        # Проверяем, что после команды есть текст
        if len(message.text.split(maxsplit=1)) > 1:
            command, *value = message.text.split(" ")
            value = " ".join(value)
            add_to_book_en(value)
            bot.reply_to(message, f"✅ '{value}'.")
        else:
            bot.reply_to(message, "Пожалуйста, укажи текст на английском после команды /bookadden.")
    else:
        bot.reply_to(message, "Недоступно для тебя")


# Функция для добавления значения в таблицу book
def add_to_book(value):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO book (value) VALUES (?)''', (value,))
    conn.commit()
    conn.close()

# Обработчик команды /bookadd
@bot.message_handler(commands=['bookadd'])
def handle_book_add_command(message):
    if message.from_user and message.from_user.id in allowed_users:
        if len(message.text.split(maxsplit=1)) > 1:
            command, *value = message.text.split(" ")
            value = " ".join(value)
            add_to_book(value)
            bot.reply_to(message, f"✅ '{value}'.")
        else:
            bot.reply_to(message, "Пожалуйста, укажи текст после команды /bookadd.")
    else:
        bot.reply_to(message, "Недоступно для тебя")

# Функция для удаления значения из таблицы book
def remove_from_book(value):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM book WHERE value = ?''', (value,))
    conn.commit()
    conn.close()

# Обработчик команды /bookremove
@bot.message_handler(commands=['bookremove'])
def handle_book_remove_command(message):
    if message.from_user and message.from_user.id in allowed_users:
        # Проверяем, что после команды есть текст
        if len(message.text.split(maxsplit=1)) > 1:
            command, *value = message.text.split(" ")
            value = " ".join(value)
            remove_from_book(value)
            bot.reply_to(message, f"✅ '{value}' было удалено.")
        else:
            bot.reply_to(message, "Пожалуйста, укажи текст после команды /bookremove text.")
    else:
        bot.reply_to(message, "Недоступно для тебя")

# Функция для удаления значения из таблицы book
def en_remove_from_book(value):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM book_en WHERE value = ?''', (value,))
    conn.commit()
    conn.close()

# Обработчик команды /bookremove
@bot.message_handler(commands=['enbookremove'])
def handle_book_remove_command(message):
    if message.from_user and message.from_user.id in allowed_users:
        # Проверяем, что после команды есть текст
        if len(message.text.split(maxsplit=1)) > 1:
            command, *value = message.text.split(" ")
            value = " ".join(value)
            en_remove_from_book(value)
            bot.reply_to(message, f"✅ '{value}' было удалено.")
        else:
            bot.reply_to(message, "Пожалуйста, укажи текст после команды /enbookremove text.")
    else:
        bot.reply_to(message, "Недоступно для тебя")

# Функция для получения всех значений из таблицы book
def get_book_info_en():
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM book_en''')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Обработчик команды /bookinfo
@bot.message_handler(commands=['bookinfoen'])
def handle_book_info_command(message):
    if message.from_user and message.from_user.id in allowed_users:
        # Проверяем, что команда доступна только определенным пользователям
        book_info = get_book_info_en()
        if book_info:
            values = "\n\n".join([row[1] for row in book_info])
            bot.reply_to(message, f"Значения для книги:\n\n{values}")
        else:
            bot.reply_to(message, "Значений нет")
    else:
        bot.reply_to(message, "Недоступно для тебя")

# Функция для получения всех значений из таблицы book
def get_book_info():
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM book''')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Обработчик команды /bookinfo
@bot.message_handler(commands=['bookinfo'])
def handle_book_info_command(message):
    if message.from_user and message.from_user.id in allowed_users:
        # Проверяем, что команда доступна только определенным пользователям
        book_info = get_book_info()
        if book_info:
            values = "\n\n".join([row[1] for row in book_info])
            bot.reply_to(message, f"Значения для книги:\n\n{values}")
        else:
            bot.reply_to(message, "Значений нет")
    else:
        bot.reply_to(message, "Недоступно для тебя!")

    # Функция для удаления данных о чате и создателе из базы данных
def remove_chat_and_creator_from_db(chat_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM chats WHERE chat_id=?", (chat_id,))
        cursor.execute("DELETE FROM creators WHERE chat_id=?", (chat_id,))
        conn.commit()
        
        # Добавление вывода в консоль
        print(f"Deleted data for chat ID: {chat_id}")
        
        return True
    except Exception as e:
        # Обработка ошибок
        return False
    
    finally:
        conn.close()

def remove_chat_db(chat_id):
    conn = connect_to_db('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM chats WHERE chat_id=?", (chat_id,))
        conn.commit()
        
        # Добавление вывода в консоль
        print(f"Deleted data for chat ID: {chat_id}")
        
        return True
    except Exception as e:
        # Обработка ошибок
        return False
    
    finally:
        conn.close()    


# Обработчик команды /delchat
@bot.message_handler(commands=['delchat'])
def delete_chat_and_creator(message):
    try:
        if message.from_user and message.from_user.id in allowed_users:
            # Проверяем, что команда доступна только определенным пользователям
            # Проверяем, что сообщение содержит аргумент
            if len(message.text.split()) != 2:
                bot.reply_to(message, 'Пожалуйста, укажи только один аргумент - chat_id.')
                return
            
            # Получаем chat_id из аргумента
            chat_id = message.text.split()[1]
            
            # Удаление данных о чате и создателе из базы данных
            if remove_chat_and_creator_from_db(chat_id):
                remove_chat_db(chat_id)
                bot.reply_to(message, f"Успешно удалены данные для чата с ID: {chat_id}")
            else:
                bot.reply_to(message, f"Произошла ошибка при удалении данных из базы данных.")
        else:
            bot.reply_to(message, f"Недоступно для тебя!")
    except Exception as e:
        # Обработка ошибок
        bot.reply_to(message, f"Произошла ошибка при выполнении команды.")

def delete_user(user_id):
    # Подключаемся к базе данных SQLite для удаления пользователя из таблицы users
    connection = connect_to_db('database.db')
    cursor = connection.cursor()

    # Удаляем пользователя из таблицы users
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    connection.commit()

    cursor.close()
    connection.close()

    # Подключаемся к базе данных SQLite для удаления пользователя из таблицы active_chats
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()

    # Удаляем пользователя из таблицы active_chats
    cursor.execute("DELETE FROM active_chats WHERE recipient_id = ? OR sender_id = ?", (user_id, user_id))
    conn.commit()

    cursor.close()
    conn.close()

@bot.message_handler(commands=['deluser'])
def del_user(message):
    if message.from_user and message.from_user.id in allowed_users:
        # Проверка, что сообщение отправлено в личном чате с ботом
        if message.chat.type == "private":
            # Разделяем команду на аргументы
            args = message.text.split()
            # Проверяем, что команда имеет правильный формат
            if len(args) == 2:
                # Получаем user_id из аргументов
                user_id = args[1]

                delete_user(user_id)

                bot.reply_to(message, f"Пользователь с ID {user_id} успешно удален.")
            else:
                bot.reply_to(message, "Используй: /deluser user_id")
        else:
            bot.reply_to(message, "Команда доступна только в личных чатах с ботом.")
    else:
        bot.reply_to(message, "Для тебя не доступно")

# Обработчик команды /proden
@bot.message_handler(commands=['proden'])
def send_info(message):
    # Проверяем, является ли идентификатор чата разрешенным
    if message.from_user and message.from_user.id in allowed_users:
        # Записываем сообщение от пользователя
        global info_message
        info_message = message.text[8:] 
        
        keyboard = types.InlineKeyboardMarkup()
        send_button = types.InlineKeyboardButton("Отправить", callback_data="send_info_en")
        keyboard.add(send_button)
            
        # Создаем сообщение с вашим текстом и кнопкой "Отправить"
        message_text = f"Сообщение для всех пользователей с англ языком:\n\n{info_message}"
        bot.send_message(message.chat.id, message_text, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Функционал не доступен для вас.")

# Обработчик нажатия на кнопку "Отправить"
@bot.callback_query_handler(func=lambda call: call.data == "send_info_en")
def send_info_to_users(call):
    # Проверяем, является ли идентификатор чата разрешенным
    if call.message.chat.id in allowed_users:
        sent_count = send_info_to_en_users(info_message)
        bot.answer_callback_query(call.id, f"Сообщение отправлено {sent_count} пользователям с англ языком.")
    else:
        bot.answer_callback_query(call.id, "Функционал не доступен для вас.")


def send_info_to_en_users(info_message):
    sent_count = 0
    try:
        # Открываем соединение с базой данных SQLite для пользователей
        connection_users = connect_to_db('database.db')
        cursor_users = connection_users.cursor()

        # Получаем всех пользователей из базы данных
        cursor_users.execute("SELECT DISTINCT user_id, language FROM users")
        users_data = cursor_users.fetchall()

        # Отправляем рекламное сообщение каждому пользователю
        for user_data in users_data:
            user_id, language = user_data
            try:
                if language == 'en':
                    # Если язык - русский, отправляем сообщение на русском
                    bot.send_message(user_id, text=info_message)
                    print(f"Отправлено сообщение пользователю {user_id} на англ")
                    sent_count += 1
                elif language == 'rus':
                    pass
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

        # Закрываем соединение с базой данных для пользователей
        cursor_users.close()
        connection_users.close()
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении SQL-запроса для пользователей: {e}")
    
    return sent_count

# Обработчик команды /prod
@bot.message_handler(commands=['prodchaten'])
def send_info(message):
    # Проверяем, является ли идентификатор чата разрешенным
    if message.from_user and message.from_user.id in allowed_users:
        # Записываем сообщение от пользователя
        global info_message
        info_message = message.text[12:] 
        
        keyboard = types.InlineKeyboardMarkup()
        send_button = types.InlineKeyboardButton("Отправить", callback_data="send_info_chat_en")
        keyboard.add(send_button)
            
        # Создаем сообщение с вашим текстом и кнопкой "Отправить"
        message_text = f"Сообщение для всех групп с англ языком:\n\n{info_message}"
        bot.send_message(message.chat.id, message_text, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Функционал не доступен для вас.")

# Обработчик нажатия на кнопку "Отправить"
@bot.callback_query_handler(func=lambda call: call.data == "send_info_chat_en")
def send_info_to_users(call):
    # Проверяем, является ли идентификатор чата разрешенным
    if call.message.chat.id in allowed_users:
        sent_count = send_info_to_chats_en(info_message)
        bot.answer_callback_query(call.id, f"Сообщение успешно отправлено {sent_count} группам с англ языком.")
    else:
        bot.answer_callback_query(call.id, "Функционал не доступен для вас.")


def send_info_to_chats_en(info_message):
    sent_count = 0
    try:
        # Открываем соединение с базой данных SQLite для пользователей
        connection_users = connect_to_db('chat_data.db')
        cursor_users = connection_users.cursor()

        # Получаем всех пользователей из базы данных
        cursor_users.execute("SELECT DISTINCT chat_id, language FROM chats")
        users_data = cursor_users.fetchall()

        # Отправляем рекламное сообщение каждому пользователю
        for user_data in users_data:
            user_id, language = user_data
            try:
                if language == 'en':
                    # Если язык - русский, отправляем сообщение на русском
                    bot.send_message(user_id, text=info_message)
                    print(f"Отправлено сообщение группе {user_id} на русском")
                    sent_count += 1
                elif language == 'rus':
                    pass
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

        # Закрываем соединение с базой данных для пользователей
        cursor_users.close()
        connection_users.close()
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении SQL-запроса для пользователей: {e}")
    return sent_count

# Обработчик команды /prod
@bot.message_handler(commands=['prodchat'])
def send_info(message):
    # Проверяем, является ли идентификатор чата разрешенным
    if message.from_user and message.from_user.id in allowed_users:
        # Записываем сообщение от пользователя
        global info_message
        info_message = message.text[10:] 
        
        keyboard = types.InlineKeyboardMarkup()
        send_button = types.InlineKeyboardButton("Отправить", callback_data="send_info_chat")
        keyboard.add(send_button)
            
        # Создаем сообщение с вашим текстом и кнопкой "Отправить"
        message_text = f"Сообщение для всех групп с русским языком:\n\n{info_message}"
        bot.send_message(message.chat.id, message_text, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Функционал не доступен для вас.")

# Обработчик нажатия на кнопку "Отправить"
@bot.callback_query_handler(func=lambda call: call.data == "send_info_chat")
def send_info_to_users(call):
    # Проверяем, является ли идентификатор чата разрешенным
    if call.message.chat.id in allowed_users:
        sent_count = send_info_to_chats(info_message)
        bot.answer_callback_query(call.id, f"Сообщение успешно отправлено {sent_count} группам с русским языком.")
    else:
        bot.answer_callback_query(call.id, "Функционал не доступен для вас.")


def send_info_to_chats(info_message):
    sent_count = 0
    try:
        # Открываем соединение с базой данных SQLite для пользователей
        connection_users = connect_to_db('chat_data.db')
        cursor_users = connection_users.cursor()

        # Получаем всех пользователей из базы данных
        cursor_users.execute("SELECT DISTINCT chat_id, language FROM chats")
        users_data = cursor_users.fetchall()

        # Отправляем рекламное сообщение каждому пользователю
        for user_data in users_data:
            user_id, language = user_data
            try:
                if language == 'rus':
                    # Если язык - русский, отправляем сообщение на русском
                    bot.send_message(user_id, text=info_message)
                    print(f"Отправлено сообщение группе {user_id} на русском")
                    sent_count += 1
                elif language == 'en':
                    pass
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

        # Закрываем соединение с базой данных для пользователей
        cursor_users.close()
        connection_users.close()
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении SQL-запроса для пользователей: {e}")
    
    return sent_count

# Обработчик команды /prod
@bot.message_handler(commands=['prod'])
def send_info(message):
    # Проверяем, является ли идентификатор чата разрешенным
    if message.from_user and message.from_user.id in allowed_users:
        # Записываем сообщение от пользователя
        global info_message
        info_message = message.text[6:] 
        
        keyboard = types.InlineKeyboardMarkup()
        send_button = types.InlineKeyboardButton("Отправить", callback_data="send_info")
        keyboard.add(send_button)
            
        # Создаем сообщение с вашим текстом и кнопкой "Отправить"
        message_text = f"Сообщение для всех пользователей с русским языком:\n\n{info_message}"
        bot.send_message(message.chat.id, message_text, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Функционал не доступен для вас.")

# Обработчик нажатия на кнопку "Отправить"
@bot.callback_query_handler(func=lambda call: call.data == "send_info")
def send_info_to_users(call):
    # Проверяем, является ли идентификатор чата разрешенным
    if call.message.chat.id in allowed_users:
        sent_count = send_info_to_users(info_message)
        bot.answer_callback_query(call.id, f"Сообщение успешно отправлено {sent_count} пользователям с русским языком.")
    else:
        bot.answer_callback_query(call.id, "Функционал не доступен для вас.")


def send_info_to_users(info_message):
    sent_count = 0
    try:
        # Открываем соединение с базой данных SQLite для пользователей
        connection_users = connect_to_db('database.db')
        cursor_users = connection_users.cursor()

        # Получаем всех пользователей из базы данных
        cursor_users.execute("SELECT DISTINCT user_id, language FROM users")
        users_data = cursor_users.fetchall()

        # Отправляем рекламное сообщение каждому пользователю
        for user_data in users_data:
            user_id, language = user_data
            try:
                if language == 'rus':
                    # Если язык - русский, отправляем сообщение на русском
                    bot.send_message(user_id, text=info_message)
                    print(f"Отправлено сообщение пользователю {user_id} на русском")
                    sent_count += 1
                elif language == 'en':
                    pass
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

        # Закрываем соединение с базой данных для пользователей
        cursor_users.close()
        connection_users.close()
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении SQL-запроса для пользователей: {e}")
    
    return sent_count

# Проверка наличия ключевого слова в базе данных
def is_keyword_read_spam():
    with connect_to_db('spam.db') as conn:
        try:
            c = conn.cursor()
            c.execute('SELECT COUNT(keyword) FROM keywords')
            result = c.fetchone()
            return result[0] > 0
        except sqlite3.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return False

@bot.message_handler(commands=['rspam'])
def read_good_keywords(message):
    if message.from_user and message.from_user.id in allowed_users:
        if is_keyword_read_spam():
            with connect_to_db('spam.db') as conn:
                try:
                    c = conn.cursor()
                    c.execute('SELECT keyword FROM keywords')
                    results = c.fetchall()
                    reply_message = "Значения в базе данных:\n\n"
                    for result in results:
                        reply_message += f"{result[0]},   "
                    bot.reply_to(message, reply_message)
                except sqlite3.Error as e:
                    print("Ошибка при выполнении запроса:", e)
                    bot.reply_to(message, "Ошибка при выполнении запроса.")
        else:
            bot.reply_to(message, "База данных пуста.")
    else:
        bot.reply_to(message, "У вас нет прав на выполнение этой команды.")

# Проверка наличия ключевого слова в базе данных
def is_keyword_exists(keyword):
    conn = connect_to_db('spam.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM keywords WHERE keyword=?', (keyword,))
    result = c.fetchone()[0]
    conn.close()
    return result > 0

## Функция для обработки команды /wspam
@bot.message_handler(commands=['wspam'])
def write_spam_keywords(message):
    if message.from_user and message.from_user.id in allowed_users:
        # Проверяем, что после команды есть текст
        if len(message.text.split(maxsplit=1)) > 1:
            # Получаем ключевые фразы из текста сообщения
            keyword_phrases = message.text.split(maxsplit=1)[1]
            keyword_phrases = keyword_phrases.split(',')  
            reply_message = ""
            for keyword_phrase in keyword_phrases:
                keyword_phrase = keyword_phrase.strip().lower()  
                if not is_keyword_exists(keyword_phrase):
                    add_spam_keyword(keyword_phrase)
                    reply_message += f"Добавлено: {keyword_phrase}\n"
                else:
                    reply_message += f"\n\nУже существует: {keyword_phrase}\n"
            bot.reply_to(message, reply_message.strip())
        else:
            bot.reply_to(message, "Пожалуйста, укажи ключевые фразы после команды /wspam.")
    else:
        bot.reply_to(message, "У вас нет прав на выполнение этой команды.")



# Добавление нового ключевого слова в базу данных
def add_fuck_keyword(keyword_phrase):
    conn = connect_to_db('fuck.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO keywords (keyword) VALUES (?)', (keyword_phrase,))
    conn.commit()
    conn.close()

# Проверка наличия ключевого слова в базе данных
def is_keyword_read_fuck():
    with connect_to_db('fuck.db') as conn:
        try:
            c = conn.cursor()
            c.execute('SELECT COUNT(keyword) FROM keywords')
            result = c.fetchone()
            return result[0] > 0
        except sqlite3.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return False

@bot.message_handler(commands=['rfuck'])
def read_good_keywords(message):
    if message.from_user and message.from_user.id in allowed_users:
        if is_keyword_read_fuck():
            with connect_to_db('fuck.db') as conn:
                try:
                    c = conn.cursor()
                    c.execute('SELECT keyword FROM keywords')
                    results = c.fetchall()
                    reply_message = "Значения в базе данных:\n\n"
                    for result in results:
                        reply_message += f"{result[0]},   "
                    bot.reply_to(message, reply_message)
                except sqlite3.Error as e:
                    print("Ошибка при выполнении запроса:", e)
                    bot.reply_to(message, "Ошибка при выполнении запроса.")
        else:
            bot.reply_to(message, "База данных пуста.")
    else:
        bot.reply_to(message, "У вас нет прав на выполнение этой команды.")

# Проверка наличия ключевого слова в базе данных
def is_keyword_fuck(keyword):
    conn = connect_to_db('fuck.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM keywords WHERE keyword=?', (keyword,))
    result = c.fetchone()[0]
    conn.close()
    return result > 0

## Функция для обработки команды /wfuck
@bot.message_handler(commands=['wfuck'])
def write_spam_keywords(message):
    if message.from_user and message.from_user.id in allowed_users:
        # Проверяем, что после команды есть текст
        if len(message.text.split(maxsplit=1)) > 1:
            # Получаем ключевые фразы из текста сообщения
            keyword_phrases = message.text.split(maxsplit=1)[1]
            keyword_phrases = keyword_phrases.split(',')  
            reply_message = ""
            for keyword_phrase in keyword_phrases:
                keyword_phrase = keyword_phrase.strip().lower()  
                if not is_keyword_fuck(keyword_phrase):
                    add_fuck_keyword(keyword_phrase)
                    reply_message += f"✅: {keyword_phrase}\n"
                else:
                    reply_message += f"\n⁉️: {keyword_phrase}\n"
            bot.reply_to(message, reply_message.strip())
        else:
            bot.reply_to(message, "Пожалуйста, укажи ключевые фразы после команды /wfuck.")
    else:
        bot.reply_to(message, "У вас нет прав на выполнение этой команды.")



# Добавление нового ключевого слова в базу данных
def add_good_keyword(keyword_phrase):
    conn = connect_to_db('good.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO keywords (keyword) VALUES (?)', (keyword_phrase,))
    conn.commit()
    conn.close()

# Проверка наличия ключевого слова в базе данных
def is_keyword_good(keyword):
    conn = connect_to_db('good.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM keywords WHERE keyword=?', (keyword,))
    result = c.fetchone()[0]
    conn.close()
    return result > 0

@bot.message_handler(commands=['wgood'])
def write_spam_keywords(message):
    if message.from_user and message.from_user.id in allowed_users:
        # Проверяем, что после команды есть текст
        if len(message.text.split(maxsplit=1)) > 1:
            # Получаем ключевые фразы из текста сообщения
            keyword_phrases = message.text.split(maxsplit=1)[1]
            keyword_phrases = keyword_phrases.split(',')  
            reply_message = ""
            for keyword_phrase in keyword_phrases:
                keyword_phrase = keyword_phrase.strip().lower()  
                if not is_keyword_good(keyword_phrase):
                    add_good_keyword(keyword_phrase)
                    reply_message += f"✅: {keyword_phrase}\n"
                else:
                    reply_message += f"\n⁉️: {keyword_phrase}\n"
            bot.reply_to(message, reply_message.strip())
        else:
            bot.reply_to(message, "Пожалуйста, укажи ключевые фразы после команды /wgood.")
    else:
        bot.reply_to(message, "У вас нет прав на выполнение этой команды.")

# Проверка наличия ключевого слова в базе данных
def is_keyword_read_good():
    with connect_to_db('good.db') as conn:
        try:
            c = conn.cursor()
            c.execute('SELECT COUNT(keyword) FROM keywords')
            result = c.fetchone()
            return result[0] > 0
        except sqlite3.Error as e:
            print("Ошибка при выполнении запроса:", e)
            return False

@bot.message_handler(commands=['rgood'])
def read_good_keywords(message):
    if message.from_user and message.from_user.id in allowed_users:
        if is_keyword_read_good():
            with connect_to_db('good.db') as conn:
                try:
                    c = conn.cursor()
                    c.execute('SELECT keyword FROM keywords')
                    results = c.fetchall()
                    reply_message = "Значения в базе данных:\n\n"
                    for result in results:
                        reply_message += f"{result[0]},   "
                    bot.reply_to(message, reply_message)
                except sqlite3.Error as e:
                    print("Ошибка при выполнении запроса:", e)
                    bot.reply_to(message, "Ошибка при выполнении запроса.")
        else:
            bot.reply_to(message, "База данных пуста.")
    else:
        bot.reply_to(message, "У вас нет прав на выполнение этой команды.")



# Обработчик STAFF команд - конец

# Обработчик STAFF кнопки база - начало
def create_keyboard_staff():
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    users_button = types.KeyboardButton(f"🙎")
    chats_button = types.KeyboardButton(f"🗂")
    back_button = types.KeyboardButton(f"⬅️")
    keyboard.add(users_button, chats_button, back_button)
    return keyboard


@bot.message_handler(func=lambda message: message.text == '⬅️')
def back_handler(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = "rus"
    text = data["leave_base_text"]
    send_buttons(chat_id, language, text, user_id)


@bot.message_handler(func=lambda message: message.text == f'🙎')
def users_handler(message):
    if message.from_user.id in allowed_users:
        connection_users = connect_to_db('database.db')
        cursor_users = connection_users.cursor()

        try:
            cursor_users.execute("SELECT user_id, language, prefix FROM users WHERE language=?", ("rus",))
            rus_users_info = cursor_users.fetchall()

            cursor_users.execute("SELECT user_id, language, prefix FROM users WHERE language=?", ("en",))
            en_users_info = cursor_users.fetchall()

            def format_users_info(users_info):
                users_info_text = ""
                for user_info in users_info:
                    user_id, language, prefix = user_info
                    if language == "rus":
                        lang_text = "🇷🇺"
                    else:
                        lang_text = "🇺🇸"
                    if prefix == "grand":
                        pref_text = "💠"
                    elif prefix == "free":
                        pref_text = "🟩"
                    else:
                        pref_text = "◽️"
                    users_info_text += f"[<code>{user_id}</code> {lang_text} {pref_text}]   "
                return users_info_text.strip()
            rus_users_info_text = format_users_info(rus_users_info)
            if len(rus_users_info_text) <= 4096:
                bot.send_message(message.chat.id, rus_users_info_text, parse_mode="HTML")
            else:
                bot.send_message(message.chat.id, rus_users_info_text[:4096], parse_mode="HTML")
                bot.send_message(message.chat.id, rus_users_info_text[4096:], parse_mode="HTML")

            en_users_info_text = format_users_info(en_users_info)
            if len(en_users_info_text) <= 4096:
                bot.send_message(message.chat.id, en_users_info_text, parse_mode="HTML")
            else:
                bot.send_message(message.chat.id, en_users_info_text[:4096], parse_mode="HTML")
                bot.send_message(message.chat.id, en_users_info_text[4096:], parse_mode="HTML")

        except sqlite3.Error as e:
            print(f"Ошибка при выполнении SQL-запроса для пользователей: {e}")

        finally:
            cursor_users.close()
            connection_users.close()
    else:
        bot.send_message(message.chat.id, "Функционал недоступен")        


@bot.message_handler(func=lambda message: message.text == f'🗂')
def chats_handler(message):
    if message.from_user.id in allowed_users:
        connection_chats = connect_to_db('chat_data.db')
        cursor_chats = connection_chats.cursor()

        try:
            cursor_chats.execute("SELECT chat_id, language, prefix, bonus_count, grand_count FROM chats WHERE language=?", ("rus",))
            rus_chats_info = cursor_chats.fetchall()

            cursor_chats.execute("SELECT chat_id, language, prefix, bonus_count, grand_count FROM chats WHERE language=?", ("en",))
            en_chats_info = cursor_chats.fetchall()

            def format_chats_info(chats_info):
                chats_info_text = ""
                for chat_info in chats_info:
                    chat_id, language, prefix, bonus_count, grand_count = chat_info
                    if language == "rus":
                        lang_text = "🇷🇺"
                    else:
                        lang_text = "🇺🇸"
                    if prefix == "grand":
                        pref_text = "💠"
                    elif prefix == "free":
                        pref_text = "🟩"
                    else:
                        pref_text = "◽️"
                    chats_info_text += f"[<code>{chat_id}</code> {lang_text} {pref_text} {round(bonus_count, 2)} ({grand_count})]\n"
                return chats_info_text
            
            rus_chats_info_text = format_chats_info(rus_chats_info)
            if len(rus_chats_info_text) <= 4096:
                bot.send_message(message.chat.id, rus_chats_info_text, parse_mode="HTML")
            else:
                bot.send_message(message.chat.id, rus_chats_info_text[:4096], parse_mode="HTML")
                bot.send_message(message.chat.id, rus_chats_info_text[4096:], parse_mode="HTML")

            en_chats_info_text = format_chats_info(en_chats_info)
            if len(en_chats_info_text) <= 4096:
                bot.send_message(message.chat.id, en_chats_info_text, parse_mode="HTML")
            else:
                bot.send_message(message.chat.id, en_chats_info_text[:4096], parse_mode="HTML")
                bot.send_message(message.chat.id, en_chats_info_text[4096:], parse_mode="HTML")

        except sqlite3.Error as e:
            print(f"Ошибка при выполнении SQL-запроса для чатов: {e}")

        finally:
            cursor_chats.close()
            connection_chats.close()


@bot.message_handler(func=lambda message: message.text == '🌐 База')
def base_handler(message):
    try:
        if message.from_user.id in allowed_users:
            connection_users = connect_to_db('database.db')
            cursor_users = connection_users.cursor()

            try:
                # Получаем общее количество пользователей
                cursor_users.execute("SELECT COUNT(*) FROM users")
                total_users_count = cursor_users.fetchone()[0]

            except sqlite3.Error as e:
                print(f"Ошибка при выполнении SQL-запроса для пользователей: {e}")

            cursor_users.close()
            connection_users.close()

            connection_chats = connect_to_db('chat_data.db')
            cursor_chats = connection_chats.cursor()

            try:
                # Получаем общее количество чатов
                cursor_chats.execute("SELECT COUNT(*) FROM chats")
                total_chats_count = cursor_chats.fetchone()[0]

                users_info_chunk = f"Выбери базу:\nКол-во пользователей: {total_users_count}\nКол-во групп: {total_chats_count}"
                staff = create_keyboard_staff()
                bot.send_message(message.chat.id, users_info_chunk, reply_markup=staff,parse_mode="HTML")
            except sqlite3.Error as e:
                print(f"Ошибка при выполнении SQL-запроса для чатов: {e}")

            cursor_chats.close()
            connection_chats.close()
        else:
            bot.send_message(message.chat.id, "У вас недостаточно прав для доступа к базе данных.")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '🌐 База:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Username: @{message.from_user.username if message.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        logging.error(error_message)

@bot.message_handler(func=lambda message: message.text == '📝 Команды')
def back_handler(message):
    if message.from_user.id in allowed_users:
        text = data["staff_commands"]["prod"]
        text += data["staff_commands"]["proden"]
        text += data["staff_commands"]["prodchat"]
        text += data["staff_commands"]["prodchaten"]
        text += data["staff_commands"]["police"]
        text += data["staff_commands"]["close"]
        text += data["staff_commands"]["support"]
        text += data["staff_commands"]["gift"]
        text += data["staff_commands"]["iuser"]
        text += data["staff_commands"]["ichat"]
        text += data["staff_commands"]["chatusers"]
        text += data["staff_commands"]["upcoef"]
        text += data["staff_commands"]["upchat"]
        text += data["staff_commands"]["upcreator"]
        text += data["staff_commands"]["upuser"]
        text += data["staff_commands"]["bookinfo"]
        text += data["staff_commands"]["bookinfoen"]
        text += data["staff_commands"]["bookadd"]
        text += data["staff_commands"]["bookadden"]
        text += data["staff_commands"]["bookremove"]
        text += data["staff_commands"]["enbookremove"]
        text += data["staff_commands"]["delchat"]
        text += data["staff_commands"]["deluser"]
        text += data["staff_commands"]["wspam"]
        text += data["staff_commands"]["rspam"]
        text += data["staff_commands"]["wfuck"]
        text += data["staff_commands"]["rfuck"]
        text += data["staff_commands"]["wgood"]
        text += data["staff_commands"]["rgood"]
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "У вас недостаточно прав!")

@bot.message_handler(func=lambda message: message.text == '👁‍🗨 Info')
def back_handler(message):
    if message.from_user.id in allowed_users:
        chats = data["staff_column"]["chat"]["chats"]
        chats += data["staff_column"]["chat"]["chat_id"]
        chats += data["staff_column"]["chat"]["chat_name"]
        chats += data["staff_column"]["chat"]["creator_id"]
        chats += data["staff_column"]["chat"]["creator_username"]
        chats += data["staff_column"]["chat"]["language"]
        chats += data["staff_column"]["chat"]["active_users"]
        chats += data["staff_column"]["chat"]["bonus_count"]
        chats += data["staff_column"]["chat"]["level_count"]
        chats += data["staff_column"]["chat"]["grand_count"]
        chats += data["staff_column"]["chat"]["earn"]
        chats += data["staff_column"]["chat"]["hi_text"]
        chats += data["staff_column"]["chat"]["good_text"]
        chats += data["staff_column"]["chat"]["spam"]
        chats += data["staff_column"]["chat"]["fuck"]
        chats += data["staff_column"]["chat"]["flood"]
        chats += data["staff_column"]["chat"]["link"]
        chats += data["staff_column"]["chat"]["prefix"]
        chats += data["staff_column"]["chat"]["support"]
        bot.send_message(message.chat.id, chats, parse_mode="HTML")
        creators = data["staff_column"]["creator"]["creators"]
        creators += data["staff_column"]["creator"]["creator_id"]
        creators += data["staff_column"]["creator"]["creator_username"]
        creators += data["staff_column"]["creator"]["chat_id"]
        creators += data["staff_column"]["creator"]["chat_name"]
        creators += data["staff_column"]["creator"]["language"]
        creators += data["staff_column"]["creator"]["bonus_count"]
        creators += data["staff_column"]["creator"]["level_count"]
        bot.send_message(message.chat.id, creators, parse_mode="HTML")
        users = data["staff_column"]["user"]["users"]
        users += data["staff_column"]["user"]["chat_id"]
        users += data["staff_column"]["user"]["chat_name"]
        users += data["staff_column"]["user"]["user_id"]
        users += data["staff_column"]["user"]["user_username"]
        users += data["staff_column"]["user"]["bonus_count"]
        bot.send_message(message.chat.id, users, parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, "У вас недостаточно прав!")

# Обработчик STAFF кнопки база - конец

# Обработчик кнопки Награда - начало
@bot.message_handler(func=lambda message: message.text in ["💎 Rewards", "💎 Награда"])
def rewards_button_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            creator_id = message.from_user.id  # Предполагаемый идентификатор создателя
            language = get_user_language(chat_id)
            text = data['reward_text'][language]['1']
            text += data['reward_text'][language]['2']
            text += data['reward_text'][language]['3']

            groups = get_user_groups(creator_id)

            if groups:
                # Если у пользователя есть группы, создаем кнопки для каждой группы
                keyboard = types.InlineKeyboardMarkup()
                if language == "en":
                    keyboard.row(types.InlineKeyboardButton("➕ Add to group", url="https://t.me/gmoderator_bot?startgroup=botstart"))  # Замените на вашу ссылку
                else:
                    keyboard.row(types.InlineKeyboardButton("➕ Добавить в группу", url="https://t.me/gmoderator_bot?startgroup=botstart"))  # Замените на вашу ссылку
                for group in groups:
                    group_id, group_name = group
                    keyboard.row(types.InlineKeyboardButton(text=group_name, callback_data=f"group_reward_{group_id}"))

                bot.send_message(chat_id, text, reply_markup=keyboard)

            else:
                keyboard = types.InlineKeyboardMarkup()
                if language == "en":
                    add_button = types.InlineKeyboardButton("➕ Add to group", url="https://t.me/gmoderator_bot?startgroup=botstart")  # Замените на вашу ссылку
                else:
                    add_button = types.InlineKeyboardButton("➕ Добавить в группу", url="https://t.me/gmoderator_bot?startgroup=botstart")  # Замените на вашу ссылку
                keyboard.add(add_button)

                bot.send_message(chat_id, text, reply_markup=keyboard)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'Награда':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{message.from_user.username if message.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('group_reward_'))
def group_reward_callback_handler(call):
    try:
        # Получаем ID группы из callback_data
        group_id = call.data.split('_')[-1]
        user_language = get_user_language(call.from_user.id)
        group_data = get_name_groups(group_id)
        groups_data = get_user_groups_reward(group_id)
        # Извлекаем данные, если они доступны
        group_name = group_data[0][0] if group_data else None
        active_users = group_data[0][1] if group_data else None
        bonus_count, level_count = groups_data[0] if groups_data else (None, None)

        if level_count == 0:
            new_active_users = 10
        elif level_count == 1:
            new_active_users = 50
        elif level_count == 2:
            new_active_users = 100
        elif level_count == 3:
            new_active_users = 250
        elif level_count == 4:
            new_active_users = 500
        elif level_count == 5:
            new_active_users = 600
        elif level_count == 6:
            new_active_users = 700
        elif level_count == 7:
            new_active_users = 800
        elif level_count == 8:
            new_active_users = 900
        elif level_count == 9:
            new_active_users = 1000
        else:
            new_active_users = 1000

        if user_language == "rus":
            message_text = f"--- <b>{group_name}</b> ---\n\n💠 Заработано: <b>{bonus_count}</b> <i>Grand бонус</i>\n\n🎯 Уровень: <b>{level_count}</b> / 10 <i>(с каждого начисления пользователю, тебе - {level_count}%)</i>\n\n🙎 Активных пользователей: <b>{active_users}</b>\n\n--- <i>Для перехода на <b>{level_count + 1} <i>({level_count + 1}%)</i></b> уровень, необходимо ещё 🙎 <b>{new_active_users - active_users}</b> активных пользователей!</i> ---\n\n--- <i>Начисления GRAND бонус для участников и владельца группы доступны только от 10 Активных пользователей!</i> ---"
        else:
            message_text = f"--- <b>{group_name}</b> ---\n\n💠 Earned <b>{bonus_count}</b> <i>Grand bonus</i>\n\n🎯 Level: <b>{level_count}</b> / 10 <i>(from each user accrual to you - {level_count}%)</i>\n\n🙎 Active users: <b>{active_users}</b>\n\n--- <i>To advance to level <b>{level_count + 1} <i>({level_count + 1}%)</i></b>, you need 🙎 <b>{new_active_users - active_users}</b> more active users!</i> ---\n\n--- <i>GRAND bonus accruals for members and group owner are available only from 10 Active users!</i> ---"
        # Отправляем отредактированное сообщение с кнопкой "Назад"
        keyboard = types.InlineKeyboardMarkup()
        if user_language == "rus":
            back_button = types.InlineKeyboardButton("⬅️ Назад", callback_data="back_reward_to_groups")
        else:
            back_button = types.InlineKeyboardButton("⬅️ Back", callback_data="back_reward_to_groups")
        keyboard.add(back_button)
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode='HTML')
    
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обработке callback от кнопки 'group_reward_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {call.from_user.id}\n"
            f"• Callback Data: {call.data}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)


@bot.callback_query_handler(func=lambda call: call.data == 'back_reward_to_groups')
def back_to_groups_callback_handler(call):
    try:
        language = get_user_language(call.from_user.id)
        text = data['reward_text'][language]['1']
        text += data['reward_text'][language]['2']
        text += data['reward_text'][language]['3']

        groups = get_user_groups(call.from_user.id)

        if groups:
            # Если у пользователя есть группы, создаем кнопки для каждой группы
            keyboard = types.InlineKeyboardMarkup()
            if language == "en":
                keyboard.row(types.InlineKeyboardButton("➕ Add to group", url="https://t.me/gmoderator_bot?startgroup=botstart"))  # Замените на вашу ссылку
            else:
                keyboard.row(types.InlineKeyboardButton("➕ Добавить в группу", url="https://t.me/gmoderator_bot?startgroup=botstart"))  # Замените на вашу ссылку
            for group in groups:
                group_id, group_name = group
                keyboard.row(types.InlineKeyboardButton(text=group_name, callback_data=f"group_reward_{group_id}"))

            bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=keyboard)

        else:

            keyboard = types.InlineKeyboardMarkup()
            if language == "en":
                add_button = types.InlineKeyboardButton("➕ Add to group", url="https://t.me/gmoderator_bot?startgroup=botstart")  # Замените на вашу ссылку
            else:
                add_button = types.InlineKeyboardButton("➕ Добавить в группу", url="https://t.me/gmoderator_bot?startgroup=botstart")  # Замените на вашу ссылку
            keyboard.add(add_button)

            bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=keyboard)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'Назад':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {call.from_user.id}\n"
            f"• Callback Data: {call.data}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    # Функция для получения имени группы и количества активных пользователей
def get_name_groups(group_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT chat_name, active_users FROM chats WHERE chat_id=?", (group_id,))
    groups = cursor.fetchall()
    conn.close()
    return groups

    # Функция для получения реферальных начислений и уровня
def get_user_groups_reward(group_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT bonus_count, level_count FROM creators WHERE chat_id=?", (group_id,))
    groups = cursor.fetchall()
    conn.close()
    return groups

# Обработчик кнопки Награда - конец

# Обработчик кнопки Настройки - начало
@bot.message_handler(func=lambda message: message.text in ["⚙️ Настройки", "⚙️ Settings"])
def settings_buttons_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            creator_id = message.from_user.id  # Предполагаемый идентификатор создателя

            language = get_user_language(chat_id)

            text_select = data['settings_text'][language]['select']
            text_add = data['settings_text'][language]['add']

            groups = get_user_groups(creator_id)

            if groups:
                # Если у пользователя есть группы, создаем кнопки для каждой группы
                keyboard = types.InlineKeyboardMarkup()
                if language == "en":
                    keyboard.row(types.InlineKeyboardButton("➕ Add to group", url="https://t.me/gmoderator_bot?startgroup=botstart"))  # Замените на вашу ссылку
                else:
                    keyboard.row(types.InlineKeyboardButton("➕ Добавить в группу", url="https://t.me/gmoderator_bot?startgroup=botstart"))  # Замените на вашу ссылку
                for group in groups:
                    group_id, group_name = group
                    keyboard.row(types.InlineKeyboardButton(text=group_name, callback_data=f"group_settings_{group_id}"))

                bot.send_message(chat_id, text=text_select, reply_markup=keyboard)

            else:
                # Если у пользователя нет групп, отправляем сообщение с просьбой добавить бота
                keyboard = types.InlineKeyboardMarkup()
                if language == "en":
                    add_button = types.InlineKeyboardButton("➕ Add to group", url="https://t.me/gmoderator_bot?startgroup=botstart")  # Замените на вашу ссылку
                else:
                    add_button = types.InlineKeyboardButton("➕ Добавить в группу", url="https://t.me/gmoderator_bot?startgroup=botstart")  # Замените на вашу ссылку
                keyboard.add(add_button)

                bot.send_message(chat_id, text=text_add, reply_markup=keyboard)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '⚙️ Настройки':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{message.from_user.username if message.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

        
        bot.reply_to(message, (
            "⚠️ Извините за неудобства! Возникла техническая проблема, "
            "но наш разработчик уже работают над ее решением. "
            "Пожалуйста, оставайтесь с нами, мы сообщим о любых обновлениях.\n\n"
            "⚠️ Sorry for the inconvenience! There was a technical problem, "
            "but our developer is already working on its solution. "
            "Please stay tuned, we will let you know about any updates."
        ))

    # Функция для получения списка групп создателя из базы данных
def get_user_groups(creator_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id, chat_name FROM chats WHERE creator_id=?", (creator_id,))
    groups = cursor.fetchall()
    conn.close()
    return groups

    # Функция для получения данных из группы возможных к изменению
def get_group_info(group_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT chat_name, language, earn, hi_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 FROM chats WHERE chat_id=?", (group_id,))
    group_info = cursor.fetchone()
    conn.close()
    return group_info

def create_settings_keyboard(language, group_id):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
    language_switch_text = data['settings_text'][group_language]['language_switch']['to']
    hi_text_swich_text = data['settings_text'][language]['hi_text_swich']
    if group_earn == "on_earn":
            earn_swich_text = data['settings_text'][language]['earn_swich']['on']
    elif group_earn == "off_earn":
            earn_swich_text = data['settings_text'][language]['earn_swich']['off']
    if good_text == "good_on":
            good_text_swich_text = data['settings_text'][language]['good_swich']['on']
    elif good_text == "good_off":
            good_text_swich_text = data['settings_text'][language]['good_swich']['off']
    if fuck == "on":
            fuck_swich_text = data['settings_text'][language]['fuck_swich']['on']
    elif fuck == "off":
            fuck_swich_text = data['settings_text'][language]['fuck_swich']['off']
    if spam == "on":
            spam_swich_text = data['settings_text'][language]['spam_swich']['on']
    elif spam == "off":
            spam_swich_text = data['settings_text'][language]['spam_swich']['off']
    if flood == "on":
            flood_swich_text = data['settings_text'][language]['flood_swich']['on']
    elif flood == "off":
            flood_swich_text = data['settings_text'][language]['flood_swich']['off']
    if link == "on":
            link_swich_text = data['settings_text'][language]['link_swich']['on']
    elif link == "off":
            link_swich_text = data['settings_text'][language]['link_swich']['off']
    key_add_text = data['settings_text'][language]['key_swich']['add']
    warn_edit_text = data['settings_text'][language]['warn_text']['edit']
    language_button = types.InlineKeyboardButton(text=language_switch_text, callback_data=f"switch_language_{group_id}")
    earn_button = types.InlineKeyboardButton(text=earn_swich_text, callback_data=f"switch_earn_{group_id}")
    hi_text_button = types.InlineKeyboardButton(text=hi_text_swich_text, callback_data=f"switch_hi_text_{group_id}")
    good_text_button = types.InlineKeyboardButton(text=good_text_swich_text, callback_data=f"switch_good_text_{group_id}")
    fuck_button = types.InlineKeyboardButton(text=fuck_swich_text, callback_data=f"switch_fuck_{group_id}")
    spam_button = types.InlineKeyboardButton(text=spam_swich_text, callback_data=f"switch_spam_{group_id}")
    flood_button = types.InlineKeyboardButton(text=flood_swich_text, callback_data=f"switch_flood_{group_id}")
    link_button = types.InlineKeyboardButton(text=link_swich_text, callback_data=f"switch_link_{group_id}")
    key_add_button = types.InlineKeyboardButton(text=key_add_text, callback_data=f"key_add_{group_id}")
    warn_edit_button = types.InlineKeyboardButton(text=warn_edit_text, callback_data=f"warn_edit_{group_id}")
        
    keyboard = types.InlineKeyboardMarkup()
    if language == "rus":
        back_button = types.InlineKeyboardButton("⬅️ Назад", callback_data="back_settings_to_groups")
    else:
        back_button = types.InlineKeyboardButton("⬅️ Back", callback_data="back_settings_to_groups")
    keyboard.add(language_button, earn_button)
    keyboard.add(hi_text_button, good_text_button)
    keyboard.add(fuck_button, spam_button)
    keyboard.add(flood_button, link_button)
    keyboard.add(key_add_button, warn_edit_button)
    keyboard.add(back_button)

    return keyboard


def create_warn_keyboard(language, group_id):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
    fuck = data['settings_text'][language]['5']
    spam = data['settings_text'][language]['6']
    flood = data['settings_text'][language]['7']
 
    fuck = types.InlineKeyboardButton(text=fuck, callback_data=f"fuck_warn_{group_id}")
    spam = types.InlineKeyboardButton(text=spam, callback_data=f"spam_warn_{group_id}")
    flood = types.InlineKeyboardButton(text=flood, callback_data=f"flood_warn_{group_id}")
        
    keyboard = types.InlineKeyboardMarkup()
    if language == "rus":
        back_button = types.InlineKeyboardButton("⬅️ Назад", callback_data=f"key_back_{group_id}")
    else:
        back_button = types.InlineKeyboardButton("⬅️ Back", callback_data=f"key_back_{group_id}")
    keyboard.add(fuck)
    keyboard.add(spam)
    keyboard.add(flood)
    keyboard.add(back_button)

    return keyboard


def get_time_text(duration, language):
    if duration == 5184000:
        return "🚫"
    elif duration == 5184:
        return "❌"
    else:
        hours = duration / 60 / 60
        if language == "rus":
            if hours in [1,21]:
                return "час"
            elif hours in [2,3,4,22,23,24]:
                return "часа"
            else:
                return "часов"
        else: 
            if hours in [1]:
                return "hour"
            else:
                return "hours"

def get_time_hour(duration):
    if duration == 5184000:
        return duration * 0
    elif duration == 5184:
        return duration * 0
    else:
        return duration / 60 / 60

def create_warn_message(language, group_name, language_info, group_id):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
    language = language_info


    dfl1 =  get_time_hour(duration_flood1)
    dfl2 =  get_time_hour(duration_flood2)
    dfl3 =  get_time_hour(duration_flood3)
    df1 =  get_time_hour(duration_fuck1)
    df2 =  get_time_hour(duration_fuck2)
    df3 =  get_time_hour(duration_fuck3)
    ds1 =  get_time_hour(duration_spam1)
    ds2 =  get_time_hour(duration_spam2)
    ds3 =  get_time_hour(duration_spam3)

    time_flood1 = get_time_text(duration_flood1, language)
    time_flood2 = get_time_text(duration_flood2, language)
    time_flood3 = get_time_text(duration_flood3, language)
    time_spam1 = get_time_text(duration_spam1, language)
    time_spam2 = get_time_text(duration_spam2, language)
    time_spam3 = get_time_text(duration_spam3, language)
    time_fuck1 = get_time_text(duration_fuck1, language)
    time_fuck2 = get_time_text(duration_fuck2, language)
    time_fuck3 = get_time_text(duration_fuck3, language)
    warn_text1 = data['settings_text'][language]['warn_text']['1']
    warn_text2 = data['settings_text'][language]['warn_text']['2']
    warn_text3 = data['settings_text'][language]['warn_text']['3']
    t10 = data['settings_text'][language]['10']
    message_text = f"{t10}\n\n<i>{warn_text1}</i>\n   [1⚠️ <b>{int(df1)}</b> {time_fuck1}] [2⚠️ <b>{int(df2)}</b> {time_fuck2}] [3⚠️ <b>{int(df3)}</b> {time_fuck3}]\n<i>{warn_text2}</i>\n   [1⚠️ <b>{int(ds1)}</b> {time_spam1}] [2⚠️ <b>{int(ds2)}</b> {time_spam2}] [3⚠️ <b>{int(ds3)}</b> {time_spam3}]\n<i>{warn_text3}</i>\n   [1⚠️ <b>{int(dfl1)}</b> {time_flood1}] [2⚠️ <b>{int(dfl2)}</b> {time_flood2}] [3⚠️ <b>{int(dfl3)}</b> {time_flood3}]"    

    return message_text


def create_settings_message(language, group_name, language_info, group_id):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
    language = language_info


    dfl1 =  get_time_hour(duration_flood1)
    dfl2 =  get_time_hour(duration_flood2)
    dfl3 =  get_time_hour(duration_flood3)
    df1 =  get_time_hour(duration_fuck1)
    df2 =  get_time_hour(duration_fuck2)
    df3 =  get_time_hour(duration_fuck3)
    ds1 =  get_time_hour(duration_spam1)
    ds2 =  get_time_hour(duration_spam2)
    ds3 =  get_time_hour(duration_spam3)

    time_flood1 = get_time_text(duration_flood1, language)
    time_flood2 = get_time_text(duration_flood2, language)
    time_flood3 = get_time_text(duration_flood3, language)
    time_spam1 = get_time_text(duration_spam1, language)
    time_spam2 = get_time_text(duration_spam2, language)
    time_spam3 = get_time_text(duration_spam3, language)
    time_fuck1 = get_time_text(duration_fuck1, language)
    time_fuck2 = get_time_text(duration_fuck2, language)
    time_fuck3 = get_time_text(duration_fuck3, language)

    # Проверяем, не превышает ли длина group_text 200 символов
    if len(group_text) > 200:
        group_text = group_text[:200]  # Обрезаем текст до 200 символов

    if group_earn == "on_earn":
        earn_text = data['settings_text'][language]['earn_swich']['succses']
    elif group_earn == "off_earn":
        earn_text = data['settings_text'][language]['earn_swich']['failure']
    if good_text == "good_on":
        good_text_text = data['settings_text'][language]['good_swich']['succses']
    elif good_text == "good_off":
        good_text_text = data['settings_text'][language]['good_swich']['failure']
    if fuck == "on":
        fuck_text = data['settings_text'][language]['fuck_swich']['succses']
    elif fuck == "off":
        fuck_text = data['settings_text'][language]['fuck_swich']['failure']
    if spam == "on":
        spam_text = data['settings_text'][language]['spam_swich']['succses']
    elif spam == "off":
        spam_text = data['settings_text'][language]['spam_swich']['failure']
    if flood == "on":
        flood_text = data['settings_text'][language]['flood_swich']['succses']
    elif flood == "off":
        flood_text = data['settings_text'][language]['flood_swich']['failure']
    if link == "on":
        link_text = data['settings_text'][language]['link_swich']['succses']
    elif link == "off":
        link_text = data['settings_text'][language]['link_swich']['failure']
    if key == "non":
        key_text = data['settings_text'][language]['key_swich']['no']
    else:
        keywords_list = key.split(',')  # Разделение строки ключевых слов по запятой
        key_text = ", ".join(keywords_list[:5])  # Взять только первые 20 слов и объединить их обратно в строку
    warn_text1 = data['settings_text'][language]['warn_text']['1']
    warn_text2 = data['settings_text'][language]['warn_text']['2']
    warn_text3 = data['settings_text'][language]['warn_text']['3']
            # Создаем кнопку для смены языка
    t1 = data['settings_text'][language]['1']
    t2 = data['settings_text'][language]['2']
    t3 = data['settings_text'][language]['3']
    t4 = data['settings_text'][language]['4']
    t5 = data['settings_text'][language]['5']
    t6 = data['settings_text'][language]['6']
    t7 = data['settings_text'][language]['7']
    t8 = data['settings_text'][language]['8']
    t9 = data['settings_text'][language]['9']
    t10 = data['settings_text'][language]['10']
    # Формируем текст сообщения с информацией о группе
    language_icon = '🇷🇺' if group_language == 'rus' else '🇺🇸'
    if language == "en":
        text = f"Customize the \"{group_name}\" group:"
    else:
        text = f"Настроить группу \"{group_name}\":"
    message_text = f"{text}\n\n{t1} {language_icon}\n\n{t2}\n   <i>{earn_text}</i>\n\n{t3} \n<i>\"@username, {group_text} ...\"</i>\n\n{t4}\n   <i>{good_text_text}</i>\n\n{t5}\n   <i>{fuck_text}</i>\n\n{t6}\n   <i>{spam_text}</i>\n\n{t7}\n   <i>{flood_text}</i>\n\n{t8}\n   <i>{link_text}</i>\n\n{t9}\n   <i>{key_text}</i> ...\n\n{t10}\n\n<i>{warn_text1}</i>\n   [1⚠️ <b>{int(df1)}</b> {time_fuck1}] [2⚠️ <b>{int(df2)}</b> {time_fuck2}] [3⚠️ <b>{int(df3)}</b> {time_fuck3}]\n<i>{warn_text2}</i>\n   [1⚠️ <b>{int(ds1)}</b> {time_spam1}] [2⚠️ <b>{int(ds2)}</b> {time_spam2}] [3⚠️ <b>{int(ds3)}</b> {time_spam3}]\n<i>{warn_text3}</i>\n   [1⚠️ <b>{int(dfl1)}</b> {time_flood1}] [2⚠️ <b>{int(dfl2)}</b> {time_flood2}] [3⚠️ <b>{int(dfl3)}</b> {time_flood3}]"    

    return message_text


# Обработчик нажатия на кнопку с настройками группы
@bot.callback_query_handler(func=lambda call: call.data.startswith("group_settings_"))
def group_settings_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        language_info = get_user_language(chat_id)
        
        if group_info:
            group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
            language = language_info

            # Создаем клавиатуру
            keyboard = create_settings_keyboard(language, group_id)

            # Создаем текст сообщения
            message_text = create_settings_message(language, group_name, language_info, group_id)
            
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")
        else:
            if language_info == "en":
                bot.answer_callback_query(call.id, "Group data not found - contact technical support!")
            else:
                bot.answer_callback_query(call.id, "Данные группы не найдены - обратитесь а тех поддержку!")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'group_settings_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="An error occurred. Please try again later.")


    # Обработчик нажатия на кнопку с назад для выбора какую группу настроить
@bot.callback_query_handler(func=lambda call: call.data.startswith("back_settings_to_groups"))
def group_back_settings_handler(call):
    try:
        chat_id = call.message.chat.id
        if call.message.chat.type == "private":
            creator_id = call.from_user.id  

            language = get_user_language(chat_id)
            text_select = data['settings_text'][language]['select']

            groups = get_user_groups(creator_id)

            if groups:
                # Если у пользователя есть группы, создаем кнопки для каждой группы
                keyboard = types.InlineKeyboardMarkup()
                if language == "en":
                    keyboard.row(types.InlineKeyboardButton("➕ Add to group", url="https://t.me/gmoderator_bot?startgroup=botstart"))  
                else:
                    keyboard.row(types.InlineKeyboardButton("➕ Добавить в группу", url="https://t.me/gmoderator_bot?startgroup=botstart"))  
                for group in groups:
                    group_id, group_name = group
                    keyboard.row(types.InlineKeyboardButton(text=group_name, callback_data=f"group_settings_{group_id}"))

                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=text_select, reply_markup=keyboard)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '⚙️ Настройки':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {call.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Отправка сообщения об ошибке в чат с разработчиком
        
        bot.send_message(chat_id, (
            "⚠️ Извините за неудобства! Возникла техническая проблема, "
            "но наш разработчик уже работают над ее решением. "
            "Пожалуйста, оставайтесь с нами, мы сообщим о любых обновлениях.\n\n"
            "⚠️ Sorry for the inconvenience! There was a technical problem, "
            "but our developer is already working on its solution. "
            "Please stay tuned, we will let you know about any updates."
        ))

    # Функция для получения языка группы из базы данных
def get_group_language(group_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM chats WHERE chat_id=?", (group_id,))
    language = cursor.fetchone()[0]
    conn.close()
    return language

        # Функция для обновления языка группы в базе данных
def update_group_language(group_id, new_language):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE chats SET language=? WHERE chat_id=?", (new_language, group_id))
    conn.commit()
    conn.close()
    print(f"Language for group {group_id} updated to {new_language}")  # Добавлено для отладки

    # Функция для обновления языка группы в базе данных
def update_group_hi_text(group_id, new_text):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE chats SET hi_text=? WHERE chat_id=?", (new_text, group_id))
    conn.commit()
    conn.close()

    # Обработчик нажатия на кнопку смены языка для группы
@bot.callback_query_handler(func=lambda call: call.data.startswith("switch_language_"))
def switch_group_language_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        group_info = get_group_info(group_id) 
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
        current_language = get_group_language(group_id)
        new_language = "en" if current_language == "rus" else "rus"
        language_info = get_user_language(chat_id)
        language = language_info
        new_text = None
        if group_text == "добро пожаловать! Проявляй активность и получай бонус GRAND!":
            new_text = "Welcome! Be active and earn GRAND bonus!"
        elif group_text == "Welcome! Be active and earn GRAND bonus!":
            new_text = "добро пожаловать! Проявляй активность и получай бонус GRAND!"
        else:
            pass

        update_group_language(group_id, new_language)
        if new_text:
            update_group_hi_text(group_id, new_text)

        keyboard = create_settings_keyboard(language, group_id)
        success_message = data['settings_text'][language]['language_switch']['succses']
            # Создаем текст сообщения
        message_text = create_settings_message(language, group_name, language_info, group_id)
                # Отправляем сообщение о смене начисления бонуса

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, success_message)

        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)
    
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_language_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    # Функция для получения языка группы из базы данных
def get_group_earn(group_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT earn FROM chats WHERE chat_id=?", (group_id,))
    earn = cursor.fetchone()[0]
    conn.close()
    return earn

    # Функция для обновления языка группы в базе данных
def update_group_earn(group_id, new_earn):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE chats SET earn=? WHERE chat_id=?", (new_earn, group_id))
    conn.commit()
    conn.close()

    # Обработчик нажатия на кнопку смены языка для группы
@bot.callback_query_handler(func=lambda call: call.data.startswith("switch_earn_"))
def switch_group_earn_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        current_earn = get_group_earn(group_id)
        # Определяем новое значение начисления бонуса
        new_earn = "off_earn" if current_earn == "on_earn" else "on_earn"
        language_info = get_user_language(chat_id)
        language = language_info
        update_group_earn(group_id, new_earn)
        
        if new_earn == "on_earn":
            success_message = data['settings_text'][language]['earn_swich']['succses']
        else:
            success_message = data['settings_text'][language]['earn_swich']['failure']
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_settings_keyboard(language, group_id)
        message_text = create_settings_message(language, group_name, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, success_message)
            
        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    # Функция для получения инфо о проф общении группы из базы данных
def get_group_good_text(group_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT good_text FROM chats WHERE chat_id=?", (group_id,))
    good_text = cursor.fetchone()[0]
    conn.close()
    return good_text

    # Функция для обновления инфо о проф общении группы в базе данных
def update_group_good_text(group_id, new_good_text):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE chats SET good_text=? WHERE chat_id=?", (new_good_text, group_id))
    conn.commit()
    conn.close()
    # Обработчик нажатия на кнопку смены фильтрации сообщений для группы
    
@bot.callback_query_handler(func=lambda call: call.data.startswith("switch_good_text_"))
def switch_group_good_text_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        current_good_text = get_group_good_text(group_id)
        new_good_text = "good_off" if current_good_text == "good_on" else "good_on"
        language_info = get_user_language(chat_id)
        language = language_info
        update_group_good_text(group_id, new_good_text)
        
        if new_good_text == "good_on":
            success_message = data['settings_text'][language]['good_swich']['succses']
        else:
            success_message = data['settings_text'][language]['good_swich']['failure']
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_settings_keyboard(language, group_id)
        message_text = create_settings_message(language, group_name, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, success_message)
            
        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_good_text_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    # Функция для получения инфо о мате группы из базы данных
def get_group_fuck(group_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT fuck FROM chats WHERE chat_id=?", (group_id,))
    good_text = cursor.fetchone()[0]
    conn.close()
    return good_text

    # Функция для обновления инфо о мате группы в базе данных
def update_group_fuck(group_id, new_fuck):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE chats SET fuck=? WHERE chat_id=?", (new_fuck, group_id))
    conn.commit()
    conn.close()

    
@bot.callback_query_handler(func=lambda call: call.data.startswith("switch_fuck_"))
def switch_group_fuck_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        current_fuck = get_group_fuck(group_id)
        new_fuck = "off" if current_fuck == "on" else "on"
        language_info = get_user_language(chat_id)
        language = language_info
        update_group_fuck(group_id, new_fuck)
        
        if new_fuck == "on":
            success_message = data['settings_text'][language]['fuck_swich']['succses']
        else:
            success_message = data['settings_text'][language]['fuck_swich']['failure']
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_settings_keyboard(language, group_id)
        message_text = create_settings_message(language, group_name, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, success_message)
            
        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_good_text_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    # Функция для получения инфо о спаме группы из базы данных
def get_group_spam(group_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT spam FROM chats WHERE chat_id=?", (group_id,))
    good_text = cursor.fetchone()[0]
    conn.close()
    return good_text

    # Функция для обновления инфо о спаме группы в базе данных
def update_group_spam(group_id, new_spam):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE chats SET spam=? WHERE chat_id=?", (new_spam, group_id))
    conn.commit()
    conn.close()

    
@bot.callback_query_handler(func=lambda call: call.data.startswith("switch_spam_"))
def switch_group_spam_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        current_spam = get_group_spam(group_id)
        new_spam = "off" if current_spam == "on" else "on"
        language_info = get_user_language(chat_id)
        language = language_info
        update_group_spam(group_id, new_spam)
        
        if new_spam == "on":
            success_message = data['settings_text'][language]['spam_swich']['succses']
        else:
            success_message = data['settings_text'][language]['spam_swich']['failure']
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_settings_keyboard(language, group_id)
        message_text = create_settings_message(language, group_name, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, success_message)
            
        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_good_text_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    # Функция для получения инфо о флуде группы из базы данных
def get_group_flood(group_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT flood FROM chats WHERE chat_id=?", (group_id,))
    good_text = cursor.fetchone()[0]
    conn.close()
    return good_text

    # Функция для обновления инфо о флуде группы в базе данных
def update_group_flood(group_id, new_flood):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE chats SET flood=? WHERE chat_id=?", (new_flood, group_id))
    conn.commit()
    conn.close()

    
@bot.callback_query_handler(func=lambda call: call.data.startswith("switch_flood_"))
def switch_group_flood_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        current_flood = get_group_flood(group_id)
        new_flood = "off" if current_flood == "on" else "on"
        language_info = get_user_language(chat_id)
        language = language_info
        update_group_flood(group_id, new_flood)
        
        if new_flood == "on":
            success_message = data['settings_text'][language]['flood_swich']['succses']
        else:
            success_message = data['settings_text'][language]['flood_swich']['failure']
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_settings_keyboard(language, group_id)
        message_text = create_settings_message(language, group_name, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, success_message)
            
        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_good_text_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    # Функция для получения инфо о ссылках группы из базы данных
def get_group_link(group_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT link FROM chats WHERE chat_id=?", (group_id,))
    good_text = cursor.fetchone()[0]
    conn.close()
    return good_text

    # Функция для обновления инфо о ссылках группы в базе данных
def update_group_link(group_id, new_link):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE chats SET link=? WHERE chat_id=?", (new_link, group_id))
    conn.commit()
    conn.close()

    
@bot.callback_query_handler(func=lambda call: call.data.startswith("switch_link_"))
def switch_group_flood_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        current_link = get_group_link(group_id)
        new_link = "off" if current_link == "on" else "on"
        language_info = get_user_language(chat_id)
        language = language_info
        update_group_link(group_id, new_link)
        
        if new_link == "on":
            success_message = data['settings_text'][language]['link_swich']['succses']
        else:
            success_message = data['settings_text'][language]['link_swich']['failure']
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_settings_keyboard(language, group_id)
        message_text = create_settings_message(language, group_name, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, success_message)
            
        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_good_text_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

# Функция установки статуса ожидания нового текста приветствия
def set_waiting_hi_text(chat_id, group_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO waiting_hi_text (chat_id, group_id) VALUES (?, ?)", (chat_id, group_id))
    conn.commit()
    conn.close()

# Функция получения статуса ожидания нового текста приветствия
def get_waiting_hi_text(chat_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT group_id FROM waiting_hi_text WHERE chat_id=?", (chat_id,))
    group_id = cursor.fetchone()
    conn.close()
    return group_id[0] if group_id else None

# Функция удаления статуса ожидания нового текста приветствия
def remove_waiting_hi_text(chat_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM waiting_hi_text WHERE chat_id=?", (chat_id,))
    conn.commit()
    conn.close()

# Функция для получения языка группы из базы данных
def get_group_hi_text(group_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT hi_text FROM chats WHERE chat_id=?", (group_id,))
    hi_text = cursor.fetchone()[0]
    conn.close()
    return hi_text

# Функция для обновления языка группы в базе данных
def update_group_hi_text(group_id, new_hi_text):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE chats SET hi_text=? WHERE chat_id=?", (new_hi_text, group_id))
    conn.commit()
    conn.close()

@bot.callback_query_handler(func=lambda call: call.data.startswith("switch_hi_text_"))
def switch_hi_text_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]

        # Определяем язык создателя группы
        language_creator = get_user_language(chat_id)
        
        instruction_text = data['settings_text'][language_creator]['hi_text_wait']
        # Отправляем сообщение с инструкцией
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=instruction_text)

        # Обновляем статус ожидания нового текста приветствия
        set_waiting_hi_text(chat_id, group_id)
    
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_hi_text_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

# Обработчик обновления текста приветствия
@bot.message_handler(func=lambda message: get_waiting_hi_text(message.chat.id) is not None)
def update_hi_text_handler(message):
    try:
        chat_id = message.chat.id
        username = message.from_user.username
        group_id = get_waiting_hi_text(chat_id)
        new_hi_text = message.text

        # Обновляем текст приветствия в базе данных
        update_group_hi_text(group_id, new_hi_text)

        # Удаляем статус ожидания нового текста приветствия
        remove_waiting_hi_text(chat_id)

        # Определяем язык создателя группы
        language_info = get_user_language(chat_id)
        language = language_info
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
        # Отправляем сообщение о смене языка
        keyboard = create_settings_keyboard(language, group_id)
        success_message = data['settings_text'][language]['hi_text_succses']
            # Создаем текст сообщения
        message_text = create_settings_message(language, group_name, language_info, group_id)
        bot.send_message(chat_id=chat_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, success_message)

        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обновлении текста привествия:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

# Функция для установки статуса ожидания нового текста приветствия
def set_waiting_keyadd(chat_id, group_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO waiting_keywords (chat_id, group_id) VALUES (?, ?)", (chat_id, group_id))
    conn.commit()
    conn.close()

# Функция получения статуса ожидания нового текста приветствия
def get_waiting_keyadd(chat_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT group_id FROM waiting_keywords WHERE chat_id=?", (chat_id,))
    group_id = cursor.fetchone()
    conn.close()
    return group_id[0] if group_id else None

# Функция удаления статуса ожидания нового текста приветствия
def remove_waiting_keyadd(chat_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM waiting_keywords WHERE chat_id=?", (chat_id,))
    conn.commit()
    conn.close()

# Функция для получения ключевых слов группы из базы данных
def get_group_keyadd(group_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT key FROM chats WHERE chat_id=?", (group_id,))
    key = cursor.fetchone()[0]
    conn.close()
    return key

# Функция для обновления языка группы в базе данных
def update_group_keyadd(group_id, new_key):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE chats SET key=? WHERE chat_id=?", (new_key, group_id))
    conn.commit()
    conn.close()

@bot.callback_query_handler(func=lambda call: call.data.startswith("key_add_"))
def switch_key_add_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
        # Определяем язык создателя группы
        language_creator = get_user_language(chat_id)
        if key == "non":
            new_text = data['settings_text'][language_creator]['key_swich']['wait']
            еxample_text = data['settings_text'][language_creator]['key_swich']['еxample']
            instruction_text = f"{new_text}\n\n<i>{еxample_text}</i>"
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=instruction_text, parse_mode="HTML")
        else:
            new_text = data['settings_text'][language_creator]['key_swich']['wait']
            keywords_list = key.split(',')  # Разделение строки ключевых слов по запятой
            limited_keywords = ", ".join(keywords_list[:20])  # Взять только первые 20 слов и объединить их обратно в строку
            warning_text = data['settings_text'][language_creator]['key_swich']['warning']
            button_text = data['settings_text'][language_creator]['key_swich']['del']
            keyboard = types.InlineKeyboardMarkup()
            back_button = types.InlineKeyboardButton("⬅️", callback_data=f"key_back_{group_id}")
            delete_button = types.InlineKeyboardButton(text=button_text, callback_data=f"key_delete_{group_id}")
            keyboard.add(back_button, delete_button)
            instruction_text = f"{new_text}\n\n<code>{limited_keywords}</code> ...\n\n{warning_text}"
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=instruction_text, reply_markup=keyboard, parse_mode="HTML")

        # Обновляем статус ожидания нового текста приветствия
        set_waiting_keyadd(chat_id, group_id)
    
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_hi_text_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("key_delete_"))
def switch_key_delete_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        language_info = get_user_language(chat_id)
        language = language_info
        new_key = "non"
        update_group_keyadd(group_id, new_key)
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
        # Удаляем статус ожидания нового текста приветствия
        remove_waiting_keyadd(chat_id)
        keyboard = create_settings_keyboard(language, group_id)
        success_message = data['settings_text'][language]['key_swich']['failure']
            # Создаем текст сообщения
        message_text = create_settings_message(language, group_name, language_info, group_id)
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, success_message)

        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)

    
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_hi_text_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)


@bot.callback_query_handler(func=lambda call: call.data.startswith("key_back_"))
def switch_key_back_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        language_info = get_user_language(chat_id)
        language = language_info
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
        # Определяем язык создателя группы

        keyboard = create_settings_keyboard(language, group_id)
        message_text = create_settings_message(language, group_name, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

    
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_hi_text_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

# Обработчик обновления текста приветствия
@bot.message_handler(func=lambda message: get_waiting_keyadd(message.chat.id) is not None)
def update_keyadd_handler(message):
    try:
        chat_id = message.chat.id
        username = message.from_user.username
        group_id = get_waiting_keyadd(chat_id)
        new_key = message.text

        # Обновляем текст приветствия в базе данных
        update_group_keyadd(group_id, new_key)

        # Удаляем статус ожидания нового текста приветствия
        remove_waiting_keyadd(chat_id)

        # Определяем язык создателя группы
        language_info = get_user_language(chat_id)
        language = language_info
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
        # Отправляем сообщение о смене языка
        keyboard = create_settings_keyboard(language, group_id)
        success_message = data['settings_text'][language]['hi_text_succses']
            # Создаем текст сообщения
        message_text = create_settings_message(language, group_name, language_info, group_id)
        bot.send_message(chat_id=chat_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, success_message)

        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обновлении текста привествия:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    # Обработчик нажатия на кнопку изменения наказаний
@bot.callback_query_handler(func=lambda call: call.data.startswith("warn_edit_"))
def warn_group_edit_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        current_earn = get_group_earn(group_id)
        # Определяем новое значение начисления бонуса
        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_keyboard(language, group_id)
        message_text = create_warn_message(language, group_name, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

def update_group_duration(group_id, column_name, new_value):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute(f"UPDATE chats SET {column_name}=? WHERE chat_id=?", (new_value, group_id))
    conn.commit()
    conn.close()

    # Обработчик нажатия на кнопку изменения наказаний вернутся к выбору где изменить наказание за предупреждение
@bot.callback_query_handler(func=lambda call: call.data.startswith("warn_back_"))
def warn_group_edit_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        current_earn = get_group_earn(group_id)
        # Определяем новое значение начисления бонуса
        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_keyboard(language, group_id)
        message_text = create_warn_message(language, group_name, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    # Функция для создания клавиатуры с вобором наказания
def create_hours_fuck_keyboard(language, group_id, duration_fuck, count):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

    warn_texts = {}
    for i in range(1, 25):
        warn_text = data['settings_text'][language]['warn_text'][f"{i}h"]
        if int(duration_fuck) / 3600 == i:
            warn_texts[f"warn_{i}h"] = f"{warn_text} ✅"
        else:
            warn_texts[f"warn_{i}h"] = warn_text

    buttons = []
    for key, text in warn_texts.items():
        button = types.InlineKeyboardButton(text=text, callback_data=f"fuckdur_{key}_{group_id}_{duration_fuck}_{count}")
        buttons.append(button)

    keyboard = types.InlineKeyboardMarkup()

    rows = [buttons[i:i+5] for i in range(0, len(buttons), 5)]
    for row in rows:
        keyboard.row(*row)

    if language == "rus":
        no_button = types.InlineKeyboardButton("❌", callback_data=f"no_fuck_{group_id}_{count}")
        ban_button = types.InlineKeyboardButton("🚫 Ban", callback_data=f"fuck_ban_{group_id}_{count}")
        back_button = types.InlineKeyboardButton("⬅️ Назад", callback_data=f"warn_fuck_back_{group_id}")
    else:
        no_button = types.InlineKeyboardButton("❌", callback_data=f"no_fuck_{group_id}_{count}")
        ban_button = types.InlineKeyboardButton("🚫 Ban", callback_data=f"fuck_ban_{group_id}_{count}")
        back_button = types.InlineKeyboardButton("⬅️ Back", callback_data=f"warn_fuck_back_{group_id}")

    keyboard.add(no_button, back_button, ban_button)

    return keyboard

@bot.callback_query_handler(func=lambda call: call.data.startswith('fuck_ban_'))
def handle_callback_query(call):
    try:
        # Получаем данные из callback_data
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-2]
        count = call.data.split("_")[-1]
        text_combination = f"duration_fuck{count}"
        newduration = "5184000"

        # Обновляем значение в базе данных
        update_group_duration(group_id, text_combination, newduration)

        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_fuck_count_keyboard(language, group_id)
        message_text = create_warn_fuck_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, "✅")

        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('no_fuck_'))
def handle_callback_query(call):
    try:
        # Получаем данные из callback_data
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-2]
        count = call.data.split("_")[-1]
        text_combination = f"duration_fuck{count}"
        newduration = "5184"

        # Обновляем значение в базе данных
        update_group_duration(group_id, text_combination, newduration)

        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_fuck_count_keyboard(language, group_id)
        message_text = create_warn_fuck_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, "✅")

        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith('fuckdur_'))
def handle_callback_query(call):
    try:
        # Получаем данные из callback_data
        chat_id = call.message.chat.id
        key = call.data.split("_")[-4]
        group_id = call.data.split("_")[-3]
        duration_fuck = call.data.split("_")[-2]
        count = call.data.split("_")[-1]
        duration = ''.join(filter(str.isdigit, key))
        text_combination = f"duration_fuck{count}"
        newduration = int(duration) * 60 * 60

        # Обновляем значение в базе данных
        update_group_duration(group_id, text_combination, newduration)

        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_fuck_count_keyboard(language, group_id)
        message_text = create_warn_fuck_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, "✅")

        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)



   # Функция для создания текста с когда выбрали изменить для мата
def create_warn_fuck_count_message(language, language_info, group_id):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
    language = language_info

    df1 =  get_time_hour(duration_fuck1)
    df2 =  get_time_hour(duration_fuck2)
    df3 =  get_time_hour(duration_fuck3)

    time_fuck1 = get_time_text(duration_fuck1, language)
    time_fuck2 = get_time_text(duration_fuck2, language)
    time_fuck3 = get_time_text(duration_fuck3, language)
    warn_text1 = data['settings_text'][language]['warn_text']['1']
    t10 = data['settings_text'][language]['10']
    message_text = f"{t10}\n\n<i>{warn_text1}</i>\n\n[1⚠️ <b>{int(df1)}</b> {time_fuck1}]\n\n[2⚠️ <b>{int(df2)}</b> {time_fuck2}]\n\n[3⚠️ <b>{int(df3)}</b> {time_fuck3}]"    

    return message_text

   # Функция для создания текста с подсказкой для выбора наказания
def create_edit_warn_fuck_count_message(language, language_info, group_id, df, time_fuck):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
    language = language_info

    warn_text1 = data['settings_text'][language]['warn_text']['1']
    warn_text2 = data['settings_text'][language]['warn_text']['4']
    warn_text3 = data['settings_text'][language]['warn_text']['5']
    t10 = data['settings_text'][language]['10']
    message_text = f"{t10}\n\n<i>{warn_text1}</i>\n\n[⚠️ <b>{int(float(df))}</b> {time_fuck}]\n\n<i>{warn_text2}</i>\n\n<i>{warn_text3}</i>"

    return message_text
    # Функция для создания клавиатуры с вобором предупреждения
def create_warn_fuck_count_keyboard(language, group_id):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
    df1 =  get_time_hour(duration_fuck1)
    df2 =  get_time_hour(duration_fuck2)
    df3 =  get_time_hour(duration_fuck3)
    count1 = "1"
    count2 = "2"
    count3 = "3"
    time_fuck1 = get_time_text(duration_fuck1, language)
    time_fuck2 = get_time_text(duration_fuck2, language)
    time_fuck3 = get_time_text(duration_fuck3, language)
    var1 = types.InlineKeyboardButton("1 ⚠️", callback_data=f"warn_fuck_count_{group_id}_{duration_fuck1}_{df1}_{time_fuck1}_{count1}")
    var2 = types.InlineKeyboardButton("2 ⚠️", callback_data=f"warn_fuck_count_{group_id}_{duration_fuck2}_{df2}_{time_fuck2}_{count2}")
    var3 = types.InlineKeyboardButton("3 ⚠️", callback_data=f"warn_fuck_count_{group_id}_{duration_fuck3}_{df3}_{time_fuck3}_{count3}")
    keyboard = types.InlineKeyboardMarkup()
    if language == "rus":
        back_button = types.InlineKeyboardButton("⬅️ Назад", callback_data=f"warn_back_{group_id}")
    else:
        back_button = types.InlineKeyboardButton("⬅️ Back", callback_data=f"warn_back_{group_id}")
    keyboard.row(var1, var2, var3)
    keyboard.add(back_button)

    return keyboard
# Обработчика вернуться к выбору предупреждения для мата
@bot.callback_query_handler(func=lambda call: call.data.startswith("warn_fuck_back_"))
def warn_group_edit_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        current_earn = get_group_earn(group_id)
        # Определяем новое значение начисления бонуса
        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_fuck_count_keyboard(language, group_id)
        message_text = create_warn_fuck_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    #Обработчик выбора настройки за какое предупреждение изменить наказание
@bot.callback_query_handler(func=lambda call: call.data.startswith("fuck_warn_"))
def warn_group_edit_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        current_earn = get_group_earn(group_id)
        # Определяем новое значение начисления бонуса
        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_fuck_count_keyboard(language, group_id)
        message_text = create_warn_fuck_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    # Обработчик выбора наказания за выбрнанное предупреждение
@bot.callback_query_handler(func=lambda call: call.data.startswith("warn_fuck_count_"))
def warn_group_edit_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-5]
        duration_fuck = call.data.split("_")[-4]  # Изменение здесь
        df = call.data.split("_")[-3]  # Изменение здесь
        time_fuck = call.data.split("_")[-2]  # Изменение здесь
        count = call.data.split("_")[-1]
        current_earn = get_group_earn(group_id)
        # Определяем новое значение начисления бонуса
        language_info = get_user_language(chat_id)
        language = language_info

        keyboard = create_hours_fuck_keyboard(language, group_id, duration_fuck, count)  # Изменение здесь
        message_text = create_edit_warn_fuck_count_message(language, language_info, group_id, df, time_fuck)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    # Функция для создания клавиатуры с вобором наказания
def create_hours_spam_keyboard(language, group_id, duration_spam, count):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

    warn_texts = {}
    for i in range(1, 25):
        warn_text = data['settings_text'][language]['warn_text'][f"{i}h"]
        if int(duration_spam) / 3600 == i:
            warn_texts[f"warn_{i}h"] = f"{warn_text} ✅"
        else:
            warn_texts[f"warn_{i}h"] = warn_text

    buttons = []
    for key, text in warn_texts.items():
        button = types.InlineKeyboardButton(text=text, callback_data=f"spamdur_{key}_{group_id}_{duration_spam}_{count}")
        buttons.append(button)

    keyboard = types.InlineKeyboardMarkup()

    rows = [buttons[i:i+5] for i in range(0, len(buttons), 5)]
    for row in rows:
        keyboard.row(*row)

    if language == "rus":
        no_button = types.InlineKeyboardButton("❌", callback_data=f"no_spam_{group_id}_{count}")
        ban_button = types.InlineKeyboardButton("🚫 Ban", callback_data=f"spam_ban_{group_id}_{count}")
        back_button = types.InlineKeyboardButton("⬅️ Назад", callback_data=f"warn_spam_back_{group_id}")
    else:
        no_button = types.InlineKeyboardButton("❌", callback_data=f"no_spam_{group_id}_{count}")
        ban_button = types.InlineKeyboardButton("🚫 Ban", callback_data=f"spam_ban_{group_id}_{count}")
        back_button = types.InlineKeyboardButton("⬅️ Back", callback_data=f"warn_spam_back_{group_id}")

    keyboard.add(no_button, back_button, ban_button)

    return keyboard

@bot.callback_query_handler(func=lambda call: call.data.startswith('spam_ban_'))
def handle_callback_query(call):
    try:
        # Получаем данные из callback_data
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-2]
        count = call.data.split("_")[-1]
        text_combination = f"duration_spam{count}"
        newduration = "5184000"

        # Обновляем значение в базе данных
        update_group_duration(group_id, text_combination, newduration)

        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_spam_count_keyboard(language, group_id)
        message_text = create_warn_spam_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, "✅")

        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('no_spam_'))
def handle_callback_query(call):
    try:
        # Получаем данные из callback_data
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-2]
        count = call.data.split("_")[-1]
        text_combination = f"duration_spam{count}"
        newduration = "5184"

        # Обновляем значение в базе данных
        update_group_duration(group_id, text_combination, newduration)

        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_spam_count_keyboard(language, group_id)
        message_text = create_warn_spam_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, "✅")

        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith('spamdur_'))
def handle_callback_query(call):
    try:
        # Получаем данные из callback_data
        chat_id = call.message.chat.id
        key = call.data.split("_")[-4]
        group_id = call.data.split("_")[-3]
        duration_fuck = call.data.split("_")[-2]
        count = call.data.split("_")[-1]
        duration = ''.join(filter(str.isdigit, key))
        text_combination = f"duration_spam{count}"
        newduration = int(duration) * 60 * 60

        # Обновляем значение в базе данных
        update_group_duration(group_id, text_combination, newduration)

        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_spam_count_keyboard(language, group_id)
        message_text = create_warn_spam_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, "✅")

        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)



   # Функция для создания текста с когда выбрали изменить для мата
def create_warn_spam_count_message(language, language_info, group_id):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
    language = language_info

    df1 =  get_time_hour(duration_spam1)
    df2 =  get_time_hour(duration_spam2)
    df3 =  get_time_hour(duration_spam3)

    time_fuck1 = get_time_text(duration_spam1, language)
    time_fuck2 = get_time_text(duration_spam2, language)
    time_fuck3 = get_time_text(duration_spam3, language)
    warn_text1 = data['settings_text'][language]['warn_text']['2']
    t10 = data['settings_text'][language]['10']
    message_text = f"{t10}\n\n<i>{warn_text1}</i>\n\n[1⚠️ <b>{int(df1)}</b> {time_fuck1}]\n\n[2⚠️ <b>{int(df2)}</b> {time_fuck2}]\n\n[3⚠️ <b>{int(df3)}</b> {time_fuck3}]"    

    return message_text

   # Функция для создания текста с подсказкой для выбора наказания
def create_edit_warn_spam_count_message(language, language_info, group_id, df, time_fuck):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
    language = language_info

    warn_text1 = data['settings_text'][language]['warn_text']['2']
    warn_text2 = data['settings_text'][language]['warn_text']['4']
    warn_text3 = data['settings_text'][language]['warn_text']['5']
    t10 = data['settings_text'][language]['10']
    message_text = f"{t10}\n\n<i>{warn_text1}</i>\n\n[⚠️ <b>{int(float(df))}</b> {time_fuck}]\n\n<i>{warn_text2}</i>\n\n<i>{warn_text3}</i>"

    return message_text
    # Функция для создания клавиатуры с вобором предупреждения
def create_warn_spam_count_keyboard(language, group_id):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
    df1 =  get_time_hour(duration_spam1)
    df2 =  get_time_hour(duration_spam2)
    df3 =  get_time_hour(duration_spam3)
    count1 = "1"
    count2 = "2"
    count3 = "3"
    time_fuck1 = get_time_text(duration_spam1, language)
    time_fuck2 = get_time_text(duration_spam2, language)
    time_fuck3 = get_time_text(duration_spam3, language)
    var1 = types.InlineKeyboardButton("1 ⚠️", callback_data=f"warn_spam_count_{group_id}_{duration_spam1}_{df1}_{time_fuck1}_{count1}")
    var2 = types.InlineKeyboardButton("2 ⚠️", callback_data=f"warn_spam_count_{group_id}_{duration_spam2}_{df2}_{time_fuck2}_{count2}")
    var3 = types.InlineKeyboardButton("3 ⚠️", callback_data=f"warn_spam_count_{group_id}_{duration_spam3}_{df3}_{time_fuck3}_{count3}")
    keyboard = types.InlineKeyboardMarkup()
    if language == "rus":
        back_button = types.InlineKeyboardButton("⬅️ Назад", callback_data=f"warn_back_{group_id}")
    else:
        back_button = types.InlineKeyboardButton("⬅️ Back", callback_data=f"warn_back_{group_id}")
    keyboard.row(var1, var2, var3)
    keyboard.add(back_button)

    return keyboard
# Обработчика вернуться к выбору предупреждения для мата
@bot.callback_query_handler(func=lambda call: call.data.startswith("warn_spam_back_"))
def warn_group_edit_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        current_earn = get_group_earn(group_id)
        # Определяем новое значение начисления бонуса
        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_spam_count_keyboard(language, group_id)
        message_text = create_warn_spam_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    #Обработчик выбора настройки за какое предупреждение изменить наказание
@bot.callback_query_handler(func=lambda call: call.data.startswith("spam_warn_"))
def warn_group_edit_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        current_earn = get_group_earn(group_id)
        # Определяем новое значение начисления бонуса
        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_spam_count_keyboard(language, group_id)
        message_text = create_warn_spam_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    # Обработчик выбора наказания за выбрнанное предупреждение
@bot.callback_query_handler(func=lambda call: call.data.startswith("warn_spam_count_"))
def warn_group_edit_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-5]
        duration_spam = call.data.split("_")[-4]  # Изменение здесь
        df = call.data.split("_")[-3]  # Изменение здесь
        time_fuck = call.data.split("_")[-2]  # Изменение здесь
        count = call.data.split("_")[-1]
        current_earn = get_group_earn(group_id)
        # Определяем новое значение начисления бонуса
        language_info = get_user_language(chat_id)
        language = language_info

        keyboard = create_hours_spam_keyboard(language, group_id, duration_spam, count)  # Изменение здесь
        message_text = create_edit_warn_spam_count_message(language, language_info, group_id, df, time_fuck)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    # Функция для создания клавиатуры с вобором наказания
def create_hours_flood_keyboard(language, group_id, duration_flood, count):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

    warn_texts = {}
    for i in range(1, 25):
        warn_text = data['settings_text'][language]['warn_text'][f"{i}h"]
        if int(duration_flood) / 3600 == i:
            warn_texts[f"warn_{i}h"] = f"{warn_text} ✅"
        else:
            warn_texts[f"warn_{i}h"] = warn_text

    buttons = []
    for key, text in warn_texts.items():
        button = types.InlineKeyboardButton(text=text, callback_data=f"flooddur_{key}_{group_id}_{duration_flood}_{count}")
        buttons.append(button)

    keyboard = types.InlineKeyboardMarkup()

    rows = [buttons[i:i+5] for i in range(0, len(buttons), 5)]
    for row in rows:
        keyboard.row(*row)

    if language == "rus":
        no_button = types.InlineKeyboardButton("❌", callback_data=f"no_flood_{group_id}_{count}")
        ban_button = types.InlineKeyboardButton("🚫 Ban", callback_data=f"flood_ban_{group_id}_{count}")
        back_button = types.InlineKeyboardButton("⬅️ Назад", callback_data=f"warn_flood_back_{group_id}")
    else:
        no_button = types.InlineKeyboardButton("❌", callback_data=f"no_flood_{group_id}_{count}")
        ban_button = types.InlineKeyboardButton("🚫 Ban", callback_data=f"flood_ban_{group_id}_{count}")
        back_button = types.InlineKeyboardButton("⬅️ Back", callback_data=f"warn_flood_back_{group_id}")

    keyboard.add(no_button, back_button, ban_button)

    return keyboard

@bot.callback_query_handler(func=lambda call: call.data.startswith('flood_ban_'))
def handle_callback_query(call):
    try:
        # Получаем данные из callback_data
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-2]
        count = call.data.split("_")[-1]
        text_combination = f"duration_flood{count}"
        newduration = "5184000"

        # Обновляем значение в базе данных
        update_group_duration(group_id, text_combination, newduration)

        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_flood_count_keyboard(language, group_id)
        message_text = create_warn_flood_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, "✅")

        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('no_flood_'))
def handle_callback_query(call):
    try:
        # Получаем данные из callback_data
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-2]
        count = call.data.split("_")[-1]
        text_combination = f"duration_flood{count}"
        newduration = "5184"

        # Обновляем значение в базе данных
        update_group_duration(group_id, text_combination, newduration)

        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_flood_count_keyboard(language, group_id)
        message_text = create_warn_flood_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, "✅")

        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
    
@bot.callback_query_handler(func=lambda call: call.data.startswith('flooddur_'))
def handle_callback_query(call):
    try:
        # Получаем данные из callback_data
        chat_id = call.message.chat.id
        key = call.data.split("_")[-4]
        group_id = call.data.split("_")[-3]
        duration_flood = call.data.split("_")[-2]
        count = call.data.split("_")[-1]
        duration = ''.join(filter(str.isdigit, key))
        text_combination = f"duration_flood{count}"
        newduration = int(duration) * 60 * 60

        # Обновляем значение в базе данных
        update_group_duration(group_id, text_combination, newduration)

        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_flood_count_keyboard(language, group_id)
        message_text = create_warn_flood_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

        sent_message = bot.send_message(chat_id, "✅")

        time.sleep(1)

        bot.delete_message(chat_id, sent_message.message_id)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)



   # Функция для создания текста с когда выбрали изменить для мата
def create_warn_flood_count_message(language, language_info, group_id):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
    language = language_info

    df1 =  get_time_hour(duration_flood1)
    df2 =  get_time_hour(duration_flood2)
    df3 =  get_time_hour(duration_flood3)

    time_fuck1 = get_time_text(duration_flood1, language)
    time_fuck2 = get_time_text(duration_flood2, language)
    time_fuck3 = get_time_text(duration_flood3, language)
    warn_text1 = data['settings_text'][language]['warn_text']['3']
    t10 = data['settings_text'][language]['10']
    message_text = f"{t10}\n\n<i>{warn_text1}</i>\n\n[1⚠️ <b>{int(df1)}</b> {time_fuck1}]\n\n[2⚠️ <b>{int(df2)}</b> {time_fuck2}]\n\n[3⚠️ <b>{int(df3)}</b> {time_fuck3}]"    

    return message_text

   # Функция для создания текста с подсказкой для выбора наказания
def create_edit_warn_flood_count_message(language, language_info, group_id, df, time_fuck):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
    language = language_info

    warn_text1 = data['settings_text'][language]['warn_text']['3']
    warn_text2 = data['settings_text'][language]['warn_text']['4']
    warn_text3 = data['settings_text'][language]['warn_text']['5']
    t10 = data['settings_text'][language]['10']
    message_text = f"{t10}\n\n<i>{warn_text1}</i>\n\n[⚠️ <b>{int(float(df))}</b> {time_fuck}]\n\n<i>{warn_text2}</i>\n\n<i>{warn_text3}</i>"

    return message_text
    # Функция для создания клавиатуры с вобором предупреждения
def create_warn_flood_count_keyboard(language, group_id):
    group_info = get_group_info(group_id)
    group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info
    df1 =  get_time_hour(duration_flood1)
    df2 =  get_time_hour(duration_flood2)
    df3 =  get_time_hour(duration_flood3)
    count1 = "1"
    count2 = "2"
    count3 = "3"
    time_fuck1 = get_time_text(duration_flood1, language)
    time_fuck2 = get_time_text(duration_flood2, language)
    time_fuck3 = get_time_text(duration_flood3, language)
    var1 = types.InlineKeyboardButton("1 ⚠️", callback_data=f"warn_flood_count_{group_id}_{duration_flood1}_{df1}_{time_fuck1}_{count1}")
    var2 = types.InlineKeyboardButton("2 ⚠️", callback_data=f"warn_flood_count_{group_id}_{duration_flood2}_{df2}_{time_fuck2}_{count2}")
    var3 = types.InlineKeyboardButton("3 ⚠️", callback_data=f"warn_flood_count_{group_id}_{duration_flood3}_{df3}_{time_fuck3}_{count3}")
    keyboard = types.InlineKeyboardMarkup()
    if language == "rus":
        back_button = types.InlineKeyboardButton("⬅️ Назад", callback_data=f"warn_back_{group_id}")
    else:
        back_button = types.InlineKeyboardButton("⬅️ Back", callback_data=f"warn_back_{group_id}")
    keyboard.row(var1, var2, var3)
    keyboard.add(back_button)

    return keyboard
# Обработчика вернуться к выбору предупреждения для мата
@bot.callback_query_handler(func=lambda call: call.data.startswith("warn_flood_back_"))
def warn_group_edit_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        current_earn = get_group_earn(group_id)
        # Определяем новое значение начисления бонуса
        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_flood_count_keyboard(language, group_id)
        message_text = create_warn_flood_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    #Обработчик выбора настройки за какое предупреждение изменить наказание
@bot.callback_query_handler(func=lambda call: call.data.startswith("flood_warn_"))
def warn_group_edit_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-1]
        current_earn = get_group_earn(group_id)
        # Определяем новое значение начисления бонуса
        language_info = get_user_language(chat_id)
        language = language_info
        # Получаем информацию о группе из базы данных
        group_info = get_group_info(group_id)
        group_name, group_language, group_earn, group_text, good_text, fuck, spam, flood, link, key, duration_flood1, duration_flood2, duration_flood3, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3 = group_info

        keyboard = create_warn_flood_count_keyboard(language, group_id)
        message_text = create_warn_flood_count_message(language, language_info, group_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    # Обработчик выбора наказания за выбрнанное предупреждение
@bot.callback_query_handler(func=lambda call: call.data.startswith("warn_flood_count_"))
def warn_group_edit_handler(call):
    try:
        chat_id = call.message.chat.id
        group_id = call.data.split("_")[-5]
        duration_spam = call.data.split("_")[-4]  # Изменение здесь
        df = call.data.split("_")[-3]  # Изменение здесь
        time_fuck = call.data.split("_")[-2]  # Изменение здесь
        count = call.data.split("_")[-1]
        current_earn = get_group_earn(group_id)
        # Определяем новое значение начисления бонуса
        language_info = get_user_language(chat_id)
        language = language_info

        keyboard = create_hours_flood_keyboard(language, group_id, duration_spam, count)  # Изменение здесь
        message_text = create_edit_warn_flood_count_message(language, language_info, group_id, df, time_fuck)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=message_text, reply_markup=keyboard, parse_mode="HTML")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'switch_earn_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

# Обработчик кнопки Настройки - конец




    # Отправляем сообщение о том, что пользователь был предупрежден



def connect_db():
    """
    Функция для подключения к базе данных chat_data.db.

    Returns:
        connect_to_dbion: Объект соединения с базой данных.
    """
    try:
        conn = connect_to_db('chat_data.db')
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

#Функция получения id по username в чате
def get_user_id_by_username(username, chat_id):
    conn = connect_db()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_username = ? AND chat_id = ?", (username, chat_id))
        result = cursor.fetchone()
        if result:
            return result[0]  # Возвращаем ID пользователя
        else:
            return None
    except Exception as e:
        print(f"Error getting user ID by username: {e}")
        return None
    finally:
        conn.close()
    #Функция для которая снимает 1 предупреждение с пользователя
def delete_warncount_by_username(username, chat_id):
    conn = connect_db()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT warn_count FROM users WHERE user_username = ? AND chat_id = ?", (username, chat_id))
        result = cursor.fetchone()
        if result:
            current_count = result[0]
            if current_count > 0:
                new_count = max(0, current_count - 1)
                cursor.execute("UPDATE users SET warn_count = ? WHERE user_username = ? AND chat_id = ?", (new_count, username, chat_id))
                conn.commit()
                return new_count
            else:
                return 0  # Если уже 0, ничего не меняем и возвращаем 0
        else:
            return None
    except Exception as e:
        print(f"Error getting or updating warn count: {e}")
        return None
    finally:
        conn.close()

    #Функция для которая снимает 1 предупреждение с группы
def delete_warncount_by_group(chat_id):
    conn = connect_db()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT warn_count FROM chats WHERE chat_id = ?", (chat_id,))
        result = cursor.fetchone()
        if result:
            current_count = result[0]
            if current_count > 0:
                new_count = max(0, current_count - 1)
                cursor.execute("UPDATE chats SET warn_count = ? WHERE chat_id = ?", (new_count, chat_id))
                conn.commit()
                return new_count
            else:
                return 0  # Если уже 0, ничего не меняем и возвращаем 0
        else:
            return None
    except Exception as e:
        print(f"Error getting or updating warn count: {e}")
        return None
    finally:
        conn.close()


    # Функция для которая добавляет 1 предупреждение пользователю
def add_warncount_by_username(username, chat_id):
    conn = connect_db()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT warn_count FROM users WHERE user_username = ? AND chat_id = ?", (username, chat_id))
        result = cursor.fetchone()
        if result:
            current_count = result[0]
            if current_count < 3:  # Проверяем, что количество предупреждений меньше 3
                new_count = current_count + 1
                cursor.execute("UPDATE users SET warn_count = ? WHERE user_username = ? AND chat_id = ?", (new_count, username, chat_id))
                conn.commit()
                return new_count
            else:
                return 3  # Если уже 3 предупреждения, возвращаем 3, ничего не меняем
        else:
            return None
    except Exception as e:
        print(f"Error getting or updating warn count: {e}")
        return None
    finally:
        conn.close()

    # Функция для которая добавляет 1 предупреждение группе
def add_warncount_by_group(chat_id):
    conn = connect_db()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT warn_count FROM chats WHERE chat_id = ?", (chat_id,))
        result = cursor.fetchone()
        if result:
            current_count = result[0]
            new_count = current_count + 1
            cursor.execute("UPDATE chats SET warn_count = ? WHERE chat_id = ?", (new_count, chat_id))
            conn.commit()
            return new_count
        else:
            return None
    except Exception as e:
        print(f"Error getting or updating warn count: {e}")
        return None
    finally:
        conn.close()


def format_duration(seconds):
    periods = [
        ('день', 60 * 60 * 24),
        ('час', 60 * 60),
        ('минуту', 60)
    ]
    result = []
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 1:
                result.append(f"{period_value} {period_name}")
            else:
                result.append(f"{period_value} {period_name}{'а' if period_value > 1 else ''}")
    return ', '.join(result)

# Функция для получения идентификаторов сообщений для указанного чата
def get_message_ids(chat_id):
    # Создание нового соединения с базой данных
    with connect_to_db("messages.db") as conn:
        # Создание курсора для выполнения запроса
        cursor = conn.cursor()
        # Выполнение SQL-запроса для получения идентификаторов сообщений
        cursor.execute("SELECT message_id FROM messages WHERE chat_id=?", (chat_id,))
        # Получение результата запроса
        return cursor.fetchall()

# Функция для удаления сообщения из базы данных
def delete_message(chat_id, message_id):
    # Создание нового соединения с базой данных
    with connect_to_db("messages.db") as conn:
        # Создание курсора для выполнения запроса
        cursor = conn.cursor()
        # Выполнение SQL-запроса для удаления сообщения
        cursor.execute("DELETE FROM messages WHERE chat_id=? AND message_id=?", (chat_id, message_id))
        # Фиксация изменений в базе данных
        conn.commit()

# Функция для получения информации о статистике группы по chat_id
def get_group_statistics_by_chat_id(chat_id):
    try:
        # Подключение к базе данных
        conn = connect_to_db('chat_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT chat_id, chat_name, creator_id, creator_username, active_users, language, message_count, bonus_count, word_count, warn_count, earn, hi_text, good_text FROM chats WHERE chat_id=?", (chat_id,))
        group_statistics = cursor.fetchall()
        
        # Проверка на пустоту
        if not group_statistics:
            return "Информации о данной группе нет в базе данных."
        
        return group_statistics
    except Exception as e:
        return f"⚠️ Произошла ошибка при получении статистики группы:\n• {type(e).__name__}: {e}"
    finally:
        # Закрытие подключения к базе данных
        if conn:
            conn.close()

# Функция для получения информации о статистике пользователя по chat_id и user_id
def get_user_statistics_by_chat_id(user_id, chat_id):
    try:
        # Подключение к базе данных
        conn = connect_to_db('chat_data.db')
        cursor = conn.cursor()

        cursor.execute("SELECT user_username, message_count, bonus_count, word_count, warn_count FROM users WHERE chat_id=? AND user_id=?", (chat_id, user_id,))
        user_statistics = cursor.fetchone()
        
        # Проверка на пустоту
        if not user_statistics:
            return "Информации о пользователе нет в базе данных."
        
        return user_statistics
    except Exception as e:
        return f"⚠️ Произошла ошибка при получении статистики группы:\n• {type(e).__name__}: {e}"
    finally:
        # Закрытие подключения к базе данных
        if conn:
            conn.close()

#Функции для ручной модерации конец

#Команды ручной модерации начало

#Обработчик команды `/unwarn`, которая снимает ограничения с пользователя.
@bot.message_handler(commands=['unwarn'])
def unwarn_user(message):
    try:
        chat_id = message.chat.id
        # Проверяем, что чат является группой или супергруппой
        if message.chat.type not in ['group', 'supergroup']:
            return

        language = get_chat_language(chat_id)
        only_admin = data['commands'][language]['allow_text']
        bott = data['commands'][language]['bot_text']
        error = data['commands'][language]['error_text']
        formate = data['commands'][language]['unwarn']['formate']
        erroruser = data['commands'][language]['unwarn']['error']
        allow = data['commands'][language]['unwarn']['allow']
        # Проверяем, что отправитель команды является администратором или создателем чата
        if message.from_user.id not in [chat_member.user.id for chat_member in bot.get_chat_administrators(chat_id)]:
            bot.send_message(chat_id, text=only_admin)
            return

        # Если сообщение является ответом на другое сообщение, извлекаем username из него
        if message.reply_to_message and message.reply_to_message.from_user:
            username = message.reply_to_message.from_user.username
        else:
            # Получаем username из аргумента команды и удаляем символ "@", если присутствует
            if len(message.text.split()) == 2:
                username = message.text.split()[1].lstrip('@')
            else:
                bot.send_message(chat_id, text=formate)
                return

        # Проверяем, что команда не применяется к боту
        if username == bot.get_me().username:
            bot.send_message(chat_id, text=bott)
            return

        # Пытаемся найти пользователя по username
        user_id = get_user_id_by_username(username, chat_id)
        user_status = bot.get_chat_member(chat_id, user_id).status
        # Проверяем, что найденный пользователь не является администратором или создателем чата
        if user_status not in ('creator'):
            delete_warncount_by_username(username, chat_id)
            delete_warncount_by_group(chat_id)
            bot.send_message(chat_id, f"{allow} @{username}")
        else:
            delete_warncount_by_username(username, chat_id)
            delete_warncount_by_group(chat_id)
            bot.send_message(chat_id, f"{allow} @{username}")
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при снятии предупреждения пользователя:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        bot.send_message(chat_id, text=erroruser)


# Обработчик команды `/warn`, которая предупреждает.
@bot.message_handler(commands=['warn'])
def warn_user(message):
    try:
        chat_id = message.chat.id

        # Проверяем, что чат является группой или супергруппой
        if message.chat.type not in ['group', 'supergroup']:
            return

        language = get_chat_language(chat_id)

        only_admin = data['commands'][language]['allow_text']
        bott = data['commands'][language]['bot_text']
        error = data['commands'][language]['error_text']
        formate = data['commands'][language]['warn']['formate']
        erroruser = data['commands'][language]['warn']['error']
        allow = data['commands'][language]['warn']['allow']
        allow_reason = data['commands'][language]['warn']['reason']
        # Проверяем, что отправитель команды является администратором или создателем чата
        if message.from_user.id not in [chat_member.user.id for chat_member in bot.get_chat_administrators(chat_id)]:
            bot.send_message(chat_id, text=only_admin)
            return

        # Если сообщение является ответом на другое сообщение, извлекаем username из него
        if message.reply_to_message and message.reply_to_message.from_user:
            username = message.reply_to_message.from_user.username
            reason = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else None
        else:
            # Получаем username из аргумента команды и удаляем символ "@", если присутствует
            if len(message.text.split()) > 1:
                username = message.text.split()[1].lstrip('@')
                reason = message.text.split(' ', 2)[2] if len(message.text.split()) > 2 else None
            else:
                bot.send_message(chat_id, text=formate)
                return

        # Проверяем, что команда не применяется к боту
        if username == bot.get_me().username:
            bot.send_message(chat_id, text=bott)
            return

        # Пытаемся найти пользователя по username
        user_id = get_user_id_by_username(username, chat_id)
        user_status = bot.get_chat_member(chat_id, user_id).status
        # Проверяем, что найденный пользователь не является администратором или создателем чата
        if user_status not in ('creator'):
            add_warncount_by_username(username, chat_id)
            add_warncount_by_group(chat_id)
            if reason:
                bot.send_message(chat_id, f"@{username}! {allow_reason} {reason}")
            else:
                bot.send_message(chat_id, f"@{username}! {allow_reason}")
        else:
            bot.send_message(chat_id, text=error)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при выдаче предупреждения пользователю:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        bot.send_message(chat_id, text=erroruser)




# Обработчик команды `/mute`, которая блокирует пользователя на определенный период времени
@bot.message_handler(commands=['mute'])
def mute_user(message):
    try:
        chat_id = message.chat.id

        # Проверяем, что чат является группой или супергруппой
        if message.chat.type not in ['group', 'supergroup']:
            return

        language = get_chat_language(chat_id)

        only_admin = data['commands'][language]['allow_text']
        bott = data['commands'][language]['bot_text']
        error = data['commands'][language]['error_text']
        formate = data['commands'][language]['mute']['formate']
        time_formate = data['commands'][language]['mute']['time_formate']
        erroruser = data['commands'][language]['mute']['error']
        allow = data['commands'][language]['mute']['allow']
        ban = data['commands'][language]['mute']['ban_formate']
        # Проверяем, что отправитель команды является администратором или создателем чата
        if message.from_user.id not in [chat_member.user.id for chat_member in bot.get_chat_administrators(chat_id)]:
            bot.send_message(chat_id, text=only_admin)
            return

        # Проверяем, что команда имеет аргументы
        if len(message.text.split()) < 2:
            if not message.reply_to_message:
                bot.send_message(chat_id, text=formate)
                return
            else:
                # Если аргументов нет, блокируем пользователя навсегда
                username = message.reply_to_message.from_user.username
                duration = 365*24*60*60  # Блокировка на 1 год в секундах
        else:
            # Извлекаем информацию из сообщения
            args = message.text.split()[1:]
            username = None
            duration = 0

            if args[0].startswith('@'):  # Если указан username
                username = args[0].lstrip('@')
                duration_args = args[1:]
            else:  # Если username не указан, считаем, что первый аргумент - это часть длительности
                duration_args = args

            for arg in duration_args:
                if arg.endswith('d'):
                    duration += int(arg[:-1]) * 24 * 60 * 60  # Преобразуем дни в секунды
                elif arg.endswith('h'):
                    duration += int(arg[:-1]) * 60 * 60  # Преобразуем часы в секунды
                elif arg.endswith('m'):
                    duration += int(arg[:-1]) * 60  # Преобразуем минуты в секунды
                else:
                    bot.send_message(chat_id, text=time_formate)
                    return

        # Проверяем, что команда не применяется к боту
        if username == bot.get_me().username:
            bot.send_message(chat_id, text=bott)
            return


        # Если username не был указан в аргументах, пытаемся получить его из ответного сообщения
        if not username and message.reply_to_message:
            if message.reply_to_message.from_user.username:
                username = message.reply_to_message.from_user.username
            else:
                bot.send_message(chat_id, text=erroruser)
                return

        # Блокируем пользователя
        user_id = get_user_id_by_username(username, chat_id)
        user_status = bot.get_chat_member(chat_id, user_id).status
        # Проверяем, что найденный пользователь не является администратором или создателем чата
        if user_status not in ('creator', 'administrator'):
            bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + duration)
            formatted_duration = format_duration(duration)
            if not formatted_duration:
                formatted_duration = ban
                bot.send_message(chat_id, f"@{username}! {allow} {formatted_duration}.")
        else:
            bot.send_message(chat_id, text=error)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при блокировке пользователя:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        bot.send_message(chat_id, text=erroruser)


# Обработчик команды `/unmute`, которая снимает заглушения с пользователя
@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    try:
        chat_id = message.chat.id

        # Проверяем, что чат является группой или супергруппой
        if message.chat.type not in ['group', 'supergroup']:
            return

        language = get_chat_language(chat_id)

        only_admin = data['commands'][language]['allow_text']
        bott = data['commands'][language]['bot_text']
        error = data['commands'][language]['error_text']
        formate = data['commands'][language]['unmute']['formate']
        fail = data['commands'][language]['unmute']['fail']
        erroruser = data['commands'][language]['unmute']['error']
        allow = data['commands'][language]['unmute']['allow']
        # Проверяем, что отправитель команды является администратором или создателем чата
        if message.from_user.id not in [chat_member.user.id for chat_member in bot.get_chat_administrators(chat_id)]:
            bot.send_message(chat_id, text=only_admin)
            return


        # Проверяем, что команда имеет аргументы
        if len(message.text.split()) < 2 and not message.reply_to_message:
            bot.send_message(chat_id, text=formate)
            return

        # Получаем имя пользователя из аргументов команды или из ответного сообщения
        if len(message.text.split()) >= 2:
            username = message.text.split()[1].lstrip('@')
        elif message.reply_to_message:
            if message.reply_to_message.from_user.username:
                username = message.reply_to_message.from_user.username
            else:
                bot.send_message(chat_id, text=fail)
                return
        else:
            bot.send_message(chat_id, text=fail)
            return

        # Получаем user_id пользователя
        user_id = get_user_id_by_username(username, chat_id)

        # Проверяем, что команда не применяется к боту
        if username == bot.get_me().username:
            bot.send_message(chat_id, text=bott)
            return

        # Пытаемся разблокировать пользователя
        bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True,
                                can_send_other_messages=True, can_add_web_page_previews=True, until_date=0)
        bot.send_message(chat_id, f"@{username}! {allow}")
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при снятии заглушки у пользователя:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        bot.send_message(chat_id, text=erroruser)


# Обработчик команды `/kick`, которая исключает пользователя
@bot.message_handler(commands=['kick'])
def kick_user(message):
    try:
        chat_id = message.chat.id

        # Проверяем, что чат является группой или супергруппой
        if message.chat.type not in ['group', 'supergroup']:
            return

        language = get_chat_language(chat_id)


        only_admin = data['commands'][language]['allow_text']
        bott = data['commands'][language]['bot_text']
        error = data['commands'][language]['error_text']
        formate = data['commands'][language]['kick']['formate']
        allow = data['commands'][language]['kick']['allow']
        areason = data['commands'][language]['kick']['reason']
        erroruser = data['commands'][language]['kick']['error']
        # Проверяем, что отправитель команды является администратором или создателем чата
        if message.from_user.id not in [chat_member.user.id for chat_member in bot.get_chat_administrators(chat_id)]:
            bot.send_message(chat_id, text=only_admin)
            return

        # Если сообщение является ответом на другое сообщение, извлекаем username из него
        if message.reply_to_message and message.reply_to_message.from_user:
            username = message.reply_to_message.from_user.username
            reason = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else None
        else:
            # Получаем username из аргумента команды и удаляем символ "@", если присутствует
            if len(message.text.split()) > 1:
                username = message.text.split()[1].lstrip('@')
                reason = message.text.split(' ', 2)[2] if len(message.text.split()) > 2 else None
            else:
                bot.send_message(chat_id, text=formate)
                return

        # Проверяем, что команда не применяется к администраторам или создателям чата
        if username == bot.get_me().username:
            bot.send_message(chat_id, text=bott)
            return

        user_id = get_user_id_by_username(username, chat_id)
        
        # Выполняем исключение пользователя из чата
        bot.kick_chat_member(chat_id, user_id)
        if reason:
            bot.send_message(chat_id, f"@{username}! {areason} {reason}")
        else:
            bot.send_message(chat_id, f"@{username}! {allow}")
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при исключении пользователя из чата:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        bot.send_message(chat_id, text=erroruser)

# Обработчик команды `/setrules`, который устанавливает правила группы
@bot.message_handler(commands=['setrules'])
def set_rules(message):
    try:
        chat_id = message.chat.id

        # Проверяем, что чат является группой или супергруппой
        if message.chat.type not in ['group', 'supergroup']:
            return

        language = get_chat_language(chat_id)

        only_admin = data['commands'][language]['allow_text']
        bott = data['commands'][language]['bot_text']
        error = data['commands'][language]['error_text']
        formate = data['commands'][language]['setrules']['formate']
        allow = data['commands'][language]['setrules']['allow']
        fail = data['commands'][language]['setrules']['fail']
        # Проверяем, что отправитель команды является администратором или создателем чата
        if message.from_user.id not in [chat_member.user.id for chat_member in bot.get_chat_administrators(chat_id)]:
            bot.send_message(chat_id, text=only_admin)
            return

        # Проверяем, что после команды указаны правила
        if len(message.text.split()) < 2:
            bot.send_message(chat_id, text=formate)
            return

        # Получаем текст правил из сообщения
        rules_text = message.text.split(maxsplit=1)[1]

        # Подключаемся к базе данных rules.db
        conn = connect_to_db('rules.db')
        cursor = conn.cursor()

        # Сохраняем правила в базу данных
        cursor.execute("INSERT INTO group_rules (chat_id, rules_text) VALUES (?, ?)", (chat_id, rules_text))
        conn.commit()
        conn.close()
        bot.send_message(chat_id, text=allow)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при установке правил группы:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        bot.send_message(chat_id, text=fail)


# Обработчик команды `/editrules`, который изменяет правила группы
@bot.message_handler(commands=['editrules'])
def edit_rules(message):
    try:
        chat_id = message.chat.id

        # Проверяем, что чат является группой или супергруппой
        if message.chat.type not in ['group', 'supergroup']:
            return

        language = get_chat_language(chat_id)

        only_admin = data['commands'][language]['allow_text']
        bott = data['commands'][language]['bot_text']
        error = data['commands'][language]['error_text']
        formate = data['commands'][language]['editrules']['formate']
        allow = data['commands'][language]['editrules']['allow']
        fail = data['commands'][language]['editrules']['fail']
        # Проверяем, что отправитель команды является администратором или создателем чата
        if message.from_user.id not in [chat_member.user.id for chat_member in bot.get_chat_administrators(chat_id)]:
            bot.send_message(chat_id, text=only_admin)
            return

        # Проверяем, что после команды указаны новые правила
        if len(message.text.split()) < 2:
            bot.send_message(chat_id, text=formate)
            return

        # Получаем новый текст правил из сообщения
        new_rules_text = message.text.split(maxsplit=1)[1]

        # Подключаемся к базе данных rules.db
        conn = connect_to_db('rules.db')
        cursor = conn.cursor()

        # Обновляем правила в базе данных
        cursor.execute("UPDATE group_rules SET rules_text=? WHERE chat_id=?", (new_rules_text, chat_id))
        conn.commit()
        conn.close()
        bot.send_message(chat_id, text=allow)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при изменении правил группы:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        bot.send_message(chat_id, text=fail)


# Обработчик команды `/rules`, который отправляет правила группы в чат
@bot.message_handler(commands=['rules'])
def send_rules(message):
    try:
        chat_id = message.chat.id

        # Проверяем, что чат является группой или супергруппой
        if message.chat.type not in ['group', 'supergroup']:
            return

        language = get_chat_language(chat_id)
        no = data['commands'][language]['rules']['no']
        fail = data['commands'][language]['rules']['fail']
        # Подключаемся к базе данных rules.db
        conn = connect_to_db('rules.db')
        cursor = conn.cursor()

        # Получаем текст правил из базы данных
        cursor.execute("SELECT rules_text FROM group_rules WHERE chat_id=?", (chat_id,))
        result = cursor.fetchone()

        # Проверяем, есть ли правила для этой группы в базе данных
        if result is None or result[0] == "":
            bot.send_message(chat_id, text=no)
            return

        rules_text = result[0]

        # Отправляем текст правил в чат
        bot.send_message(chat_id, f"{rules_text}")

        conn.close()
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при отправке правил группы:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        bot.send_message(chat_id, text=fail)


# Обработчик команды `/promote`, который повышает статус пользователя до администратора
@bot.message_handler(commands=['promote'])
def promote_user(message):
    try:
        chat_id = message.chat.id
        # Проверяем, что чат является группой или супергруппой
        if message.chat.type not in ['group', 'supergroup']:
            return
        language = get_chat_language(chat_id)

        only_admin = data['commands'][language]['allow_text']
        bott = data['commands'][language]['bot_text']
        error = data['commands'][language]['error_text']
        formate = data['commands'][language]['promote']['formate']
        allow = data['commands'][language]['promote']['allow']
        admin = data['commands'][language]['promote']['fail']
        fail = data['commands'][language]['promote']['error']
        # Проверяем, что отправитель команды является администратором или создателем чата
        if message.from_user.id not in [chat_member.user.id for chat_member in bot.get_chat_administrators(chat_id)]:
            bot.send_message(chat_id, text=only_admin)
            return

        # Получаем user_id пользователя
        if message.reply_to_message and message.reply_to_message.from_user:
            user_id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username
        elif len(message.text.split()) > 1:
            username = message.text.split()[1].lstrip('@')
            user_id = get_user_id_by_username(username, chat_id)
        else:
            bot.send_message(chat_id, text=formate)
            return
        # Проверяем, что команда не применяется к администраторам или создателям чата
        if username == bot.get_me().username:
            bot.send_message(chat_id, text=bott)
            return
        # Проверяем, что найденный пользователь не является администратором или создателем чата
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status not in ('creator', 'administrator'):
            # Повышаем статус пользователя до администратора
            bot.promote_chat_member(chat_id, user_id, can_change_info=True, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=False)
            bot.send_message(chat_id, f"@{username}! {allow}")
        else:
            bot.send_message(chat_id, text=admin)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при повышении пользователя до администратора:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        bot.send_message(chat_id, text=fail)


# Обработчик команды `/demote`, который понизит статус администратора до пользователя
@bot.message_handler(commands=['demote'])
def demote_user(message):
    try:
        chat_id = message.chat.id
        # Проверяем, что чат является группой или супергруппой
        if message.chat.type not in ['group', 'supergroup']:
            return
        language = get_chat_language(chat_id)
        only_admin = data['commands'][language]['allow_text']
        bott = data['commands'][language]['bot_text']
        error = data['commands'][language]['error_text']
        formate = data['commands'][language]['demote']['formate']
        allow = data['commands'][language]['demote']['allow']
        admin = data['commands'][language]['demote']['fail']
        fail = data['commands'][language]['demote']['error']
        # Проверяем, что отправитель команды является администратором или создателем чата
        if message.from_user.id not in [chat_member.user.id for chat_member in bot.get_chat_administrators(chat_id)]:
            bot.send_message(chat_id, text=only_admin)
            return

        # Получаем user_id пользователя
        if message.reply_to_message and message.reply_to_message.from_user:
            user_id = message.reply_to_message.from_user.id
            username = message.reply_to_message.from_user.username
        elif len(message.text.split()) > 1:
            username = message.text.split()[1].lstrip('@')
            user_id = get_user_id_by_username(username, chat_id)
        else:
            bot.send_message(chat_id, text=formate)
            return
        # Проверяем, что команда не применяется к администраторам или создателям чата
        if username == bot.get_me().username:
            bot.send_message(chat_id, text=bott)
            return
        # Проверяем, что найденный пользователь является администратором
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status in ('creator', 'administrator'):
            # Понижаем статус пользователя до обычного
            bot.promote_chat_member(chat_id, user_id, can_change_info=False, can_delete_messages=False, can_invite_users=False, can_restrict_members=False, can_pin_messages=False, can_promote_members=False)
            bot.send_message(chat_id, f"@{username}! {allow}")
        else:
            bot.send_message(chat_id, f"@{username}! {admin}")
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при понижении статуса пользователя:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        bot.send_message(chat_id, text=fail)

# Обработчик команды `/groupstats`, который покажет статистику группы
@bot.message_handler(commands=['groupstats'])
def group_statistics(message):
    try:
        chat_id = message.chat.id
        # Проверяем, что чат является группой или супергруппой
        if message.chat.type not in ['group', 'supergroup']:
            return
        language = get_chat_language(chat_id)

        only_admin = data['commands'][language]['allow_text']
        bott = data['commands'][language]['bot_text']
        error = data['commands'][language]['error_text']
        fail = data['commands'][language]['groupstats']['fail']
        # Проверяем, что отправитель команды является администратором или создателем чата
        if message.from_user.id not in [chat_member.user.id for chat_member in bot.get_chat_administrators(chat_id)]:
            bot.send_message(chat_id, text=only_admin)
            return

        # Получаем информацию о статистике группы
        group_stats = get_group_statistics_by_chat_id(chat_id)

        # Форматируем данные в строку
        formatted_stats = f"Статистика группы:\n\n" + "\n".join([f"🧑‍💻 Создатель: @{stats[3]}\n👥 Активные пользователи: <b>{stats[4]}</b>\n🌎 Язык группы: <b>{'🇷🇺' if stats[5] == 'rus' else '🇺🇸'}</b>\n💬 Всего сообщений: <b>{stats[6]}</b>\n📝 Всего слов: <b>{stats[8]}</b>\n💠 Заработано пользователями: <b>{round(stats[7], 2)}</b> Grand бонусов\n⚠️ Всего предупреждений: <b>{stats[9]}</b>" for stats in group_stats])

        # Если язык чата английский, отправляем статистику группы на английском
        if language == "en":
            formatted_stats_en = f"Group Statistics:\n\n" + "\n".join([f"🧑‍💻 Creator: @{stats[3]}\n👥 Active Users: <b>{stats[4]}</b>\n🌎 Group Language: <b>{'🇷🇺' if stats[5] == 'rus' else '🇺🇸'}</b>\n💬 Total Messages: <b>{stats[6]}</b>\n📝 Total Words: <b>{stats[8]}</b>\n💠 Earned by Users: <b>{round(stats[7], 2)}</b> Grand bonuses\n⚠️ Total Warnings: <b>{stats[9]}</b>" for stats in group_stats])
            bot.send_message(chat_id, formatted_stats_en, parse_mode="HTML")
        else:
            # Отправляем отформатированную информацию о статистике группы в чат
            bot.send_message(chat_id, formatted_stats, parse_mode="HTML")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при получении статистики группы:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        bot.send_message(chat_id, text=fail)

# Обработчик команды `/stats`, который покажет статистику пользователя
@bot.message_handler(commands=['stats'])
def group_statistics(message):
    try:
        chat_id = message.chat.id
        # Проверяем, что чат является группой или супергруппой
        if message.chat.type not in ['group', 'supergroup']:
            return
        language = get_chat_language(chat_id)

        only_admin = data['commands'][language]['allow_text']
        bott = data['commands'][language]['bot_text']
        error = data['commands'][language]['error_text']
        formate = data['commands'][language]['stats']['formate']
        fail = data['commands'][language]['stats']['fail']
        # Проверяем, что отправитель команды является администратором или создателем чата
        if message.from_user.id not in [chat_member.user.id for chat_member in bot.get_chat_administrators(chat_id)]:
            bot.send_message(chat_id, text=only_admin)
            return

        # Если сообщение является ответом на другое сообщение, извлекаем username из него
        if message.reply_to_message and message.reply_to_message.from_user:
            username = message.reply_to_message.from_user.username
            reason = message.text.split(' ', 1)[1] if len(message.text.split()) > 1 else None
        else:
            # Получаем username из аргумента команды и удаляем символ "@", если присутствует
            if len(message.text.split()) > 1:
                username = message.text.split()[1].lstrip('@')
                reason = message.text.split(' ', 2)[2] if len(message.text.split()) > 2 else None
            else:
                bot.send_message(chat_id, text=formate)
                return

        # Проверяем, что команда не применяется к администраторам или создателям чата
        if username == bot.get_me().username:
            bot.send_message(chat_id, text=bott)
            return

        user_id = get_user_id_by_username(username, chat_id)

        # Получаем информацию о статистике пользователя
        user_stats = get_user_statistics_by_chat_id(user_id, chat_id)

        # Форматируем данные в строку
        formatted_stats = f"Статистика @{user_stats[0]}:\n\n💬 Всего сообщений: <b>{user_stats[1]}</b>\n📝 Всего слов: <b>{user_stats[3]}</b>\n💠 Всего Grand бонусов: <b>{round(user_stats[2], 2)}</b>\n⚠️ Всего предупреждений: <b>{user_stats[4]}</b>\n"

        # Если язык чата английский, отправляем статистику пользователя на английском
        if language == "en":
            formatted_stats_en = f"Stats @{user_stats[0]}:\n\n💬 Total messages: <b>{user_stats[1]}</b>\n📝 Total words: <b>{user_stats[3]}</b>\n💠 Total Grand bonuses: <b>{round(user_stats[2], 2)}</b>\n⚠️ Total warnings: <b>{user_stats[4]}</b>\n"
            bot.send_message(chat_id, formatted_stats_en, parse_mode="HTML")
        else:
            # Отправляем отформатированную информацию о статистике группы в чат
            bot.send_message(chat_id, formatted_stats, parse_mode="HTML")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при получении статистики группы:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        bot.send_message(chat_id, text=fail)

# Обработчик команды `/top`, который выведет топ участников группы
@bot.message_handler(commands=['top'])
def top_users(message):
    try:
        chat_id = message.chat.id
        # Проверяем, что чат является группой или супергруппой
        if message.chat.type not in ['group', 'supergroup']:
            return
        language = get_chat_language(chat_id)

        only_admin = data['commands'][language]['allow_text']
        bott = data['commands'][language]['bot_text']
        error = data['commands'][language]['error_text']
        fail = data['commands'][language]['top']['fail']
        top = data['commands'][language]['top']['top']
        # Проверяем, что отправитель команды является администратором или создателем чата
        if message.from_user.id not in [chat_member.user.id for chat_member in bot.get_chat_administrators(chat_id)]:
            bot.send_message(chat_id, text=only_admin)
            return

        # Получаем список пользователей для топа
        connection_users = connect_to_db('chat_data.db')
        cursor_users = connection_users.cursor()
        cursor_users.execute("SELECT user_id, message_count, user_username FROM users WHERE chat_id = ? ORDER BY message_count DESC LIMIT 30", (chat_id,))
        top_users = cursor_users.fetchall()
        chat_message = top

        for idx, user_data in enumerate(top_users, start=1):
            user_id = user_data[0]
            message_count = user_data[1]
            username = user_data[2]

            user_mention = username
            if language == "en":
                chat_message += f"{idx}🏅 - @{user_mention}\n Number of 💬: <b>{message_count}</b>\n\n"
            else:
                chat_message += f"{idx}🏅 - @{user_mention}\n Количество 💬: <b>{message_count}</b>\n\n"

        bot.send_message(chat_id, chat_message, parse_mode='HTML')

    except sqlite3.Error as e:
        error_message = f"⚠️ Ошибка при выполнении SQL-запроса: {e}"
        logging.error(error_message)
        bot.send_message(chat_id, text=fail)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при получении топа пользователей:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )
        logging.error(error_message)
        bot.send_message(chat_id, text=fail)
    finally:
        if 'cursor_users' in locals() and cursor_users is not None:
            cursor_users.close()
        if 'connection_users' in locals() and connection_users is not None:
            connection_users.close()

# Обработчик команды `/help`, список всех команд
@bot.message_handler(commands=['help'])
def help_command(message):
    try:
        chat_id = message.chat.id
        # Проверяем, что чат является группой или супергруппой
        if message.chat.type not in ['group', 'supergroup']:
            return
        language = get_chat_language(chat_id)

        only_admin = data['commands'][language]['allow_text']
        bott = data['commands'][language]['bot_text']
        error = data['commands'][language]['error_text']
        fail = data['commands'][language]['help']['fail']
        # Проверяем, что отправитель команды является администратором или создателем чата
        if message.from_user.id not in [chat_member.user.id for chat_member in bot.get_chat_administrators(chat_id)]:
            bot.send_message(chat_id, text=only_admin)
            return

        # Определяем текст помощи с перечислением команд и их описанием
        help_text = data['help_commands'][language]['help_text']
        help_text += data['help_commands'][language]['stats_commands']
        help_text += data['help_commands'][language]['groupstats_commands']
        help_text += data['help_commands'][language]['mute_commands']
        help_text += data['help_commands'][language]['unmute_commands']
        help_text += data['help_commands'][language]['kick_commands']
        help_text += data['help_commands'][language]['promote_commands']
        help_text += data['help_commands'][language]['demote_commands']
        help_text += data['help_commands'][language]['setrules_commands']
        help_text += data['help_commands'][language]['rules_commands']
        help_text += data['help_commands'][language]['editrules_commands']
        help_text += data['help_commands'][language]['warn_commands']
        help_text += data['help_commands'][language]['unwarn_commands']
        help_text += data['help_commands'][language]['top_commands']
        help_text += data['help_commands'][language]['help_commands']

        # Отправляем сообщение с помощью на соответствующем языке
        bot.send_message(chat_id, help_text, parse_mode='HTML')

    except Exception as e:
        # Обрабатываем ошибки и записываем сообщения об ошибке в журнал
        error_message = (
            f"⚠️ Произошла ошибка при выполнении команды help:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )
        logging.error(error_message)
        bot.send_message(chat_id, text=fail)

#Команды ручной модерации конец

@bot.message_handler(commands=['spam'])
def spam(message):
    chat_id = message.chat.id 
    language = get_chat_language(chat_id)
    if message.reply_to_message:  # Если команда вызвана в ответ на сообщение
        replied_user_id = message.reply_to_message.from_user.id
        try:
            # Отмечаем пользователя и ограничиваем его возможность отправки сообщений на сутки
            bot.restrict_chat_member(message.chat.id, replied_user_id, until_date=time.time() + 86400)
            if language == "rus":
                bot.reply_to(message, f"✅ Сообщение отправлено на рассмотрение!\n\nСообщение отмечено участником группы как СПАМ. В случае если данное сообщение является СПАМОМ, бонус Grand не будет начислен за активность\n\n🚫 Пользователь @{message.reply_to_message.from_user.username} ограничен в отправке сообщений до окончания проверки.")
            else:
                bot.reply_to(message, f"✅ Message sent for review!\n\nThis message has been marked as SPAM by a group member. If this message is SPAM, the Grand bonus will not be credited for the activity.\n\n🚫 User @{message.reply_to_message.from_user.username} is restricted from sending messages until verification is complete.")
            
            # Очищаем сообщение от смайликов, эмодзи, HTML-тегов, форматирования и лишних пробелов
            cleaned_text = clean_message(message.reply_to_message.text)
            
            # Создаем клавиатуру с кнопками "записать" и "удалить"
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(InlineKeyboardButton("Удалить ❌", callback_data="delete"),
                     InlineKeyboardButton("Записать ✅", callback_data="write"))
            
            # Отправляем очищенное сообщение в нужный чат с клавиатурой
            bot.send_message(-1002007478754, cleaned_text, reply_markup=keyboard)
            
            # Удаляем сообщение, которое вызвало команду
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.reply_to_message.message_id)
        except Exception as e:
            print(f"Error: {e}")
            bot.reply_to(message, "⚠️ Я не могу отправить на проверку данное сообщение.\n\n⚠️ I am unable to submit this message for verification.")
    else:  # Если команда вызвана без ответа
        # Удаляем сообщение, которое вызвало команду
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            print(f"Error: {e}")
            bot.reply_to(message, "⚠️ Я не могу отправить на проверку данное сообщение.\n\n⚠️ I am unable to submit this message for verification.")

# Функция для генерации случайного кода из 5 цифр
def generate_code():
    return ''.join(random.choices('0123456789', k=5))




@bot.message_handler(func=lambda message: message.text in ["💠 G-бонус", "💠 G-bonus"])
def grand_buttons_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            username = message.from_user.username
            user_language = get_user_language(chat_id)
            text = data['grand_bonus'][user_language]['1']
            text += data['grand_bonus'][user_language]['2']
            text += data['grand_bonus'][user_language]['3']
            text += data['grand_bonus'][user_language]['4']
            text += data['grand_bonus'][user_language]['5']

            if user_language == "en":
                photo = open('bw_EN.png', 'rb')
                keyboard = types.InlineKeyboardMarkup()
                url_enchat_button = types.InlineKeyboardButton(text="Going read! 📚", url="https://a.co/d/gJxsXqP")
                keyboard.add(url_enchat_button)
                bot.send_photo(chat_id, photo, caption=text, reply_markup=keyboard)
            else:
                photo = open('bw_RU.png', 'rb')
                keyboard = types.InlineKeyboardMarkup()
                url_ruschat_button = types.InlineKeyboardButton(text="Иду читать! 📚", url="https://www.litres.ru/book/artur-grandi/grand-time-70005007/?lfrom=1117899162&ref_key=c640e512577d7235adb7f208059ba746eb3dd77dbbb2d48de86aa6ec141245fb&ref_offer=1")
                keyboard.add(url_ruschat_button)
                bot.send_photo(chat_id, photo, caption=text, reply_markup=keyboard)
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '💠 GRAND бонус':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{message.from_user.username if message.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)



# Создание базы данных и таблицы
conn = connect_to_db('active_chats.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS active_chats
                  (sender_id INTEGER PRIMARY KEY, recipient_id INTEGER, message INTEGER, message_id INTEGER, language INTEGER)''')
conn.commit()
conn.close()


# Функция для удаления активного чата из базы данных
def remove_active_chat(user_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM active_chats WHERE user_id = ?''', (user_id,))
    conn.commit()
    conn.close()

# Функция для получения чата, с которым пользователь активно общается
def get_active_chat(user_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT chat_id FROM active_chats WHERE user_id = ?''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None


def send_new_buttons(language, chat_id):
    connection, cursor, user = initialize_database(chat_id)
    prefix = user[2]
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    if language == 'rus':
        stats_button = types.KeyboardButton("📊 Профиль")
        referrals_button = types.KeyboardButton("💎 Награда")
        language_ru_button = types.KeyboardButton("🌎 Язык")
        settings_ru_button = types.KeyboardButton("⚙️ Настройки")
        support_ru_button = types.KeyboardButton("🛠 Помощь")
        grand_ru_button = types.KeyboardButton("💠 G-бонус")
        keyboard.add(stats_button, referrals_button, language_ru_button, settings_ru_button, support_ru_button, grand_ru_button)
        if prefix == "free":
            sotrud_button = types.KeyboardButton("📢 Сотрудничество")
            keyboard.add(sotrud_button)            
        # Если пользователь имеет права администратора
        if chat_id in allowed_users:
            bd_button = types.KeyboardButton("🌐 База")
            staff_commands_button = types.KeyboardButton("📝 Команды")
            info_button = types.KeyboardButton("👁‍🗨 Info")
            if chat_id == 1858164732:
                ad_button = types.KeyboardButton("📢 Реклама")
                keyboard.add(bd_button, staff_commands_button, info_button, ad_button)
            else:
                keyboard.add(bd_button, staff_commands_button, info_button)
    elif language == 'en':
        keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        stats_button = types.KeyboardButton("📊 Statistics")
        referrals_button = types.KeyboardButton("💎 Rewards")
        language_en_button = types.KeyboardButton("🌎 Language")
        settings_en_button = types.KeyboardButton("⚙️ Settings")
        support_en_button = types.KeyboardButton("🛠 Support")
        grand_en_button = types.KeyboardButton("💠 G-bonus")
        keyboard.add(stats_button, referrals_button, language_en_button, settings_en_button, support_en_button, grand_en_button)

        # Если пользователь имеет права администратора
        if chat_id in allowed_users:
            bd_button = types.KeyboardButton("🌐 База")
            staff_commands_button = types.KeyboardButton("📝 Команды")
            info_button = types.KeyboardButton("👁‍🗨 Info")
            if chat_id == 1858164732:
                ad_button = types.KeyboardButton("📢 Реклама")
                keyboard.add(bd_button, staff_commands_button, info_button, ad_button)
            else:
                keyboard.add(bd_button, staff_commands_button, info_button)
    
    return keyboard



# Функция для создания клавиатуры отправителя
def create_keyboard_cancel(user_language):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if user_language == "rus":
        cancel_button = types.KeyboardButton("❌ Отменить")
    else: 
        cancel_button = types.KeyboardButton("❌ Cancel")
    keyboard.add(cancel_button)
    return keyboard


@bot.message_handler(func=lambda message: message.text in ["❌ Отменить", "❌ Cancel"])
def cancel_buttons_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            sender_id = message.from_user.id
            language_user = get_user_language(chat_id)
            new_keyboard = send_new_buttons(language_user, sender_id)
            # Удаляем последнее сообщение бота
            bot.delete_message(chat_id, message.message_id - 1)
            # Проверяем, содержит ли сообщение строки "❌ Отменить" или "❌ Cance
            if language_user == "en":
                bot.send_message(sender_id, "You've cancelled your request to technical support! If you have any questions, we'll be waiting for you! 🛠️❓", reply_markup=new_keyboard)
            else:
                bot.send_message(sender_id, "Ты отменил запрос в техническую поддержку! Если у тебя возникнут вопросы, мы будем тебя ждать! 🛠️❓", reply_markup=new_keyboard)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '🛠 Помощь':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @username\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)



def get_block_time(sender_id):
    """
    Получает время блокировки пользователя по его ID.

    Args:
        sender_id (INTEGER): ID пользователя

    Returns:
        datetime: Время блокировки (если пользователь заблокирован), иначе None
    """

    connection = connect_to_db('chat_data.db')
    cursor = connection.cursor()

    cursor.execute("""
        SELECT block_time
        FROM police
        WHERE sender_id = ? 
    """, (sender_id,))

    # Получаем время блокировки из базы данных
    block_time_str = cursor.fetchone()

    connection.close()

    # Если есть запись о блокировке, возвращаем время блокировки в формате datetime
    if block_time_str:
        return datetime.strptime(block_time_str[0], '%Y-%m-%d %H:%M:%S.%f')
    else:
        return None

def get_active(chat_id):
    connection = connect_to_db('active_chats.db')
    cursor = connection.cursor()

    cursor.execute("""
        SELECT sender_id, recipient_id
        FROM active_chats
        WHERE sender_id = ? OR recipient_id = ?
    """, (chat_id, chat_id))

    result = cursor.fetchone()

    connection.close()

    return result is not None

def format_block_time(block_time):
    """
    Преобразует время блокировки пользователя в нужный формат.

    Args:
        block_time (datetime): Время блокировки пользователя

    Returns:
        str: Отформатированное время блокировки в формате "день.месяц.год часы:минуты"
    """
    formatted_block_time = block_time.strftime("%d.%m.%Y %H:%M")
    return formatted_block_time


@bot.message_handler(func=lambda message: message.text in ["🛠 Помощь", "🛠 Support"])
def support_buttons_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            username = message.from_user.username
            user_language = get_user_language(chat_id)
            keyboard_cancel = create_keyboard_cancel(user_language)

            # Проверка на блокировку пользователя
            block_time = get_block_time(chat_id)
            active_chat = get_active(chat_id)
            if block_time:
                formatted_block_time = block_time.strftime("%d.%m.%Y %H:%M")
                formatted_block_time_en = block_time.strftime("%m/%d/%Y %I:%M %p")
                if user_language == "en":
                    block_message = f"The feature is not available for you until  {formatted_block_time_en}."
                else:
                     block_message = f"Для тебя функция недоступна до {formatted_block_time}."                   
                bot.send_message(chat_id, block_message)
            else:
                # Пользователь не заблокирован
                if user_language == "en":
                    bot.send_message(chat_id, " If you have any questions or problems, don't hesitate to share them with us! Our technical service is ready to help you find a solution. We will try to offer you the best solution.\n\n<b>Describe your problem or question in detail and send it to me!</b>", reply_markup=keyboard_cancel, parse_mode="HTML")
                else:
                    bot.send_message(chat_id, " Если у тебя возникли вопросы или проблемы, не стесняйся поделиться ими с нами! Наша техническая служба готова помочь тебе найти решение. Мы постараемся предложить тебе наилучшее решение.\n\n<b>Подробно опиши свою проблему или вопрос и отправь мне!</b>", reply_markup=keyboard_cancel, parse_mode="HTML")

                # Ожидаем сообщение от пользователя после нажатия кнопки
                bot.register_next_step_handler(message, process_user_message, language_user=user_language, sender_id=chat_id)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку ' Помощь':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: {username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

        






def process_user_message(message, language_user, sender_id):
    try:
        new_keyboard = send_new_buttons(language_user, sender_id)
        # Проверяем, содержит ли сообщение строки "❌ Отменить" или "❌ Cancel"
        if "❌ Отменить" in message.text or "❌ Cancel" in message.text:

            if language_user == "en":
                bot.send_message(sender_id, "You've cancelled your request to technical support! If you have any questions, we'll be waiting for you! 🛠️❓", reply_markup=new_keyboard)
            else:
                bot.send_message(sender_id, "Ты отменил запрос в техническую поддержку! Если у тебя возникнут вопросы, мы будем тебя ждать! 🛠️❓", reply_markup=new_keyboard)
            return  # Завершаем функцию обработки сообщения без выполнения дальнейших действий

        keyboard = InlineKeyboardMarkup()
        if language_user == "rus":
            keyboard.row(InlineKeyboardButton("📤 Отправить", callback_data='send_message_rus'),
                         InlineKeyboardButton("✏️ Редактировать", callback_data='edit_message_rus'))
        else:
            keyboard.row(InlineKeyboardButton("📤 Send", callback_data='send_message_en'),
                         InlineKeyboardButton("✏️ Edit", callback_data='edit_message_en'))

        # Отправка сообщения с клавиатурой
        sent_message = bot.send_message(message.chat.id, message.text, reply_markup=keyboard)

        # Запись данных в базу данных

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обработке сообщения от пользователя:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.chat.id}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

        



@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_message'))
def edit_message_callback(call):
    if call.data.endswith('_rus'):
        language = "rus"
    else:
        language = "en"

    if language == "rus":
        edit_text = "Введите новое сообщение:"
    else: 
        edit_text = "Enter a new message:"
    # Изменение старого сообщения
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=edit_text)

    # Ожидаем новое сообщение от пользователя для редактирования
    bot.register_next_step_handler(call.message, process_edited_message, language_user=language, sender_id=call.message.chat.id)

def process_edited_message(message, language_user, sender_id):
    try:
        # Проверяем, содержит ли сообщение строки "❌ Отменить" или "❌ Cancel"
        if "❌ Отменить" in message.text or "❌ Cancel" in message.text:
            new_keyboard = send_new_buttons(language_user, sender_id)
            if language_user == "en":
                bot.send_message(sender_id, "You've cancelled your request to technical support! If you have any questions, we'll be waiting for you! 🛠️❓", reply_markup=new_keyboard)
            else:
                bot.send_message(sender_id, "Ты отменил запрос в техническую поддержку! Если у тебя возникнут вопросы, мы будем тебя ждать! 🛠️❓", reply_markup=new_keyboard)
            return  # Завершаем функцию обработки сообщения без выполнения дальнейших действий

        keyboard = InlineKeyboardMarkup()
        if language_user == "rus":
            keyboard.row(InlineKeyboardButton("📤 Отправить", callback_data='send_message_rus'),
                         InlineKeyboardButton("✏️ Редактировать", callback_data='edit_message_rus'))
        else:
            keyboard.row(InlineKeyboardButton("📤 Send", callback_data='send_message_en'),
                         InlineKeyboardButton("✏️ Edit", callback_data='edit_message_en'))

        # Отправка отредактированного сообщения с клавиатурой
        sent_message = bot.send_message(message.chat.id, message.text, reply_markup=keyboard)

        # Запись данных в базу данных

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обработке отредактированного сообщения от пользователя:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.chat.id}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

        







def save_to_database(sender_id, message_id, message, language, recipient_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO active_chats (sender_id, message_id, recipient_id, message, language) VALUES (?, ?, ?, ?, ?)''', (sender_id, message_id, recipient_id, message, language))
    conn.commit()
    conn.close()

@bot.callback_query_handler(func=lambda call: call.data == 'send_message_en')
def send_message_callback(call):
    try:
        language_user = "en"
        sender_id = call.message.chat.id
        username = call.from_user.username or call.from_user.first_name
        fq = call.message.text
        new_keyboard = send_new_buttons(language_user, sender_id)
        text = f"🇺🇸 @{username} ({sender_id})\n\n{fq}"
        # Редактирование сообщения с кнопкой "Отправить" на сообщение "Отправлено, ожидайте"
        bot.edit_message_text("Your message has been sent.📬 Our team will contact you shortly.👨‍💻", call.message.chat.id, call.message.message_id)
        bot.send_message(sender_id, "Request in queue", reply_markup=new_keyboard)

        # Отправка сообщения в другой чат с кнопками "Принять" и "Отклонить" и запись в базу данных
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton("Reject ❌", callback_data=f'reject_{call.message.message_id}'),
                     InlineKeyboardButton("Accept ✅", callback_data=f'accept_{call.message.message_id}'))

        bot.send_message(-1002130493902, text=text, reply_markup=keyboard)

        # Запись данных в базу данных
        save_to_database(call.message.chat.id, call.message.message_id, message=call.message.text, recipient_id=username, language="en")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обработке колбэка:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {call.message.chat.id}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

        

@bot.callback_query_handler(func=lambda call: call.data == 'send_message_rus')
def send_message_callback(call):
    try:
        language_user = "rus"
        sender_id = call.message.chat.id
        username = username = call.from_user.username or call.from_user.first_name
        fq = call.message.text
        new_keyboard = send_new_buttons(language_user, sender_id)
        text = f"🇷🇺 @{username} ({sender_id})\n\n{fq}"
        # Редактирование сообщения с кнопкой "Отправить" на сообщение "Отправлено, ожидайте"
        bot.edit_message_text("Твоё сообщение отправлено.📬 Наша команда свяжется с тобой в ближайшее время.👨‍💻", call.message.chat.id, call.message.message_id)
        bot.send_message(sender_id, "Запрос в очереди", reply_markup=new_keyboard)

        # Отправка сообщения в другой чат с кнопками "Принять" и "Отклонить" и запись в базу данных
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton("Отклонить ❌", callback_data=f'reject_{call.message.message_id}'),
                     InlineKeyboardButton("Принять ✅", callback_data=f'accept_{call.message.message_id}'))

        bot.send_message(-1002130493902, text=text, reply_markup=keyboard)

        # Запись данных в базу данных
        save_to_database(call.message.chat.id, call.message.message_id, message=call.message.text, recipient_id=username, language="rus")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обработке колбэка:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {call.message.chat.id}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

        


def get_chat_info_help(message_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT sender_id, message, recipient_id, language FROM active_chats WHERE message_id = ?''', (message_id,))
    chat_info = cursor.fetchone()
    conn.close()
    return chat_info

def get_support_entry(support_id):
    # Подключение к базе данных
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()

    # Поиск записи по support_id
    cursor.execute("SELECT * FROM support WHERE support_id=?", (support_id,))
    entry = cursor.fetchone()

    # Закрытие соединения с базой данных
    conn.close()

    return entry

@bot.callback_query_handler(func=lambda call: call.data.startswith('reject_'))
def reject_callback(call):
    try:
        # Получаем message_id из callback_data
        message_id = int(call.data.split('_')[1])
        support_id = call.from_user.id
        username = call.from_user.username or call.from_user.first_name
        support_data = get_support_entry(support_id)
        # Проверяем существует ли запись с данным message_id
        conn = connect_to_db('active_chats.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM active_chats WHERE recipient_id = ?''', (support_id,))
        existing_entry = cursor.fetchone()
        conn.close()



        # Получаем sender_id из базы данных по message_id
        conn = connect_to_db('active_chats.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT sender_id, message, language, recipient_id FROM active_chats WHERE message_id = ?''', (message_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
                sender_id = result[0]
                text = result[1]
                language = result[2]
                recipient_id = result[3]
                rej_keyboard = reject_keyboard()
                if language == "rus":
                    lan = "🇷🇺"
                else:
                    lan = "🇺🇸"
                # Отправляем сообщение об отмене запроса
                edit_text = f"{lan} @{recipient_id} ({sender_id})\n\n{text}\n\n🛠️ Запрос отклонил(а) @{username}!"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=edit_text)

                conn = connect_to_db('active_chats.db')
                cursor = conn.cursor()
                cursor.execute('''DELETE FROM active_chats WHERE sender_id = ?''', (sender_id,))
                conn.commit()
                conn.close()

        else:
                bot.send_message(call.from_user.id, "Не удалось найти сообщение с таким идентификатором")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обработке колбэка 'Принять':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {call.from_user.id}\n"
            f"• Время: {datetime.now()}"
        )

        logging.error(error_message)
        bot.send_message(call.from_user.id, "Произошла ошибка при обработке вашего запроса")

        # Логгирование ошибки
        logging.error(error_message)

# Функция для создания клавиатуры получателя
def reject_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    reject_with_reason = types.KeyboardButton("По причине 👮")
    reject_without_reasont = types.KeyboardButton("Без причины ❌")
    keyboard.add(reject_with_reason, reject_without_reasont)
    return keyboard

def process_reject_message(message):
    try:
        keyboard = InlineKeyboardMarkup()
        keyboard.row(InlineKeyboardButton("📤 Отправить", callback_data='send_reject'))

        # Отправка сообщения с клавиатурой
        sent_message = bot.send_message(message.chat.id, message.text, reply_markup=keyboard)

        # Запись данных в базу данных

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обработке сообщения от пользователя:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {message.chat.id}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

        

@bot.callback_query_handler(func=lambda call: call.data == 'send_reject')
def send_reject_callback(call):
    try:
        recipient_id = call.message.chat.id
        sender_id = recipient_id
        language_user = "rus"
        new_keyboard = send_new_buttons(language_user, sender_id)
        message = call.message.text

        # Получаем sender_id из базы данных по message_id
        conn = connect_to_db('active_chats.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT sender_id, language FROM active_chats WHERE recipient_id = ?''', (recipient_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            senderto_id = result[0]
            language_users = result[1]
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(sender_id, f"❌ Запрос отклонен по причине:\n\n {message}", reply_markup=new_keyboard)
            if language_users == "en":
                bot.send_message(senderto_id, f"⛔️ Your request has been rejected for the following reason: {message}")
            else: 
                bot.send_message(senderto_id, f"⛔️ Твой запрос был отклонен по причине: {message}")

            conn = connect_to_db('active_chats.db')
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM active_chats WHERE sender_id = ?''', (senderto_id,))
            conn.commit()
            conn.close()
        else:
            bot.send_message(recipient_id, "Не удалось найти сообщение с таким идентификатором")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '🛠 Помощь':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {call.message.chat.id}\n"
            f"• Username: @username\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)


@bot.message_handler(func=lambda message: message.text in ["По причине 👮"])
def reject_with_reasont_buttons_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            recipient_id = message.from_user.id
            bot.send_message(chat_id, "Напиши причину и отправь мне!")
            bot.register_next_step_handler(message, process_reject_message)


    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '🛠 Помощь':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @username\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

@bot.message_handler(func=lambda message: message.text in ["Без причины ❌"])
def reject_without_reasont_buttons_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            recipient_id = message.from_user.id
            language_user = "rus"
            sender_id = recipient_id
            new_keyboard = send_new_buttons(language_user, sender_id)

            # Получаем sender_id из базы данных по message_id
            conn = connect_to_db('active_chats.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT sender_id, language FROM active_chats WHERE recipient_id = ?''', (recipient_id,))
            result = cursor.fetchone()
            conn.close()

            if result:
                senderto_id = result[0]
                language_users = result[1]
                bot.delete_message(chat_id, message.message_id - 1)
                bot.send_message(sender_id, "❌ Запрос отклонен без указания причины!", reply_markup=new_keyboard)
                if language_users == "rus":
                    bot.send_message(senderto_id, "⛔️ Твой запрос был отклонен без указания причины")
                else:
                    bot.send_message(senderto_id, "⛔️ Your request has been rejected without giving a reason")

                conn = connect_to_db('active_chats.db')
                cursor = conn.cursor()
                cursor.execute('''DELETE FROM active_chats WHERE sender_id = ?''', (senderto_id,))
                conn.commit()
                conn.close()

            else:
                bot.send_message(recipient_id, "Не удалось найти сообщение с таким идентификатором")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '🛠 Помощь':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @username\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

        
        bot.reply_to(message, (
            "⚠️ Извините за неудобства! Возникла техническая проблема, "
            "но наш разработчик уже работают над ее решением. "
            "Пожалуйста, оставайтесь с нами, мы сообщим о любых обновлениях.\n\n"
            "⚠️ Sorry for the inconvenience! There was a technical problem, "
            "but our developer is already working on its solution. "
            "Please stay tuned, we will let you know about any updates."
        ))


@bot.callback_query_handler(func=lambda call: call.data.startswith('accept_'))
def accept_callback(call):
    try:
        # Получаем message_id из callback_data
        message_id = int(call.data.split('_')[1])
        support_id = call.from_user.id
        support_data = get_support_entry(support_id)
        username = call.from_user.username or call.from_user.first_name

        # Проверяем существует ли запись с данным message_id
        conn = connect_to_db('active_chats.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM active_chats WHERE recipient_id = ?''', (support_id,))
        existing_entry = cursor.fetchone()
        conn.close()




        # Получаем sender_id из базы данных по message_id
        conn = connect_to_db('active_chats.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT sender_id, message, language, recipient_id FROM active_chats WHERE message_id = ?''', (message_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
                sender_id = result[0]
                text = result[1]
                recipient_id = result[3]
                language_user = result[2]
                support = support_data[0]
                sup_name = support_data[1]
                sup_balance = support_data[2]
                like = support_data[3]
                dislike = support_data[4]
                code = support_data[5]
                if language_user == "rus":
                    lan = "🇷🇺"
                else:
                    lan = "🇺🇸"
                # Отправляем сообщение с данными в личку отправителю
                keyboard_sender = create_keyboard_sender(language_user)
                if language_user == "rus":
                    bot.send_message(sender_id, f"🛠️ Твой запрос приняли! Специалист: @{username}")
                else: 
                    bot.send_message(sender_id, f"🛠️ Your request has been accepted! Specialist: @{username}")
                keyboard_recipient = create_keyboard_recipient()
                edit_text = f"{lan} @{recipient_id} ({sender_id})\n\n{text}\n\n🛠️ Запрос принял(а) @{username}!"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=edit_text)

        else:
                bot.send_message(call.from_user.id, "Не удалось найти сообщение с таким идентификатором")

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обработке колбэка 'Принять':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {call.from_user.id}\n"
            f"• Время: {datetime.now()}"
        )

        logging.error(error_message)
        bot.send_message(call.from_user.id, "Произошла ошибка при обработке вашего запроса")

        # Логгирование ошибки
        logging.error(error_message)


# Функция для создания клавиатуры получателя
def rank_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    dislike = types.KeyboardButton("👎")
    like = types.KeyboardButton("👍")
    keyboard.add(dislike, like)
    return keyboard



def delete_chat(sender_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM active_chats WHERE sender_id = ?''', (sender_id, ))
    conn.commit()
    conn.close()

def get_recipient_like(sender_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT recipient_id FROM active_chats WHERE sender_id = ?''', (sender_id,))
    recipient_id = cursor.fetchone()
    conn.close()
    
    return recipient_id[0] if recipient_id else None

def get_sender_like(chat_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT sender_id FROM active_chats WHERE sender_id = ?''', (chat_id,))
    sender_id = cursor.fetchone()
    conn.close()
    
    return sender_id[0] if sender_id else None


def increment_like_count(recipient_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE support SET like = like + 1 WHERE support_id = ?''', (recipient_id,))
    conn.commit()
    conn.close()

def send_new_buttons_recipient(language, chat_id):
    connection, cursor, user = initialize_database(chat_id)
    prefix = user[2]
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    if language == 'rus':
        stats_button = types.KeyboardButton("📊 Профиль")
        referrals_button = types.KeyboardButton("💎 Награда")
        language_ru_button = types.KeyboardButton("🌎 Язык")
        settings_ru_button = types.KeyboardButton("⚙️ Настройки")
        support_ru_button = types.KeyboardButton("🛠 Помощь")
        grand_ru_button = types.KeyboardButton("💠 G-бонус")
        keyboard.add(stats_button, referrals_button, language_ru_button, settings_ru_button, support_ru_button, grand_ru_button)
        if prefix == "free":
            sotrud_button = types.KeyboardButton("📢 Сотрудничество")
            keyboard.add(sotrud_button)            
        # Если пользователь имеет права администратора
        if chat_id in allowed_users:
            bd_button = types.KeyboardButton("🌐 База")
            staff_commands_button = types.KeyboardButton("📝 Команды")
            info_button = types.KeyboardButton("👁‍🗨 Info")
            if chat_id == 1858164732:
                ad_button = types.KeyboardButton("📢 Реклама")
                keyboard.add(bd_button, staff_commands_button, info_button, ad_button)
            else:
                keyboard.add(bd_button, staff_commands_button, info_button)
    elif language == 'en':
        keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        stats_button = types.KeyboardButton("📊 Statistics")
        referrals_button = types.KeyboardButton("💎 Rewards")
        language_en_button = types.KeyboardButton("🌎 Language")
        settings_en_button = types.KeyboardButton("⚙️ Settings")
        support_en_button = types.KeyboardButton("🛠 Support")
        grand_en_button = types.KeyboardButton("💠 G-bonus")
        keyboard.add(stats_button, referrals_button, language_en_button, settings_en_button, support_en_button, grand_en_button)

        # Если пользователь имеет права администратора
        if chat_id in allowed_users:
            bd_button = types.KeyboardButton("🌐 База")
            staff_commands_button = types.KeyboardButton("📝 Команды")
            info_button = types.KeyboardButton("👁‍🗨 Info")
            if chat_id == 1858164732:
                ad_button = types.KeyboardButton("📢 Реклама")
                keyboard.add(bd_button, staff_commands_button, info_button, ad_button)
            else:
                keyboard.add(bd_button, staff_commands_button, info_button)
    
    return keyboard

@bot.message_handler(func=lambda message: message.text in ["👍"])
def like_buttons_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            language_user = get_user_language(chat_id)
            sender_id = get_sender_like(chat_id)
            recipient_id = get_recipient_like(sender_id)
            lk_keyboard = send_new_buttons(language_user, sender_id)
            language = "rus"
            new_key = send_new_buttons_recipient(language, recipient_id)
            if language_user == "rus":
                bot.send_message(sender_id, "Благодарю за оценку помощи специалиста!", reply_markup=lk_keyboard)
            else:
                bot.send_message(sender_id, "Thank you for appreciating the expert help!", reply_markup=lk_keyboard)
            bot.send_message(recipient_id, f"Ты завершил(а) чат с {sender_id} ✅\n\nОценка твоей помощи 👍", reply_markup=new_key)
            increment_like_count(recipient_id)
            delete_chat(sender_id)


    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '🛠 Помощь':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @username\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    

def increment_dislike_count(recipient_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute('''UPDATE support SET dislike = dislike + 1 WHERE support_id = ?''', (recipient_id,))
    conn.commit()
    conn.close()

@bot.message_handler(func=lambda message: message.text in ["👎"])
def like_buttons_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            language_user = get_user_language(chat_id)
            sender_id = get_sender_like(chat_id)
            recipient_id = get_recipient_like(sender_id)
            lk_keyboard = send_new_buttons(language_user, sender_id)
            language = "rus"
            new_key = send_new_buttons_recipient(language, recipient_id)
            if language_user == "rus":
                bot.send_message(sender_id, "Благодарю за оценку помощи специалиста!", reply_markup=lk_keyboard)
            else:
                bot.send_message(sender_id, "Thank you for appreciating the expert help!", reply_markup=lk_keyboard)
            bot.send_message(recipient_id, f"Ты завершил(а) чат с {sender_id} ✅\n\nОценка твоей помощи 👎", reply_markup=new_key)
            increment_dislike_count(recipient_id)
            delete_chat(sender_id)


    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '🛠 Помощь':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @username\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

def get_recipient(chat_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT recipient_id FROM active_chats WHERE recipient_id = ?''', (chat_id,))
    recipient_id = cursor.fetchone()
    conn.close()
    
    return recipient_id[0] if recipient_id else None

def get_sender(recipient_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT sender_id FROM active_chats WHERE recipient_id = ?''', (recipient_id,))
    sender_id = cursor.fetchone()
    conn.close()
    
    return sender_id[0] if sender_id else None

def get_recipient_to(sender_id_to):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT recipient_id FROM active_chats WHERE sender_id = ?''', (sender_id_to,))
    recipient_id = cursor.fetchone()
    conn.close()
    
    return recipient_id[0] if recipient_id else None

def get_sender_to(chat_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT sender_id FROM active_chats WHERE sender_id = ?''', (chat_id,))
    sender_id = cursor.fetchone()
    conn.close()
    
    return sender_id[0] if sender_id else None

def send_new_buttons_sender_id_to(language, chat_id):
    connection, cursor, user = initialize_database(chat_id)
    prefix = user[2]
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    if language == 'rus':
        stats_button = types.KeyboardButton("📊 Профиль")
        referrals_button = types.KeyboardButton("💎 Награда")
        language_ru_button = types.KeyboardButton("🌎 Язык")
        settings_ru_button = types.KeyboardButton("⚙️ Настройки")
        support_ru_button = types.KeyboardButton("🛠 Помощь")
        grand_ru_button = types.KeyboardButton("💠 G-бонус")
        keyboard.add(stats_button, referrals_button, language_ru_button, settings_ru_button, support_ru_button, grand_ru_button)
        if prefix == "free":
            sotrud_button = types.KeyboardButton("📢 Сотрудничество")
            keyboard.add(sotrud_button)            
        # Если пользователь имеет права администратора
        if chat_id in allowed_users:
            bd_button = types.KeyboardButton("🌐 База")
            staff_commands_button = types.KeyboardButton("📝 Команды")
            info_button = types.KeyboardButton("👁‍🗨 Info")
            if chat_id == 1858164732:
                ad_button = types.KeyboardButton("📢 Реклама")
                keyboard.add(bd_button, staff_commands_button, info_button, ad_button)
            else:
                keyboard.add(bd_button, staff_commands_button, info_button)
    elif language == 'en':
        keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        stats_button = types.KeyboardButton("📊 Statistics")
        referrals_button = types.KeyboardButton("💎 Rewards")
        language_en_button = types.KeyboardButton("🌎 Language")
        settings_en_button = types.KeyboardButton("⚙️ Settings")
        support_en_button = types.KeyboardButton("🛠 Support")
        grand_en_button = types.KeyboardButton("💠 G-bonus")
        keyboard.add(stats_button, referrals_button, language_en_button, settings_en_button, support_en_button, grand_en_button)

        # Если пользователь имеет права администратора
        if chat_id in allowed_users:
            bd_button = types.KeyboardButton("🌐 База")
            staff_commands_button = types.KeyboardButton("📝 Команды")
            info_button = types.KeyboardButton("👁‍🗨 Info")
            if chat_id == 1858164732:
                ad_button = types.KeyboardButton("📢 Реклама")
                keyboard.add(bd_button, staff_commands_button, info_button, ad_button)
            else:
                keyboard.add(bd_button, staff_commands_button, info_button)
    
    return keyboard

def send_new_buttons_sender_id_to(language, chat_id):
    connection, cursor, user = initialize_database(chat_id)
    prefix = user[2]
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    if language == 'rus':
        stats_button = types.KeyboardButton("📊 Профиль")
        referrals_button = types.KeyboardButton("💎 Награда")
        language_ru_button = types.KeyboardButton("🌎 Язык")
        settings_ru_button = types.KeyboardButton("⚙️ Настройки")
        support_ru_button = types.KeyboardButton("🛠 Помощь")
        grand_ru_button = types.KeyboardButton("💠 G-бонус")
        keyboard.add(stats_button, referrals_button, language_ru_button, settings_ru_button, support_ru_button, grand_ru_button)
        if prefix == "free":
            sotrud_button = types.KeyboardButton("📢 Сотрудничество")
            keyboard.add(sotrud_button)            
        # Если пользователь имеет права администратора
        if chat_id in allowed_users:
            bd_button = types.KeyboardButton("🌐 База")
            staff_commands_button = types.KeyboardButton("📝 Команды")
            info_button = types.KeyboardButton("👁‍🗨 Info")
            if chat_id == 1858164732:
                ad_button = types.KeyboardButton("📢 Реклама")
                keyboard.add(bd_button, staff_commands_button, info_button, ad_button)
            else:
                keyboard.add(bd_button, staff_commands_button, info_button)
    elif language == 'en':
        keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        stats_button = types.KeyboardButton("📊 Statistics")
        referrals_button = types.KeyboardButton("💎 Rewards")
        language_en_button = types.KeyboardButton("🌎 Language")
        settings_en_button = types.KeyboardButton("⚙️ Settings")
        support_en_button = types.KeyboardButton("🛠 Support")
        grand_en_button = types.KeyboardButton("💠 G-bonus")
        keyboard.add(stats_button, referrals_button, language_en_button, settings_en_button, support_en_button, grand_en_button)

        # Если пользователь имеет права администратора
        if chat_id in allowed_users:
            bd_button = types.KeyboardButton("🌐 База")
            staff_commands_button = types.KeyboardButton("📝 Команды")
            info_button = types.KeyboardButton("👁‍🗨 Info")
            if chat_id == 1858164732:
                ad_button = types.KeyboardButton("📢 Реклама")
                keyboard.add(bd_button, staff_commands_button, info_button, ad_button)
            else:
                keyboard.add(bd_button, staff_commands_button, info_button)
    
    return keyboard

def delete_chats(sender_id_to):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM active_chats WHERE sender_id = ?''', (sender_id_to, ))
    conn.commit()
    conn.close()

def get_recipient(user_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT recipient_id FROM active_chats WHERE recipient_id = ?''', (user_id,))
    recipient_id = cursor.fetchone()
    conn.close()
    
    return recipient_id[0] if recipient_id else None

def get_sender_language(sender_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT language FROM active_chats WHERE sender_id = ?''', (sender_id,))
    recipient_id = cursor.fetchone()
    conn.close()
    
    return recipient_id[0] if recipient_id else None


@bot.message_handler(func=lambda message: message.text in ["🔇 Завершить", "🔇 End"])
def cancel_buttons_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            language_user = get_user_language(chat_id)
            recipient_id = get_recipient(chat_id)
            sender_id = get_sender(recipient_id)
            sender_id_to = get_sender_to(chat_id)
            language_sender = get_sender_language(sender_id)
            recipient_id_to = get_recipient_to(sender_id_to)
            rk_keyboard = rank_keyboard()
            language = "rus"
            lk_keyboard = send_new_buttons_recipient(language, recipient_id)
            sender_keyboard = send_new_buttons_sender_id_to(language_user, sender_id_to)
            recipient_keyboard = send_new_buttons_sender_id_to(language, recipient_id_to)
        if sender_id: # сотрудник
            if language_sender == "rus":
                bot.send_message(sender_id, "Технический специалист завершил чат с тобой. Пожалуйста, оцените качество помощи! 🛠️", reply_markup=rk_keyboard)
            else:
                bot.send_message(sender_id, "The technician has finished chatting with you. Please rate the quality of help! 🛠️", reply_markup=rk_keyboard)
            bot.send_message(recipient_id, f"Ожидай ответа от собеседника ({sender_id})")
        else:
            bot.send_message(recipient_id_to, f"{sender_id_to}, собеседник завершил чат с тобой. 👋",reply_markup=recipient_keyboard)
            if language_user == "rus":
                bot.send_message(sender_id_to, f"Ты завершил(а) чат с сотрудником технической поддержки! ✅  Благодарим за обращение!", reply_markup=sender_keyboard)
            else:
                bot.send_message(sender_id_to, f"You have completed a chat with a technical support staff member! ✅ Thank you for contacting us!", reply_markup=sender_keyboard)
            delete_chats(sender_id_to)


    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '🔇 Завершить':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @username\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)


@bot.message_handler(func=lambda message: message.text in ["👮‍♀️ Ограничить"])
def cancel_buttons_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            recipient_id = get_recipient(chat_id)
            sender_id = get_sender(recipient_id)
            sender_id_to = get_sender_to(chat_id)
            recipient_id_to = get_recipient_to(sender_id_to)
            language = "rus"
            police = create_keyboard_police()
            bot.send_message(recipient_id, f"Выбери на какое время запретить пользоваться Технической поддержкой?",reply_markup=police)


    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '👮‍♀️ Ограничить':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @username\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)



def check_expired_users():
    """
    Проверяет время блокировки для пользователей и удаляет их, если время блокировки истекло.
    """

    connection = connect_to_db('chat_data.db')
    cursor = connection.cursor()

    # Получаем текущее время
    current_time = datetime.now()

    # Получаем всех заблокированных пользователей
    cursor.execute("SELECT sender_id, block_time FROM police")
    blocked_users = cursor.fetchall()

    # Проверяем время блокировки каждого пользователя
    for user_id, block_time_str in blocked_users:
        block_time = datetime.strptime(block_time_str, '%Y-%m-%d %H:%M:%S.%f') # Преобразуем строку в datetime
        if current_time > block_time:
            # Время блокировки истекло, удаляем пользователя из базы данных
            cursor.execute("DELETE FROM police WHERE sender_id = ?", (user_id,))
            print(f"Пользователь с ID {user_id} удален из базы данных.")

    connection.commit()
    connection.close()

def block_user(sender_id, block_time):
    """
    Записывает информацию о блокировке пользователя в таблицу "police".

    Args:
        sender_id (INTEGER): ID пользователя, которому наложено ограничение
        block_time (timedelta): Время блокировки (timedelta объект)
    """

    connection = connect_to_db('chat_data.db')
    cursor = connection.cursor()

    # Создаем триггер для обнуления значений после истечения срока блокировки
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS reset_block_time AFTER INSERT ON police
        BEGIN
            UPDATE police
            SET block_time = NULL
            WHERE datetime('now') > block_time;
        END;
    """)

    # Получаем текущее время
    current_time = datetime.now()

    # Вычисляем конечное время блокировки
    end_time = current_time + block_time

    # Записываем данные в таблицу
    cursor.execute("""
        INSERT INTO police (sender_id, block_time)
        VALUES (?, ?)
    """, (sender_id, end_time))

    connection.commit()
    connection.close()


@bot.message_handler(func=lambda message: message.text in ["⚡️ День"])
def cancel_buttons_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            recipient_id = get_recipient(chat_id)
            sender_id = get_sender(recipient_id)
            sender_id_to = get_sender_to(chat_id)
            recipient_id_to = get_recipient_to(sender_id_to)
            language_user = get_sender_language(sender_id)
            language = "rus"
            block_time = timedelta(days=1)
            lk_keyboard = send_new_buttons_recipient(language, recipient_id)
            sender_keyboard = send_new_buttons_sender_id_to(language_user, sender_id_to)
            end_time = (datetime.now() + block_time).strftime("%d.%m.%Y %H:%M")
            end_en_time = (datetime.now() + block_time).strftime("%m/%d/%Y %I:%M %p")
            if language_user == "rus":
                bot.send_message(sender_id, f"Технический специалист завершил чат с тобой. 🛠️ На тебя наложено ограничение в использовании технической поддержки до {end_time}.", reply_markup=sender_keyboard)
            else:
                bot.send_message(sender_id, f"The technician has finished chatting with you. 🛠️ You are restricted from using technical support until {end_en_time}.", reply_markup=sender_keyboard)
            bot.send_message(recipient_id, f"Вы ограничили пользователя на 1 день.",reply_markup=lk_keyboard)
            block_user(sender_id, block_time)
            delete_chats(sender_id_to)


    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '⚡️ День':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @username\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)


@bot.message_handler(func=lambda message: message.text in ["⚡️ Неделя"])
def cancel_buttons_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            recipient_id = get_recipient(chat_id)
            sender_id = get_sender(recipient_id)
            sender_id_to = get_sender_to(chat_id)
            recipient_id_to = get_recipient_to(sender_id_to)
            language_user = get_sender_language(sender_id)
            language = "rus"
            block_time = timedelta(days=7)
            lk_keyboard = send_new_buttons_recipient(language, recipient_id)
            sender_keyboard = send_new_buttons_sender_id_to(language_user, sender_id_to)
            end_time = (datetime.now() + block_time).strftime("%d.%m.%Y %H:%M")
            end_en_time = (datetime.now() + block_time).strftime("%m/%d/%Y %I:%M %p")
            if language_user == "rus":
                bot.send_message(sender_id, f"Технический специалист завершил чат с тобой. 🛠️ На тебя наложено ограничение в использовании технической поддержки до {end_time}.", reply_markup=sender_keyboard)
            else:
                bot.send_message(sender_id, f"The technician has finished chatting with you. 🛠️ You are restricted from using technical support until {end_en_time}.", reply_markup=sender_keyboard)
            bot.send_message(recipient_id, f"Вы ограничили пользователя на 7 дней.",reply_markup=lk_keyboard)
            block_user(sender_id, block_time)
            delete_chats(sender_id_to)


    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '⚡️ Неделя':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @username\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)


@bot.message_handler(func=lambda message: message.text in ["⚡️ Месяц"])
def cancel_buttons_handler(message):
    try:
        if message.chat.type == "private":
            chat_id = message.from_user.id
            recipient_id = get_recipient(chat_id)
            sender_id = get_sender(recipient_id)
            sender_id_to = get_sender_to(chat_id)
            recipient_id_to = get_recipient_to(sender_id_to)
            language_user = get_sender_language(sender_id)
            language = "rus"
            block_time = timedelta(days=30)
            lk_keyboard = send_new_buttons_recipient(language, recipient_id)
            sender_keyboard = send_new_buttons_sender_id_to(language_user, sender_id_to)
            end_time = (datetime.now() + block_time).strftime("%d.%m.%Y %H:%M")
            end_en_time = (datetime.now() + block_time).strftime("%m/%d/%Y %I:%M %p")
            if language_user == "rus":
                bot.send_message(sender_id, f"Технический специалист завершил чат с тобой. 🛠️ На тебя наложено ограничение в использовании технической поддержки до {end_time}.", reply_markup=sender_keyboard)
            else:
                bot.send_message(sender_id, f"The technician has finished chatting with you. 🛠️ You are restricted from using technical support until {end_en_time}.", reply_markup=sender_keyboard)
            bot.send_message(recipient_id, f"Вы ограничили пользователя на 30 дней.",reply_markup=lk_keyboard)
            block_user(sender_id, block_time)
            delete_chats(sender_id_to)


    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '⚡️ Месяц':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @username\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)


# Функция для создания клавиатуры получателя
def create_keyboard_recipient():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    police_button = types.KeyboardButton("👮‍♀️ Ограничить")
    close_call_rus_button = types.KeyboardButton("🔇 Завершить")
    keyboard.add(police_button, close_call_rus_button)
    return keyboard

# Функция для создания клавиатуры получателя
def create_keyboard_police():
    keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    day_button = types.KeyboardButton("⚡️ День")
    week_button = types.KeyboardButton("⚡️ Неделя")
    month_button = types.KeyboardButton("⚡️ Месяц")
    keyboard.add(day_button, week_button, month_button)
    return keyboard


# Функция для создания клавиатуры отправителя
def create_keyboard_sender(language_user):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if language_user == "rus":
        close_call_rus_button = types.KeyboardButton("🔇 Завершить")
    else:
        close_call_rus_button = types.KeyboardButton("🔇 End") 
    keyboard.add(close_call_rus_button)
    return keyboard





# Функция для отображения инлайн-клавиатуры с кнопками групп
def show_group_buttons(chat_id):
    try:
        current_language = get_user_language(chat_id)
        language = current_language
        conn, cursor = create_connection()
        cursor.execute("SELECT DISTINCT chat_id, chat_name FROM users WHERE user_id=?", (chat_id,))
        groups = cursor.fetchall()
        keyboard = types.InlineKeyboardMarkup()
        if language == "rus":
            keyboard.row(types.InlineKeyboardButton("Вся статистика", callback_data="all_stats"))
        else:
            keyboard.row(types.InlineKeyboardButton("All statistics", callback_data="all_stats"))
        for group in groups:
            keyboard.row(types.InlineKeyboardButton(group[1], callback_data=f"group_{group[0]}"))
        return keyboard
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при отображение списка групп пользователя':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{chat_id.from_user.username if chat_id.from_user else 'N/A'}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

@bot.callback_query_handler(func=lambda call: call.data == 'back_profile_to_groups')
def back_to_groups_callback_handler(call):
    try:
        # Получаем информацию о чате из объекта сообщения
        chat_id = call.message.chat.id
        message_id = call.message.message_id

        # Проверка, что сообщение отправлено в личном чате с ботом
        if call.message.chat.type == "private":
            user_id = call.from_user.id
            username = call.from_user.username
            button_pressed = call.data
            current_language = get_user_language(user_id)
            language = current_language
            conn, cursor = create_connection()
            cursor.execute("SELECT SUM(message_count), SUM(bonus_count), SUM(word_count), SUM(warn_count) FROM users WHERE user_id=?", (user_id,))
            user_stats = cursor.fetchone()

            # Проверяем, что есть статистика для пользователя
            if language == "rus":
                total_stats_message = f"🚀 Здесь ты найдешь свою статистика, которая поможет отслеживать твой прогресс в группах. 🌟"
            else:
                total_stats_message = f"🚀 Here you will find your own stats to help you track your progress in the groups. 🌟"
            keyboard = show_group_buttons(user_id)
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=total_stats_message, reply_markup=keyboard)

        else:
            pass
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '📊 Профиль - назад':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {user_id}\n"
            f"• Username: @{username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)




# Обработчик нажатия на кнопку "📊 Статистика"
@bot.message_handler(func=lambda message: message.text in ["📊 Профиль", "📊 Statistics"])
def stats_button_handler(message):
    try:
        # Проверка, что сообщение отправлено в личном чате с ботом
        if message.chat.type == "private":
            user_id = message.from_user.id
            chat_id = message.from_user.id
            username = message.from_user.username
            current_language = get_user_language(user_id)
            language = current_language
            conn, cursor = create_connection()
            cursor.execute("SELECT SUM(message_count), SUM(bonus_count), SUM(word_count), SUM(warn_count) FROM users WHERE user_id=?", (user_id,))
            user_stats = cursor.fetchone()

            # Проверяем, что есть статистика для пользователя
            if user_stats and not all(value is None for value in user_stats):
                if language == "rus":
                    total_stats_message = f"🚀 Здесь ты найдешь свою статистика, которая поможет отслеживать твой прогресс в группах. 🌟"
                else:
                    total_stats_message = f"🚀 Here you will find your own stats to help you track your progress in the groups. 🌟"
                keyboard = show_group_buttons(user_id)
                bot.send_message(user_id, total_stats_message, reply_markup=keyboard)
            else:
                if language == "rus":
                    stats_no = f"Упс! У тебя еще нет статистики. Присоединяйся к нашей группе, где есть Grand Moderator, чтобы начать зарабатывать бонус grand! 💪🚀"
                else:
                    stats_no = f"Oops, you don't have stats yet. Join our group with Grand Moderator to start earning bonus GRAND! 💪🚀 "
                keyboard = types.InlineKeyboardMarkup()
                if language == "rus":
                    stats_no_button = types.InlineKeyboardButton("🚀 Присоединиться 🚀", url="https://t.me/chatgrandtime/")
                else:
                    stats_no_button = types.InlineKeyboardButton("🚀 Join 🚀", url="https://t.me/GRANDTIMECHATENG/")
                keyboard.add(stats_no_button)
                bot.send_message(user_id, stats_no, reply_markup=keyboard)

        else:
            pass
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку '📊 Профиль':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)





# Обработчик нажатия на кнопки инлайн-клавиатуры
@bot.callback_query_handler(func=lambda call: call.data.startswith(('group_', 'all_stats')))
def group_stats_callback(call):
    try:
        user_id = call.from_user.id
        chat_id = call.message.chat.id
        message_id = call.message.message_id
        username = call.from_user.username
        button_pressed = call.data
        
        current_language = get_user_language(user_id)
        language = current_language
        
        if call.data == 'all_stats':
            conn, cursor = create_connection()
            cursor.execute("SELECT COUNT(*) FROM users WHERE user_id=?", (user_id,))
            user_exists = cursor.fetchone()[0]

            if user_exists == 0:
                if language == "rus":
                    stats_no = f"Упс! У тебя еще нет статистики. Присоединяйся к нашей группе, где есть Grand Moderator, чтобы начать зарабатывать бонус grand! 💪🚀"
                else:
                    stats_no = f"Oops, you don't have stats yet. Join our group with Grand Moderator to start earning bonus GRAND! 💪🚀 "
                keyboard = types.InlineKeyboardMarkup()
                if language == "rus":
                    stats_no_button = types.InlineKeyboardButton("🚀 Присоединиться 🚀", url="https://t.me/chatgrandtime/")
                else:
                    stats_no_button = types.InlineKeyboardButton("🚀 Join 🚀", url="https://t.me/GRANDTIMECHATENG/")
                keyboard.add(stats_no_button)
                bot.send_message(user_id, stats_no, reply_markup=keyboard)
            else:
                cursor.execute("SELECT SUM(message_count), SUM(bonus_count), SUM(word_count), SUM(warn_count) FROM users WHERE user_id=?", (user_id,))
                user_stats = cursor.fetchone()
                
                if language == "rus":
                    total_stats_message = f"Твоя статистика:\n\n💬 Всего сообщений: <b>{user_stats[0]}</b>\n💠 Всего GRAND бонусов: <b>{round(user_stats[1], 2)}</b>\n📝 Всего слов: <b>{user_stats[2]}</b>\n⚠️ Всего предупреждений: <b>{user_stats[3]}</b>\n"
                else:
                    total_stats_message = f"Your stats:\n\n💬 Total messages: <b>{user_stats[0]}</b>\n💠 Total GRAND bonuses: <b>{round(user_stats[1], 2)}</b>\n📝 Total words: <b>{user_stats[2]}</b>\n⚠️ Total Warnings: <b>{user_stats[3]}</b>\n"
                keyboard = types.InlineKeyboardMarkup()
                if language == "rus":
                    back_button = types.InlineKeyboardButton("⬅️ Назад", callback_data="back_profile_to_groups")
                else:
                    back_button = types.InlineKeyboardButton("⬅️ Back", callback_data="back_profile_to_groups")
                keyboard.add(back_button)
                bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=total_stats_message, reply_markup=keyboard, parse_mode='HTML')


        else:
            group_id = int(call.data.replace('group_', ''))
            conn, cursor = create_connection()
            cursor.execute("SELECT chat_name, SUM(message_count), SUM(bonus_count), SUM(word_count), SUM(warn_count) FROM users WHERE chat_id=? AND user_id=?", (group_id, user_id))
            group_stats = cursor.fetchone()
            if group_stats:
                if language == "rus":
                    group_stats_message = f"Статистика из <b>{group_stats[0]}</b>:\n\n💬 Всего сообщений: <b>{group_stats[1]}</b>\n💠 Всего бонусов: <b>{round(group_stats[2], 2)}</b>\n📝 Всего слов: <b>{group_stats[3]}</b>\n⚠️ Всего предупреждений: <b>{group_stats[4]}</b>\n"
                else:
                    group_stats_message = f"Stats from <b>{group_stats[0]}</b>:\n\n💬 Total messages: <b>{group_stats[1]}</b>\n💠 Total GRAND bonuses: <b>{round(group_stats[2], 2)}</b>\n📝 Total words: <b>{group_stats[3]}</b>\n⚠️ Total Warnings: <b>{group_stats[4]}</b>\n"
                keyboard = types.InlineKeyboardMarkup()
                if language == "rus":
                    back_button = types.InlineKeyboardButton("⬅️ Назад", callback_data="back_profile_to_groups")
                else:
                    back_button = types.InlineKeyboardButton("⬅️ Back", callback_data="back_profile_to_groups")
                keyboard.add(back_button)
                bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=group_stats_message, reply_markup=keyboard, parse_mode='HTML')
            else:
                if language == "rus":
                    bot.send_message(user_id, f"Упс! У тебя еще нет статистики. Присоединяйся к нашей группе, где есть Grand Moderator, чтобы начать собирать данные! 💪🚀")
                else:
                    bot.send_message(user_id, f"Oops, you don't have stats yet. Join our group with a Grand Moderator to start collecting data! 💪🚀")
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при нажатии на кнопку 'group_':\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{call.from_user.username if call.from_user else 'N/A'}\n"
            f"• Кнопка: {button_pressed}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

def ad_buttons(user_id):
    if user_id in prod_users:
        keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        no_prefix = types.KeyboardButton("no 💠")
        basa = types.KeyboardButton("📂 База")
        balance = types.KeyboardButton("💰 Баланс")
        keyboard.add(no_prefix, basa, balance)

        return keyboard
    else:
        pass

def save_proposal(user_id, username, proposal, message_id):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO proposals (user_id, username, proposal, message_id) VALUES (?, ?, ?, ?)', 
                   (user_id, username, proposal, message_id))
    conn.commit()
    conn.close()

def get_proposal(message_id):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, username, proposal FROM proposals WHERE message_id = ?', (message_id,))
    result = cursor.fetchone()
    conn.close()
    return result

@bot.message_handler(func=lambda message: message.text == "📢 Сотрудничество")
def ad_button_handler(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Написать предложение ✍️", callback_data=f"make_proposal_{user_id}")
    markup.add(button)

    cooperation_text = f"👋 Здравствуйте, {username}!\n\n" \
                       "Спасибо за ваш интерес к сотрудничеству. Мы предлагаем несколько вариантов:\n\n" \
                       "🔹 Заказать разработку телеграм-бота 🤖\n" \
                       "🔹 Заказать рекламу в наших группах и пользователям 📢\n" \
                       "🔹 Свой вариант сотрудничества 💡\n\n" \
                       "Пожалуйста, нажмите на кнопку ниже, чтобы сделать предложение."

    bot.send_message(user_id, cooperation_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("make_proposal_"))
def proposal_handler(call):
    user_id = call.from_user.id
    message_id = call.message.message_id

    bot.edit_message_text("✏️ Пожалуйста, напишите ваше предложение:", chat_id=user_id, message_id=message_id)

    bot.register_next_step_handler(call.message, process_proposal, message_id)

def process_proposal(message, message_id):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    proposal = message.text

    save_proposal(user_id, username, proposal, message_id)

    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Отправить 📤", callback_data=f"send_proposal_{message_id}")
    markup.add(button)

    bot.send_message(user_id, "📋 Вы написали:\n\n" + proposal + "\n\nНажмите 'Отправить 📤', чтобы отправить ваше предложение.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("send_proposal_"))
def confirm_sending(call):
    message_id = int(call.data.split('_')[-1])

    result = get_proposal(message_id)
    if result:
        user_id, username, proposal = result
        bot.edit_message_text("✅ Ваше предложение отправлено. Ожидайте обратной связи.", chat_id=user_id, message_id=call.message.message_id)
        bot.send_message(-1001810568716, f"🔔 Новое предложение от @{username} (ID: {user_id}):\n\n{proposal}")

def create_db():
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            proposal TEXT,
            message_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

create_db()

@bot.message_handler(func=lambda message: message.text == "📢 Реклама")
def ad_button_handler(message):
    user_id = message.from_user.id
    if message.from_user.id in prod_users:
        keyboard = ad_buttons(user_id)
        bot.send_message(chat_id=user_id, text="Рекламный режим", reply_markup=keyboard)
    else:
        bot.send_message(chat_id=user_id, text="Эта кнопка не работает!")

@bot.message_handler(func=lambda message: message.text == "💰 Баланс")
def balance_button_handler(message):
    user_id = message.from_user.id
    if user_id in prod_users:
        total_balance = get_total_balance()
        ad_balances = get_ad_balances()

        # Отправляем общий баланс
        bot.send_message(chat_id=user_id, text=f"Общий баланс: {total_balance}")

        # Формируем сообщение о балансе для каждой рекламы
        message_text = ""
        for index, (ad_id, amount, data) in enumerate(ad_balances, start=1):
            message_text += f"[{ad_id}, Сумма: {amount}, {data}]\n"
            # Отправляем сообщение каждые 20 балансов или в конце списка
            if index % 20 == 0 or index == len(ad_balances):
                bot.send_message(chat_id=user_id, text=message_text)
                message_text = ""
    else:
        bot.send_message(chat_id=user_id, text="Эта кнопка не работает!")


def get_total_balance():
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM balance2")
    total_balance = cursor.fetchone()[0]

    conn.close()

    return total_balance

def get_ad_balances():
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    cursor.execute("SELECT ad_id, amount, data FROM balance2")
    ad_balances = cursor.fetchall()

    conn.close()

    return ad_balances

@bot.message_handler(func=lambda message: message.text == "📂 База")
def ad_button_handler(message):
    user_id = message.from_user.id
    if message.from_user.id in prod_users:
        all_ad_info = get_all_ad_info()

        # Форматируем информацию для отправки
        formatted_info = "\n".join([f"[{ad_id} ({send_count}), User: {user_count}, Group: {group_count}]" for ad_id, send_count, user_count, group_count in all_ad_info])

        bot.send_message(chat_id=user_id, text="Информация о рекламных записях:\n" + formatted_info)
    else:
        bot.send_message(chat_id=user_id, text="Эта кнопка не работает!")

def get_all_ad_info():
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    # Выполняем запрос к базе данных для получения данных для всех записей
    cursor.execute("SELECT ad_id, send_count, user_count, group_count FROM ad")
    all_ad_info = cursor.fetchall()

    conn.close()

    return all_ad_info

def count_users_with_prefix_and_language(prefix, language):
    conn = connect_to_db('database.db')
    cursor = conn.cursor()

    # Выполняем запрос к базе данных для подсчета пользователей с заданными значениями prefix и language
    cursor.execute("SELECT COUNT(*) FROM users WHERE prefix=? AND language=?", (prefix, language))
    count = cursor.fetchone()[0]

    conn.close()

    return count

def count_chats_with_prefix_and_language(prefix, language):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()

    # Выполняем запрос к базе данных для подсчета пользователей с заданными значениями prefix и language
    cursor.execute("SELECT COUNT(*) FROM chats WHERE prefix=? AND language=?", (prefix, language))
    count = cursor.fetchone()[0]

    conn.close()

    return count

def count_active_users_in_chats_with_prefix_and_language(prefix, language):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()

    # Выполняем запрос к базе данных для выбора чатов с заданными значениями prefix и language
    cursor.execute("SELECT chat_id FROM chats WHERE prefix=? AND language=?", (prefix, language))
    chat_ids = cursor.fetchall()

    total_active_users = 0

    # Перебираем каждый чат и подсчитываем количество активных пользователей
    for chat_id in chat_ids:
        cursor.execute("SELECT SUM(active_users) FROM chats WHERE chat_id=?", (chat_id[0],))
        active_users_count = cursor.fetchone()[0]
        total_active_users += active_users_count

    conn.close()

    return total_active_users

@bot.message_handler(func=lambda message: message.text == "no 💠")
def ad_button_handler(message):
    user_id = message.from_user.id
    if message.from_user.id in prod_users:
        prefix = "free"
        language = "rus"
        count_user = count_users_with_prefix_and_language(prefix, language)
        count_group = count_chats_with_prefix_and_language(prefix, language)
        active_user = count_active_users_in_chats_with_prefix_and_language(prefix, language)
        bot.send_message(chat_id=user_id, text=f"В базе {count_user} пользователей, и {count_group} групп общее количество активных пользователей ({active_user})")
    else:
        bot.send_message(chat_id=user_id, text="Эта кнопка не работает!")

def users_id_with_prefix_and_language(prefix, language):
    conn = connect_to_db('database.db')
    cursor = conn.cursor()

    # Выполняем запрос к базе данных для выбора чатов с заданными значениями prefix и language
    cursor.execute("SELECT user_id FROM users WHERE prefix=? AND language=?", (prefix, language))
    user_ids = cursor.fetchall()

    conn.close()

    return user_ids

def chats_id_with_prefix_and_language(prefix, language):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()

    # Выполняем запрос к базе данных для выбора чатов с заданными значениями prefix и language
    cursor.execute("SELECT chat_id FROM chats WHERE prefix=? AND language=?", (prefix, language))
    chat_ids = cursor.fetchall()

    conn.close()

    return chat_ids

def ad_info_sotrud(ad_id):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    # Выполняем запрос к базе данных для получения данных по ad_id
    cursor.execute("SELECT ad_user, ad_group, ad_text, tbutton1, tbutton2, tbutton3, nbutton1, nbutton2, nbutton3 FROM ad WHERE ad_id=?", (ad_id,))
    ad_info = cursor.fetchone()

    conn.close()

    return ad_info

def get_photo_from_db(ad_id):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    # Выполняем запрос к базе данных для получения данных по photo_id
    cursor.execute("SELECT file_id FROM photos WHERE ad_id=?", (ad_id,))
    photo_data = cursor.fetchone()

    conn.close()

    return photo_data

def get_ad_with_max_send_count():
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    # Проверяем, есть ли записи в таблице
    cursor.execute("SELECT COUNT(*) FROM ad")
    count_result = cursor.fetchone()

    if count_result[0] == 0:
        conn.close()
        return None

    # Выполняем запрос к базе данных для получения ad_id с наибольшим значением send_count
    cursor.execute("SELECT ad_id FROM ad ORDER BY send_count DESC LIMIT 1")
    result = cursor.fetchone()

    conn.close()

    # Проверяем, что результат не пустой
    if result:
        ad_id = result[0]
        return ad_sotrudnichestvo(ad_id)
    else:
        return None

# Функция для отправки рекламы сотрудничества
def ad_sotrudnichestvo(ad_id):
    prefix = "free"
    language = "rus"
    directory = f"photos/{ad_id}"
    ad_info = ad_info_sotrud(ad_id)
    photo_data = get_photo_from_db(ad_id)
    user_ids = users_id_with_prefix_and_language(prefix, language)
    chat_ids = chats_id_with_prefix_and_language(prefix, language)
    ad_user, ad_group, ad_text, tbutton1, tbutton2, tbutton3, nbutton1, nbutton2, nbutton3 = ad_info
    keyboard = types.InlineKeyboardMarkup()
    url_button1 = types.InlineKeyboardButton(text=f"{tbutton1}", url=f"{nbutton1}")
    url_button2 = types.InlineKeyboardButton(text=f"{tbutton2}", url=f"{nbutton2}")
    url_button3 = types.InlineKeyboardButton(text=f"{tbutton3}", url=f"{nbutton3}")
    keyboard.add(url_button1)
    keyboard.add(url_button2)
    keyboard.add(url_button3)

    try:
        if ad_user == "yes":
            user_count = 0
            for user_id in user_ids:
                with open(f"{directory}/{photo_data[0]}.jpg", 'rb') as photo_file:
                    bot.send_photo(user_id, photo_file, caption=ad_text, reply_markup=keyboard, parse_mode="HTML")
                    user_count += 1
                    update_ad_user_count(ad_id, user_count)
        else:
            pass
    except Exception as e:
        logging.error(f"Error sending ad to user: {e}")
    
    try:
        if ad_group == "yes":
            group_count = 0
            for chat_id in chat_ids:
                with open(f"{directory}/{photo_data[0]}.jpg", 'rb') as photo_file:
                    bot.send_photo(chat_id, photo_file, caption=ad_text, reply_markup=keyboard, parse_mode="HTML")
                    group_count += 1
                    update_ad_chat_count(ad_id, group_count)
        else:
            pass
    except Exception as e:
        logging.error(f"Error sending ad to group: {e}")
    
    try:
        send_count = decrement_send_count(ad_id)
        text = f"Рекламу получили:\n\n {user_count} пользователей\n{group_count} групп\nРеклама ещё отправится: {send_count} раз(а)"
        text += ad_text
        with open(f"{directory}/{photo_data[0]}.jpg", 'rb') as photo_file:
            bot.send_photo(ad_id, photo_file, caption=text, reply_markup=keyboard, parse_mode="HTML")
            bot.send_photo(-1001810568716, photo_file, caption=text, reply_markup=keyboard, parse_mode="HTML")
            check_and_delete_ad(ad_id)
    except Exception as e:
        logging.error(f"Error sending summary message: {e}")

@bot.message_handler(commands=['balance'])
def balance_command(message):
    # Разделяем текст команды по пробелам
    command_parts = message.text.split()

    # Проверяем, что в команде указаны все необходимые параметры
    if len(command_parts) != 4:
        bot.reply_to(message, "Неверный формат команды. Используйте /balance [ad_id] [amount] [data]")
        return

    try:
        # Извлекаем ad_id, amount и data из команды
        ad_id = int(command_parts[1])
        amount = float(command_parts[2])
        data = command_parts[3]

        # Вызываем функцию добавления в баланс
        add_balance(ad_id, amount, data)

        bot.reply_to(message, f"Сумма {amount} успешно добавлена к балансу с ID {ad_id} с данными '{data}'.")
    except ValueError:
        bot.reply_to(message, "Неверный формат числа. Пожалуйста, убедитесь, что amount указан в числовом формате.")

@bot.message_handler(commands=['remove_balance'])
def remove_balance_command(message):
    # Разделяем текст команды по пробелам
    command_parts = message.text.split()

    # Проверяем, что в команде указан ad_id
    if len(command_parts) != 2:
        bot.reply_to(message, "Неверный формат команды. Используйте /remove_balance [ad_id]")
        return

    try:
        # Извлекаем ad_id из команды
        ad_id = int(command_parts[1])

        # Вызываем функцию удаления записи из баланса
        if remove_balance(ad_id):
            bot.reply_to(message, f"Запись с ID {ad_id} удалена из баланса.")
        else:
            bot.reply_to(message, f"Запись с ID {ad_id} не найдена в балансе.")
    except ValueError:
        bot.reply_to(message, "Неверный формат ad_id. Пожалуйста, укажите ad_id в числовом формате.")

def remove_balance(ad_id):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    try:
        # Удаляем запись из таблицы balance по ad_id
        cursor.execute("DELETE FROM balance2 WHERE ad_id = ?", (ad_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Ошибка SQLite:", e)
        conn.close()
        return False

def add_balance(ad_id, amount, data):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    try:
        # Создаем таблицу balance, если она еще не существует
        cursor.execute('''CREATE TABLE IF NOT EXISTS balance2 (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            ad_id INTEGER,
                            amount TEXT,
                            data TEXT
                          )''')

        # Добавляем значение в таблицу balance
        cursor.execute("INSERT INTO balance2 (ad_id, amount, data) VALUES (?, ?, ?)", (ad_id, amount, data))

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Ошибка SQLite:", e)

# Функция для добавления рекламы в базу данных
def add_ad_to_db(ad_id, send_count, nbutton1, tbutton1, nbutton2, tbutton2, nbutton3, tbutton3, ad_user, ad_group):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    # Добавление рекламы в базу данных
    cursor.execute("INSERT INTO ad (ad_id, ad_text, group_count, user_count, send_count, nbutton1, tbutton1, nbutton2, tbutton2, nbutton3, tbutton3, ad_user, ad_group) VALUES (?, ?, 0, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (ad_id, "non", send_count, nbutton1, tbutton1, nbutton2, tbutton2, nbutton3, tbutton3, ad_user, ad_group))

    conn.commit()
    conn.close()

# Функция для обновления текста рекламы в базе данных
def update_ad_chat_count(ad_id, group_count):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    # Обновление текста рекламы в базе данных
    cursor.execute("UPDATE ad SET group_count = ? WHERE ad_id = ?", (group_count, ad_id))

    conn.commit()
    conn.close()

# Функция для обновления текста рекламы в базе данных
def update_ad_user_count(ad_id, user_count):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    # Обновление текста рекламы в базе данных
    cursor.execute("UPDATE ad SET user_count = ? WHERE ad_id = ?", (user_count, ad_id))

    conn.commit()
    conn.close()

def check_and_delete_ad(ad_id):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    # Получаем текущее значение send_count
    cursor.execute("SELECT send_count FROM ad WHERE ad_id = ?", (ad_id,))
    result = cursor.fetchone()
    current_send_count = result[0] if result else None

    # Если значение send_count равно 0, удаляем запись
    if current_send_count == 0:
        cursor.execute("DELETE FROM ad WHERE ad_id = ?", (ad_id,))
        conn.commit()
        conn.close()
        return True  # Возвращаем True, чтобы указать, что запись была удалена
    else:
        conn.close()
        return False  # Возвращаем False, чтобы указать, что запись не была удалена

def decrement_send_count(ad_id):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    # Получаем текущее значение send_count
    cursor.execute("SELECT send_count FROM ad WHERE ad_id = ?", (ad_id,))
    result = cursor.fetchone()
    current_send_count = result[0] if result else None

    # Если значение send_count больше 0, обновляем его
    if current_send_count is not None and current_send_count > 0:
        cursor.execute("UPDATE ad SET send_count = send_count - 1 WHERE ad_id = ?", (ad_id,))
        new_send_count = current_send_count - 1
    else:
        new_send_count = current_send_count

    conn.commit()
    conn.close()

    # Возвращаем новое значение send_count
    return new_send_count

# Функция для обновления текста рекламы в базе данных
def update_ad_text(ad_id, new_text):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    # Обновление текста рекламы в базе данных
    cursor.execute("UPDATE ad SET ad_text = ? WHERE ad_id = ?", (new_text, ad_id))

    conn.commit()
    conn.close()

@bot.message_handler(commands=['ad_text'])
def ad_text(message):
    # Разделяем текст команды по пробелам
    command_parts = message.text.split()

    # Проверяем, что в команде указан ad_id и текст
    if len(command_parts) < 3:
        bot.reply_to(message, "Неверный формат команды. Используйте /ad_text [ad_id] [text]")
        return

    # Извлекаем ad_id из команды
    ad_id = command_parts[1]

    # Извлекаем текст из оставшейся части команды
    new_text = message.text.split(' ', 2)[2]

    # Вызываем функцию обновления текста рекламы
    update_ad_text(ad_id, new_text)

    bot.reply_to(message, f"Текст рекламы с ID {ad_id} обновлен.")




# Обработчик команды /adinfo
@bot.message_handler(commands=['adinfo'])
def ad_info(message):
    # Получение ad_id из аргументов команды
    ad_id = message.text.split(' ', 1)[-1]
    if not ad_id:
        bot.reply_to(message, "Вы забыли указать ad_id. Пример использования: /adinfo [ad_id]")
        return

    # Получение данных о рекламе из базы данных
    ad_data = get_ad_info_from_db(ad_id)
    if not ad_data:
        bot.reply_to(message, "Реклама с указанным ad_id не найдена.")
        return

    # Формирование ответа
    ad_text = ad_data[0]
    send_count = ad_data[1]
    nbutton1 = ad_data[2]
    tbutton1 = ad_data[3]
    nbutton2 = ad_data[4]
    tbutton2 = ad_data[5]
    nbutton3 = ad_data[6]
    tbutton3 = ad_data[7]
    ad_user = ad_data[8]
    ad_group = ad_data[9]

    reply_text = f"Данные рекламы с ad_id {ad_id}:\n\n" \
                 f"Текст рекламы: {ad_text}\n" \
                 f"Количество отправок: {send_count}\n" \
                 f"Кнопка 1: {tbutton1} - {nbutton1}\n" \
                 f"Кнопка 2: {tbutton2} - {nbutton2}\n" \
                 f"Кнопка 3: {tbutton3} - {nbutton3}\n" \
                 f"Пользователь: {ad_user}\n" \
                 f"Группа: {ad_group}"

    bot.reply_to(message, reply_text)


# Функция для получения данных о рекламе из базы данных
def get_ad_info_from_db(ad_id):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    # Выполнение запроса к базе данных для получения данных по ad_id
    cursor.execute("SELECT ad_text, send_count, nbutton1, tbutton1, nbutton2, tbutton2, nbutton3, tbutton3, ad_user, ad_group FROM ad WHERE ad_id=?", (ad_id,))
    ad_data = cursor.fetchone()

    conn.close()

    return ad_data

@bot.message_handler(commands=['remove_ad'])
def remove_ad_command(message):
    # Разделяем текст команды по пробелам
    command_parts = message.text.split()

    # Проверяем, что в команде указан ad_id
    if len(command_parts) != 2:
        bot.reply_to(message, "Неверный формат команды. Используйте /remove_ad [ad_id]")
        return

    try:
        # Извлекаем ad_id из команды
        ad_id = int(command_parts[1])

        # Вызываем функцию удаления рекламы из базы данных
        if remove_ad(ad_id):
            bot.reply_to(message, f"Реклама с ID {ad_id} удалена из базы данных.")
        else:
            bot.reply_to(message, f"Реклама с ID {ad_id} не найдена в базе данных.")
    except ValueError:
        bot.reply_to(message, "Неверный формат ad_id. Пожалуйста, укажите ad_id в числовом формате.")

def remove_ad(ad_id):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    try:
        # Удаляем рекламу из таблицы ad по ad_id
        cursor.execute("DELETE FROM ad WHERE ad_id = ?", (ad_id,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print("Ошибка SQLite:", e)
        conn.close()
        return False

# Обработчик команды "/add_ad"
@bot.message_handler(commands=['add_ad'])
def add_ad(message):
    # Получение аргументов из сообщения
    args = message.text.split()[1:]
    if len(args) != 10:
        bot.reply_to(message, "Неправильное количество аргументов. Используйте команду в следующем формате: /add_ad [ad_id] [send_count] [nbutton1] [tbutton1] [nbutton2] [tbutton2] [nbutton3] [tbutton3] [ad_user] [ad_group]")
        return
    
    try:
        ad_id = int(args[0])
        send_count = int(args[1])
    except ValueError:
        bot.reply_to(message, "ad_id и send_count должны быть числами.")
        return
    
    # Добавление рекламы в базу данных
    add_ad_to_db(ad_id, send_count, *args[2:])

    bot.reply_to(message, f"Реклама с ad_id {ad_id} успешно добавлена в базу данных.")

# Функция для сохранения фото с текстом в базу данных
def save_photo_to_db(ad_id, file_id, file_path):
    conn = connect_to_db('ad.db')
    cursor = conn.cursor()

    # Добавление фото с текстом в базу данных
    cursor.execute("INSERT INTO photos (ad_id, file_id, file_path) VALUES (?, ?, ?)",
                   (ad_id, file_id, file_path))

    conn.commit()
    conn.close()

# Обработчик получения фото
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    photo_id = message.photo[-1].file_id
    chat_id = message.chat.id
    text = message.caption
    ad_id = None
    if text and text.startswith("ad_id:"):
        ad_id = text.split(":")[1].strip()

    # Если ad_id найден, сохраняем фото с текстом в базу данных
    if ad_id:
        file_info = bot.get_file(photo_id)
        file_path = file_info.file_path
        save_photo_to_db(ad_id, message.photo[-1].file_id, file_path)
        save_photo_to_directory(ad_id, message.photo[-1].file_id, file_path)
        bot.reply_to(message, f"Фото с текстом, содержащим ad_id {ad_id}, успешно сохранено в базе данных.")
    else:
        pass

def save_photo_to_directory(ad_id, file_id, file_path):
    # Получаем URL для загрузки фото
    BOT_TOKEN = "6971843804:AAHe5i1mA2j5cRSrCoJnG8UyBEpxBCYjX6k"
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    
    # Создаем директорию для сохранения фото, если ее еще нет
    directory = f"photos/{ad_id}"
    os.makedirs(directory, exist_ok=True)

    # Загружаем фото с серверов Telegram
    response = requests.get(file_url)
    if response.status_code == 200:
        # Сохраняем фото в директории
        with open(f"{directory}/{file_id}.jpg", 'wb') as photo_file:
            photo_file.write(response.content)
        return f"{directory}/{file_id}.jpg"  # Возвращаем путь к сохраненному файлу
    else:
        return None

# Конец рекламного блока

def get_users_data():
    try:
        connection = connect_to_db('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT user_id, language FROM users")
        users_data = cursor.fetchall()
        return users_data
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении SQL-запроса для пользователей: {e}")
    finally:
        cursor.close()
        connection.close()

def get_russian_texts():
    try:
        connection = connect_to_db('chat_data.db')
        cursor = connection.cursor()
        cursor.execute("SELECT value FROM book")
        russian_texts = cursor.fetchall()
        return russian_texts
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении SQL-запроса для русских текстов: {e}")
    finally:
        cursor.close()
        connection.close()

def get_english_texts():
    try:
        connection = connect_to_db('chat_data.db')
        cursor = connection.cursor()
        cursor.execute("SELECT value FROM book_en")
        english_texts = cursor.fetchall()
        return english_texts
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении SQL-запроса для английских текстов: {e}")
    finally:
        cursor.close()
        connection.close()

def send_advertisement_to_users():
    users_data = get_users_data()
    russian_texts = get_russian_texts()
    english_texts = get_english_texts()

    if not users_data:
        print("Нет данных о пользователях")
        return

    try:
        for user_data in users_data:
            user_id, language = user_data
            try:
                random_caption = random.choice(russian_texts)[0] if language == 'rus' else random.choice(english_texts)[0]
                photo_path = 'grand.jpg'
                keyboard = types.InlineKeyboardMarkup()
                
                if language == 'rus':
                    url_ru_button = types.InlineKeyboardButton(text="Иду читать!", url="https://www.litres.ru/book/artur-grandi/grand-time-70005007/?lfrom=1117899162&ref_key=c640e512577d7235adb7f208059ba746eb3dd77dbbb2d48de86aa6ec141245fb&ref_offer=1")
                    keyboard.add(url_ru_button)
                    with open(photo_path, 'rb') as photo:
                        bot.send_photo(user_id, photo, caption=random_caption, reply_markup=keyboard)
                    print(f"Отправлено сообщение пользователю {user_id} на русском")
                elif language == 'en':
                    url_button = types.InlineKeyboardButton(text="Going read!", url="https://a.co/d/gJxsXqP")
                    keyboard.add(url_button)
                    with open(photo_path, 'rb') as photo:
                        bot.send_photo(user_id, photo, caption=random_caption, reply_markup=keyboard)
                    print(f"Sent message to user {user_id} in English")
                    
                time.sleep(5)  # задержка в 5 секунд перед отправкой следующего сообщения

            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

    except sqlite3.Error as e:
        print(f"Ошибка при выполнении SQL-запроса: {e}")


def send_advertisement_to_chats():
    try:
        # Открываем соединение с базой данных SQLite для чатов
        connection_chats = connect_to_db('chat_data.db')
        cursor_chats = connection_chats.cursor()

        # Получаем все чаты из базы данных
        cursor_chats.execute("SELECT DISTINCT chat_id, language FROM chats")
        chat_ids = cursor_chats.fetchall()

        russian_texts = get_russian_texts()
        english_texts = get_english_texts()

        # Отправляем рекламное сообщение в каждый активный чат
        for chat_id, language in chat_ids:
            try:
                random_caption = random.choice(russian_texts)[0] if language == 'rus' else random.choice(english_texts)[0]
                if language == 'rus':
                    # Если язык - русский, отправляем сообщение на русском
                    photo = open('grand.jpg', 'rb')
                    keyboard = types.InlineKeyboardMarkup()
                    url_ruschat_button = types.InlineKeyboardButton(text="Иду читать! 📚", url="https://www.litres.ru/book/artur-grandi/grand-time-70005007/?lfrom=1117899162&ref_key=c640e512577d7235adb7f208059ba746eb3dd77dbbb2d48de86aa6ec141245fb&ref_offer=1")
                    keyboard.add(url_ruschat_button)
                    bot.send_photo(chat_id, photo, caption=random_caption, reply_markup=keyboard)
                    print(f"Отправлено сообщение в чат {chat_id} на русском")
                elif language == 'en':
                    # Если язык - английский, отправляем сообщение на английском
                    photo = open('grand.jpg', 'rb')
                    keyboard = types.InlineKeyboardMarkup()
                    url_enchat_button = types.InlineKeyboardButton(text="Going read! 📚", url="https://a.co/d/gJxsXqP")
                    keyboard.add(url_enchat_button)
                    bot.send_photo(chat_id, photo, caption=random_caption, reply_markup=keyboard)
                    print(f"Sent message to chat {chat_id} in English")
                    
                time.sleep(5)  # задержка в 5 секунд перед отправкой следующего сообщения

            except Exception as e:
                error_message = (f"Ошибка при отправке сообщения в чат {chat_id}: {e}")
                

        # Закрываем соединение с базой данных для чатов
        cursor_chats.close()
        connection_chats.close()
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении SQL-запроса для чатов: {e}")

def send_message_active_users():
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()

    # Получаем список всех чатов
    cursor.execute("SELECT chat_id, language, active_users, sent_messages, earn FROM chats")
    chat_ids = cursor.fetchall()

    for chat_id, language, active_users, sent_messages, earn in chat_ids:
        try:
            if sent_messages == 0:
                if active_users >= 10:  # Условие для активных пользователей
                    if earn == "on_earn":
                        if language == "rus":
                            bot.send_message(chat_id, "Группа достигла нового уровня 🥳\n\n Теперь 👥 участники могут получать бонус GRAND 💠 за свою активность ‼️")
                        elif language == "en":
                            bot.send_message(chat_id, "The group has reached a new level 🥳\n\n 👥 members can now receive a GRAND 💠 bonus for their activity ‼️")
                    else:
                        pass
                    
                    # Обновляем значение sent_messages на 1 в таблице chats
                    cursor.execute("UPDATE chats SET sent_messages = 1 WHERE chat_id = ?", (chat_id,))
                    conn.commit()
        except Exception as e:
            error_message = (
                f"⚠️ Произошла ошибка в функции отправки сообщения о достигнутом уровне:\n"
                f"• Тип ошибки: {e.__class__.__name__}\n"
                f"• Описание: {e}\n"
                f"• Строка: {e.__traceback__.tb_lineno}\n"
                f"• Chat ID: {chat_id}\n"
                f"• Время: {datetime.now()}"
            )

            # Используйте библиотеку logging для записи сообщения об ошибке
            logging.error(error_message)

    # Закрываем соединение с базой данных после завершения цикла
    conn.close()



def send_advertisement():
    try:
        # Открываем соединение с базой данных SQLite для чатов
        connection_chats = connect_to_db('chat_data.db')
        cursor_chats = connection_chats.cursor()

        # Получаем все чаты из базы данных
        cursor_chats.execute("SELECT DISTINCT chat_id, language FROM chats")
        chat_ids = cursor_chats.fetchall()

        # Отправляем рекламное сообщение в каждый активный чат
        for chat_id, language in chat_ids:
            try:
                if language == 'rus':
                    # Если язык - русский, отправляем сообщение на русском
                    photo = open('ru_stats.jpg', 'rb')
                    keyboard = types.InlineKeyboardMarkup()
                    url_ruschat_button = types.InlineKeyboardButton(text="Посмотреть статистику 📊", url="https://t.me/gmoderator_bot?start=GRANDMain")
                    keyboard.add(url_ruschat_button)
                    bot.send_photo(chat_id, photo, caption="Хочешь увидеть свою статистику? Тогда переходи! 🚀", reply_markup=keyboard)
                    print(f"Отправлено сообщение в чат {chat_id} на русском")
                elif language == 'en':
                    # Если язык - английский, отправляем сообщение на английском
                    photo = open('en_stats.jpg', 'rb')
                    keyboard = types.InlineKeyboardMarkup()
                    url_enchat_button = types.InlineKeyboardButton(text="View stats 📊", url="https://t.me/gmoderator_bot?start=GRANDMain")
                    keyboard.add(url_enchat_button)
                    bot.send_photo(chat_id, photo, caption="Want to see your stats? Come on over! 🚀", reply_markup=keyboard)
                    print(f"Sent message to chat {chat_id} in English")
            except Exception as e:
                error_message = (f"Ошибка при отправке сообщения в чат {chat_id}: {e}")
                

        # Закрываем соединение с базой данных для чатов
        cursor_chats.close()
        connection_chats.close()
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении SQL-запроса для чатов: {e}")


def update_active_users():
    try:
        # Подключение к базе данных
        conn = connect_to_db('chat_data.db')
        cursor = conn.cursor()

        # Получаем список всех чатов
        cursor.execute("SELECT chat_id FROM chats")
        chat_ids = cursor.fetchall()

        for chat_id_tuple in chat_ids:
            chat_id = chat_id_tuple[0]

            # Получаем количество активных пользователей для выбранной группы
            cursor.execute("SELECT COUNT(*) FROM users WHERE chat_id=?", (chat_id,))
            active_users_count = cursor.fetchone()[0]

            # Записываем количество активных пользователей в поле active_users для данной группы
            cursor.execute("UPDATE chats SET active_users=? WHERE chat_id=?", (active_users_count, chat_id))

            # Получаем уровень создателя группы
            cursor.execute("SELECT creator_id, level_count FROM creators WHERE chat_id=?", (chat_id,))
            creator_info = cursor.fetchone()
            creator_id = creator_info[0]
            creator_level_count = creator_info[1]

            # Обновляем level_count в зависимости от количества активных пользователей
            if active_users_count >= 0 and active_users_count < 10:
                new_level_count = 0
            elif active_users_count >= 10 and active_users_count < 50:
                new_level_count = 1
            elif active_users_count >= 50 and active_users_count < 100:
                new_level_count = 2
            elif active_users_count >= 100 and active_users_count < 250:
                new_level_count = 3
            elif active_users_count >= 250 and active_users_count < 500:
                new_level_count = 4
            elif active_users_count >= 500 and active_users_count < 600:
                new_level_count = 5
            elif active_users_count >= 600 and active_users_count < 700:
                new_level_count = 6
            elif active_users_count >= 700 and active_users_count < 800:
                new_level_count = 7
            elif active_users_count >= 800 and active_users_count < 900:
                new_level_count = 8
            elif active_users_count >= 900 and active_users_count < 1000:
                new_level_count = 9
            else:
                new_level_count = 10

            # Если уровень создателя не равен новому уровню, обновляем level_count
            if creator_level_count != new_level_count:
                cursor.execute("UPDATE creators SET level_count=? WHERE chat_id=?", (new_level_count, chat_id))
                cursor.execute("UPDATE chats SET level_count=? WHERE chat_id=?", (new_level_count, chat_id))
                print(f"Уровень создателя группы {chat_id} обновлен с {creator_level_count} до {new_level_count}")

        # Применяем изменения и закрываем соединение с базой данных
        conn.commit()

    except sqlite3.Error as e:
        error_message = (f"Ошибка при обновлении активных пользователей {chat_id}: {e}")
        
    finally:
        # Закрываем соединение с базой данных
        if 'conn' in locals():
            conn.close()

# Функция для удаления старых сообщений из базы данных
def delete_old_messages():
    conn = connect_to_db('messages.db')
    cursor = conn.cursor()

    # Получаем текущее время минус одна минута
    one_minute_ago = datetime.now() - timedelta(minutes=1)

    # Выбираем все сообщения, которые старше одной минуты
    cursor.execute("SELECT * FROM last_messages WHERE timestamp < ?", (one_minute_ago,))
    old_messages = cursor.fetchall()

    # Удаляем найденные старые сообщения из базы данных
    for message in old_messages:
        chat_id, user_id, message_id = message[0], message[2], message[1]
        cursor.execute("DELETE FROM last_messages WHERE chat_id = ? AND user_id = ? AND message_id = ?", (chat_id, user_id, message_id))
        conn.commit()

    conn.close()


# Функция для запуска планировщика задач в отдельном потоке
def schedule_task():
    # Планируем рассылку рекламных сообщений и обновление пользователей
    schedule.every(1).seconds.do(check_expired_users)
    schedule.every(1).seconds.do(delete_old_messages)
    schedule.every().wednesday.at("18:00").do(send_advertisement)
    schedule.every().friday.at("12:00").do(send_advertisement_to_users)
    schedule.every().monday.at("12:00").do(send_advertisement_to_chats)
    schedule.every().sunday.at("16:30").do(get_ad_with_max_send_count)
    schedule.every(10).seconds.do(update_active_users)
    schedule.every(10).seconds.do(send_message_active_users)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Создаем и запускаем поток для выполнения планировщика задач
schedule_thread = threading.Thread(target=schedule_task)
schedule_thread.daemon = True  # Помечаем поток как демон, чтобы он завершился при завершении основного потока
schedule_thread.start()



# Функция для получения creator_id на основе chat_id из таблицы creators
def get_creator_id(chat_id):
    try:
        conn = connect_to_db('chat_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT creator_id, level_count FROM creators WHERE chat_id = ?", (chat_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result  # Возвращаем кортеж (creator_id, level_count) или None, если запись не найдена
    except sqlite3.OperationalError as e:
        print("Error:", e)
        return None



# Загрузка ключевых слов из базы данных
def load_good_keywords():
    conn = connect_to_db('good.db')
    c = conn.cursor()
    c.execute('SELECT keyword FROM keywords')
    keywords = [row[0] for row in c.fetchall()]
    conn.close()
    return keywords

# Загрузка ключевых слов из базы данных
def load_fuck_keywords():
    conn = connect_to_db('fuck.db')
    c = conn.cursor()
    c.execute('SELECT keyword FROM keywords')
    keywords = [row[0] for row in c.fetchall()]
    conn.close()
    return keywords

    
# Загрузка ключевых слов из базы данных
def load_spam_keywords():
    conn = connect_to_db('spam.db')
    c = conn.cursor()
    c.execute('SELECT keyword FROM keywords')
    keywords = [row[0] for row in c.fetchall()]
    conn.close()
    return keywords

# Добавление нового ключевого слова в базу данных
def add_spam_keyword(keyword_phrase):
    conn = connect_to_db('spam.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO keywords (keyword) VALUES (?)', (keyword_phrase,))
    conn.commit()
    conn.close()

# Функция для определения похожих на спам сообщений
def is_similar_to_spam(message_text, spam_keywords):
    # Проверяем наличие ключевых слов в тексте сообщения
    for keyword in spam_keywords:
        if keyword in message_text.lower():
            return True
    
    return False

# Функция для определения похожих на спам сообщений
def is_similar_to_gm(message_text, goodmorning_keywords):
    # Проверяем наличие ключевых слов в тексте сообщения
    for keyword in goodmorning_keywords:
        if keyword in message_text.lower():
            return True
    
    return False

# Функция для определения похожих на спам сообщений
def is_similar_to_fuck(message_text, fuck_keywords):
    # Проверяем наличие ключевых слов в тексте сообщения
    for keyword in fuck_keywords:
        if keyword in message_text.lower():
            return True
    
    return False

# Функция для определения похожих на спам сообщений
def is_similar_to_key(message_text, keywords):
    # Проверяем наличие ключевых слов в тексте сообщения
    for keyword in keywords:
        if keyword in message_text.lower():
            return True
    
    return False

def contains_links(message_text):
    # Шаблон для поиска ссылок в тексте
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    # Поиск ссылок в тексте
    urls = re.findall(url_pattern, message_text)
    # Возвращаем True, если найдены ссылки, иначе False
    return len(urls) > 0

def user_if_not_exists(cursor, chat_id, chat_name, user_id, user_username):
    # Проверяем существует ли пользователь уже в базе данных
    cursor.execute("SELECT 1 FROM users WHERE chat_id=? AND user_id=?", (chat_id, user_id))
    existing_user = cursor.fetchone()
    
    if not existing_user:
        # Если пользователь не существует, добавляем его
        cursor.execute('''INSERT INTO users 
                          (chat_id, chat_name, user_id, user_username, message_count, bonus_count, word_count, reactions_count, warn_count) 
                          VALUES (?, ?, ?, ?, 0, 0, 0, 0, 0)''', (chat_id, chat_name, user_id, user_username))


# Функция для получения языка пользователя из базы данных
def get_chat_language(chat_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM chats WHERE chat_id=?", (chat_id,))
    language = cursor.fetchone()
    conn.close()
    # Если язык не найден, устанавливаем значение по умолчанию 'rus'
    if language is None:
        return 'en'
    else:
        return language[0]

def update_total_warn_count(chat_id):
    try:
        # Подключаемся к базе данных SQLite
        connection = connect_to_db('chat_data.db')
        cursor = connection.cursor()

        # Получаем всех пользователей с заданным chat_id
        cursor.execute("SELECT user_id, warn_count FROM users WHERE chat_id=?", (chat_id,))
        users_data = cursor.fetchall()

        # Считаем общее количество предупреждений
        total_warn_count = sum(warn_count for _, warn_count in users_data)

        # Обновляем запись в таблице chats с общим количеством предупреждений
        cursor.execute("UPDATE chats SET warn_count=? WHERE chat_id=?", (total_warn_count, chat_id))
        connection.commit()

        print(f"Обновлено общее количество предупреждений для чата с chat_id={chat_id}: {total_warn_count}")
    except sqlite3.Error as e:
        print("Ошибка при работе с базой данных SQLite:", e)
    except Exception as e:
        print("Произошла ошибка:", e)

def notification(user_username, chat_id, user_id, chat_name, language, text, text1, text2, duration1, duration2, duration3):
    try:
        # Подключаемся к базе данных SQLite для подсчета кликов
        connection = connect_to_db('chat_data.db')
        cursor = connection.cursor()

        # Добавляем пользователя в базу данных, если его еще нет
        user_if_not_exists(cursor, chat_id, chat_name, user_id, user_username)

        # Получаем warn_count пользователя из базы данных
        cursor.execute("SELECT warn_count FROM users WHERE chat_id=? AND user_id=?", (chat_id, user_id))
        warn_count = cursor.fetchone()[0]
        kick = data['notification_text'][language]['kick']

        if warn_count == 0:
            duration = duration1
            warn_count += 1
            if duration == 5184:
                user_status = bot.get_chat_member(chat_id, user_id).status
                if user_status not in ('creator', 'administrator'):
                    if language == "rus":
                        bot.send_message(chat_id, f"@{user_username}, {text}\n\n{text2} <b>1</b>/3",parse_mode="HTML")
                    else:
                        bot.send_message(chat_id, f"@{user_username}, {text}\n\n{text2} <b>1</b>/3", parse_mode="HTML")
            elif duration == 5184000:
                user_status = bot.get_chat_member(chat_id, user_id).status
                if user_status not in ('creator', 'administrator'):
                    if language == "rus":
                        bot.send_message(chat_id, f"@{user_username}, {text}\n\n{kick}\n\n{text2} <b>1</b>/3",parse_mode="HTML")
                    else:
                        bot.send_message(chat_id, f"@{user_username}, {text}\n\n{kick}\n\n{text2} <b>1</b>/3", parse_mode="HTML")
                    bot.kick_chat_member(chat_id, user_id)
            else:
                new_duration = duration / 60 / 60
                if new_duration <= 24:
                    # Determine the appropriate time text based on the language and hour
                    if language == "rus":
                        if new_duration == 1 or new_duration == 21:
                            time_text = "час"
                        elif new_duration == 2 or new_duration == 3 or new_duration == 4 or new_duration == 22 or new_duration == 23 or new_duration == 24:
                            time_text = "часа"
                        else:
                            time_text = "часов"
                    else:  # English language
                        if new_duration == 1 or new_duration == 21:
                            time_text = "hour"
                        elif new_duration == 2 or new_duration == 3 or new_duration == 4 or new_duration == 22 or new_duration == 23 or new_duration == 24:
                            time_text = "hours"
                        else:
                            time_text = "hours"
                    user_status = bot.get_chat_member(chat_id, user_id).status
                    if user_status not in ('creator', 'administrator'):
                        bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + duration)
                        if language == "rus":
                            bot.send_message(chat_id, f"@{user_username}, {text}\n\n{text1} <b>{int(new_duration)}</b> {time_text}\n\n{text2} <b>1</b>/3",parse_mode="HTML")
                        else:
                            bot.send_message(chat_id, f"@{user_username}, {text}\n\n{text1} <b>{int(new_duration)}</b> {time_text}\n\n{text2} <b>1</b>/3", parse_mode="HTML")

        elif warn_count == 1:
            duration = duration2
            warn_count += 1
            if duration == 5184:
                user_status = bot.get_chat_member(chat_id, user_id).status
                if user_status not in ('creator', 'administrator'):
                    if language == "rus":
                        bot.send_message(chat_id, f"@{user_username}, {text}\n\n{text2} <b>2</b>/3",parse_mode="HTML")
                    else:
                        bot.send_message(chat_id, f"@{user_username}, {text}\n\n{text2} <b>2</b>/3", parse_mode="HTML")
            elif duration == 5184000:
                user_status = bot.get_chat_member(chat_id, user_id).status
                if user_status not in ('creator', 'administrator'):
                    if language == "rus":
                        bot.send_message(chat_id, f"@{user_username}, {text}\n\n{kick}\n\n{text2} <b>2</b>/3",parse_mode="HTML")
                    else:
                        bot.send_message(chat_id, f"@{user_username}, {text}\n\n{kick}\n\n{text2} <b>2</b>/3", parse_mode="HTML")
                    bot.kick_chat_member(chat_id, user_id)
            else:
                new_duration = duration / 60 / 60
                if new_duration <= 24:
                    # Determine the appropriate time text based on the language and hour
                    if language == "rus":
                        if new_duration == 1 or new_duration == 21:
                            time_text = "час"
                        elif new_duration == 2 or new_duration == 3 or new_duration == 4 or new_duration == 22 or new_duration == 23 or new_duration == 24:
                            time_text = "часа"
                        else:
                            time_text = "часов"
                    else:  # English language
                        if new_duration == 1 or new_duration == 21:
                            time_text = "hour"
                        elif new_duration == 2 or new_duration == 3 or new_duration == 4 or new_duration == 22 or new_duration == 23 or new_duration == 24:
                            time_text = "hours"
                        else:
                            time_text = "hours"
                    user_status = bot.get_chat_member(chat_id, user_id).status
                    if user_status not in ('creator', 'administrator'):
                        bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + duration)
                        if language == "rus":
                            bot.send_message(chat_id, f"@{user_username}, {text}\n\n{text1} <b>{int(new_duration)}</b> {time_text}\n\n{text2} <b>2</b>/3",parse_mode="HTML")
                        else:
                            bot.send_message(chat_id, f"@{user_username}, {text}\n\n{text1} <b>{int(new_duration)}</b> {time_text}\n\n{text2} <b>2</b>/3", parse_mode="HTML")


        elif warn_count == 2:
            duration = duration3
            warn_count += 1
            if duration == 5184:
                user_status = bot.get_chat_member(chat_id, user_id).status
                if user_status not in ('creator', 'administrator'):
                    if language == "rus":
                        bot.send_message(chat_id, f"@{user_username}, {text}\n\n{text2} <b>3</b>/3",parse_mode="HTML")
                    else:
                        bot.send_message(chat_id, f"@{user_username}, {text}\n\n{text2} <b>3</b>/3", parse_mode="HTML")
            elif duration == 5184000:
                user_status = bot.get_chat_member(chat_id, user_id).status
                if user_status not in ('creator', 'administrator'):
                    if language == "rus":
                        bot.send_message(chat_id, f"@{user_username}, {text}\n\n{kick}\n\n{text2} <b>3</b>/3",parse_mode="HTML")
                    else:
                        bot.send_message(chat_id, f"@{user_username}, {text}\n\n{kick}\n\n{text2} <b>3</b>/3", parse_mode="HTML")
                    bot.kick_chat_member(chat_id, user_id)
            else:
                new_duration = duration / 60 / 60
                if new_duration <= 24:
                    # Determine the appropriate time text based on the language and hour
                    if language == "rus":
                        if new_duration == 1 or new_duration == 21:
                            time_text = "час"
                        elif new_duration == 2 or new_duration == 3 or new_duration == 4 or new_duration == 22 or new_duration == 23 or new_duration == 24:
                            time_text = "часа"
                        else:
                            time_text = "часов"
                    else:  # English language
                        if new_duration == 1 or new_duration == 21:
                            time_text = "hour"
                        elif new_duration == 2 or new_duration == 3 or new_duration == 4 or new_duration == 22 or new_duration == 23 or new_duration == 24:
                            time_text = "hours"
                        else:
                            time_text = "hours"
                    user_status = bot.get_chat_member(chat_id, user_id).status
                    if user_status not in ('creator', 'administrator'):
                        bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + duration)
                        if language == "rus":
                            bot.send_message(chat_id, f"@{user_username}, {text}\n\n{text1} <b>{int(new_duration)}</b> {time_text}\n\n{text2} <b>3</b>/3",parse_mode="HTML")
                        else:
                            bot.send_message(chat_id, f"@{user_username}, {text}\n\n{text1} <b>{int(new_duration)}</b> {time_text}\n\n{text2} <b>3</b>/3", parse_mode="HTML")

        else:
            duration = duration3
            new_duration = duration / 60 / 60
            warn_count += 1
            if new_duration <= 24:
                # Determine the appropriate time text based on the language and hour
                if language == "rus":
                    if new_duration == 1 or new_duration == 21:
                        time_text = "час"
                    elif new_duration == 2 or new_duration == 3 or new_duration == 4 or new_duration == 22 or new_duration == 23 or new_duration == 24:
                        time_text = "часа"
                    else:
                        time_text = "часов"
                else:  # English language
                    if new_duration == 1 or new_duration == 21:
                        time_text = "hour"
                    elif new_duration == 2 or new_duration == 3 or new_duration == 4 or new_duration == 22 or new_duration == 23 or new_duration == 24:
                        time_text = "hours"
                    else:
                        time_text = "hours"
                user_status = bot.get_chat_member(chat_id, user_id).status
                if user_status not in ('creator', 'administrator'):
                    bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + duration)
                    if language == "rus":
                        bot.send_message(chat_id, f"@{user_username}, {text}\n\n{text1} <b>{int(new_duration)}</b> {time_text}", parse_mode="HTML")
                    else:
                        bot.send_message(chat_id, f"@{user_username}, {text}\n\n{text1} <b>{int(new_duration)}</b> {time_text}", parse_mode="HTML")

        # Обновляем warn_count в базе данных
        cursor.execute("UPDATE users SET warn_count=? WHERE chat_id=? AND user_id=?", (warn_count, chat_id, user_id))
        connection.commit()
        update_total_warn_count(chat_id)
    
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при выдачи предупреждения:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{user_username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)

    finally:
        # Закрываем соединение с базой данных
        if 'connection' in locals():
            connection.close()



# Функция для получения возможности заработка группы из базы данных
def get_group_earn(chat_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT earn FROM chats WHERE chat_id=?", (chat_id,))
    result = cursor.fetchone()
    conn.close()

    if result is not None:  # Проверяем, что результат не None
        if result[0] == 'on_earn':
            return 'on_earn'
        elif result[0] == 'off_earn':
            return 'off_earn'
    # Если ничего не найдено, вернуть значение по умолчанию, например, off_earn
    return 'off_earn'  # Или любое другое значение по умолчанию


def get_group_key(chat_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT key FROM chats WHERE chat_id=?", (chat_id,))
    key = cursor.fetchone()[0]
    conn.close()
    return key

def get_group_good_text(chat_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT good_text FROM chats WHERE chat_id=?", (chat_id,))
    good_text = cursor.fetchone()[0]
    conn.close()
    return good_text

def get_group_support(chat_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT support, spam, fuck, flood, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3, duration_flood1, duration_flood2, duration_flood3, link FROM chats WHERE chat_id=?", (chat_id,))
    support_data = cursor.fetchone()  # Получаем одну строку с данными
    conn.close()
    return support_data


def clean_message(message):
    # Удаляем HTML-теги и форматирование
    cleaned_message = re.sub(r'<[^>]*>', '', message)
    # Удаляем эмодзи
    cleaned_message = remove_emoji(cleaned_message)
    # Удаляем лишние пробелы и символы перевода строки
    cleaned_message = ' '.join(cleaned_message.split())
    return cleaned_message

def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def get_active_chat_recipient(chat_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT sender_id FROM active_chats WHERE recipient_id = ?''', (chat_id,))
    active_chat = cursor.fetchone()
    conn.close()
    
    return active_chat[0] if active_chat else None

def get_active_chat_sender(chat_id):
    conn = connect_to_db('active_chats.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT recipient_id FROM active_chats WHERE sender_id = ?''', (chat_id,))
    active_chat = cursor.fetchone()
    conn.close()
    
    return active_chat[0] if active_chat else None

# Создание базы данных и таблицы, если они не существуют
def create_spam_db():
    conn = connect_to_db('spam.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS keywords (
                    id INTEGER PRIMARY KEY,
                    keyword TEXT UNIQUE
                )''')
    conn.commit()
    conn.close()

# Функция для сохранения идентификатора сообщения в базу данных
def save_message(chat_id, message_id):
    # Передаем функцию _save_message в пул потоков для выполнения
    executor.submit(_save_message, chat_id, message_id)

# Функция для фактического сохранения идентификатора сообщения в базу данных
def _save_message(chat_id, message_id):
    # Создаем новое соединение с базой данных
    with connect_to_db("messages.db") as conn:
        # Создаем курсор для выполнения запросов
        cursor = conn.cursor()
        # Выполняем SQL-запрос для вставки идентификатора сообщения
        cursor.execute("INSERT INTO messages (chat_id, message_id) VALUES (?, ?)", (chat_id, message_id))
        # Фиксируем изменения в базе данных
        conn.commit()

# Функция для получения языка пользователя из базы данных
def get_user_mod(chat_id, user_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT chat_name, user_username FROM users WHERE user_id=? AND chat_id=?", (user_id, chat_id))
    user_mod = cursor.fetchone()
    conn.close()
    return user_mod

def send_mod_notification(chat_id, user_id, duration_flood1, duration_flood2, duration_flood3):
    user_mod = get_user_mod(chat_id, user_id)
    chat_name, user_username = user_mod
    try:

        language = get_chat_language(chat_id)
        text = data['notification_text'][language]['flood']
        text1 = data['notification_text'][language]['mute']
        text2 = data['notification_text'][language]['delete']
        connection = connect_to_db('chat_data.db')
        cursor = connection.cursor()
        # Добавляем пользователя в базу данных, если его еще нет
        user_if_not_exists(cursor, chat_id, chat_name, user_id, user_username)

        duration = 3600  # Значение по умолчанию - 1 час
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status not in ('creator', 'administrator'):
            bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + duration)
        notification(user_username, chat_id, user_id, chat_name, language, text, text1, text2, duration_flood1, duration_flood2, duration_flood3)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при выдачи предупреждения за матерные слова:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• User ID: {chat_id}\n"
            f"• Username: @{user_username}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        

    finally:
        # Закрываем соединение с базой данных
        if 'connection' in locals():
            connection.close()


# Функция для сохранения сообщения в базе данных
def mod_message_more(chat_id, message_id, user_id, message_text, duration_flood1, duration_flood2, duration_flood3):
    executor.submit(_mod_message_more, chat_id, message_id, user_id, message_text, duration_flood1, duration_flood2, duration_flood3)

def _mod_message_more(chat_id, message_id, user_id, message_text, duration_flood1, duration_flood2, duration_flood3):
    conn = connect_to_db('messages.db')
    cursor = conn.cursor()

    print("Starting mod_message_more function")

    # Check for duplicate messages within the last minute
    one_minute_ago = datetime.now() - timedelta(minutes=1)
    cursor.execute("SELECT * FROM last_messages WHERE chat_id = ? AND user_id = ? AND message_text = ? AND timestamp > ?", (chat_id, user_id, message_text, one_minute_ago))
    duplicate_messages = cursor.fetchall()
    print("Duplicate messages found:", duplicate_messages)
    user_status = bot.get_chat_member(chat_id, user_id).status
    print("User status:", user_status)
    duration = 3600  # Значение по умолчанию - 1 час

    # If duplicate messages found
    if len(duplicate_messages) > 1:
        print("Duplicate messages count:", len(duplicate_messages))

        # Get duplicate message IDs, excluding the original message ID
        duplicate_message_ids = [msg[1] for msg in duplicate_messages[1:]]
        print("Duplicate message IDs:", duplicate_message_ids)

        # Delete duplicate messages from chat
        for message_id_to_delete in duplicate_message_ids:
            cursor.execute("UPDATE last_messages SET count = count + 1 WHERE chat_id = ? AND user_id = ? AND message_text = ?", (chat_id, user_id, message_text))
            cursor.execute("SELECT count FROM last_messages WHERE chat_id = ? AND user_id = ? AND message_text = ?", (chat_id, user_id, message_text))
            count_count = cursor.fetchone()[0]  # Fetch count from the fetched row
            print("Count count:", count_count)
            # If more than 3 duplicates were deleted
        # Если более 3 дубликата сообщений были удалены
        if int(count_count) > 2:
            print("More than 3 duplicates found")

            if user_status not in ('creator', 'administrator'):
                print("User is not a creator or administrator")

                # Наложение ограничения на пользователя
                bot.delete_message(chat_id, message_id_to_delete)
                bot.restrict_chat_member(chat_id, user_id, until_date=time.time() + duration)
                print("Restriction imposed on user")

                time.sleep(1)
                cursor.execute("DELETE FROM last_messages WHERE chat_id = ? AND user_id = ?", (chat_id, user_id))
                print("Duplicate messages deleted from database")

                send_mod_notification(chat_id, user_id, duration_flood1, duration_flood2, duration_flood3)
                print("Notification sent to moderators")

    conn.commit()
    conn.close()

# Функция для сохранения сообщения в базе данных
def save_last_message(chat_id, message_id, user_id, message_text):
    executor.submit(_save_last_message, chat_id, message_id, user_id, message_text)

def _save_last_message(chat_id, message_id, user_id, message_text):
    conn = connect_to_db('messages.db')
    cursor = conn.cursor()
    
    # Создание таблицы, если она еще не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS last_messages
                      (chat_id INTEGER, message_id INTEGER, user_id INTEGER, message_text TEXT, timestamp, count TEXT)''')
    
    # Вставка нового сообщения в таблицу
    cursor.execute("INSERT INTO last_messages (chat_id, message_id, user_id, message_text, timestamp, count) VALUES (?, ?, ?, ?, ?, 0)", (chat_id, message_id, user_id, message_text, datetime.now()))
    
    conn.commit()
    conn.close()

def update_chat_data(chat_id, chat_name, user_id, user_username):
    try:
        connection = connect_to_db('chat_data.db')
        cursor = connection.cursor()

        # Проверяем, изменилось ли имя чата
        cursor.execute("SELECT chat_name FROM chats WHERE chat_id=?", (chat_id,))
        old_chat_name = cursor.fetchone()[0]

        if old_chat_name != chat_name:
            # Обновляем имя чата в таблице chats
            cursor.execute("UPDATE chats SET chat_name=? WHERE chat_id=?", (chat_name, chat_id))

            # Обновляем имя чата в таблице users
            cursor.execute("UPDATE users SET chat_name=? WHERE chat_id=?", (chat_name, chat_id))

        # Проверяем, изменился ли username пользователя
        cursor.execute("SELECT user_username FROM users WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        if result is not None:
            old_user_username = result[0]
            if old_user_username != user_username:
                # Обновляем username пользователя в таблице users
                cursor.execute("UPDATE users SET user_username=? WHERE user_id=?", (user_username, user_id))
                connection.commit()
        else:
            print("Пользователь с ID", user_id, "не найден в базе данных.")


    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обновлении данных чата и пользователя:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• Chat ID: {chat_id}\n"
            f"• User ID: {user_id}\n"
            f"• Время: {datetime.now()}"
        )

        # Записываем сообщение об ошибке в журнал
        logging.error(error_message)

    finally:
        # Закрываем соединение с базой данных
        if 'connection' in locals():
            connection.close()


@bot.message_handler(content_types=['text'])
def handle_group_message(message):
    if message.chat.type == "private":  # Проверка, является ли чат приватным
        chat_id = message.from_user.id
        sender_id = get_active_chat_sender(chat_id)
        recipient_id = get_active_chat_recipient(chat_id)
        user_language = get_user_language(chat_id)
        # Если чат приватный и сообщение содержит знак вопроса, отправляем сообщение пользователю и завершаем выполнение функции
        if '?' in message.text:
            if user_language == "en":
                bot.send_message(message.chat.id, "Hi! 😊 If you need help, contact technical support. Just click on the button\"🛠 Support\" and we'll get back to you. 🚀\n\nWe are here to help you solve any problems or answer your questions. 👨‍💻")
            else:
                if sender_id:
                    bot.send_message(sender_id, message.text)
                elif recipient_id:
                    bot.send_message(recipient_id, message.text)
                else:
                    bot.send_message(message.chat.id, "Привет! 😊 Если тебе нужна помощь, обратись в техническую поддержку. Просто нажмите на кнопку \"🛠 Помощь\" и мы с тобой свяжемся. 🚀\n\nМы готовы помочь вам решить любые проблемы или ответить на ваши вопросы. 👨‍💻")
            return
        else:
            # Если в сообщении нет знака вопроса, ничего не делаем и завершаем выполнение функции
            return

    chat_id = message.chat.id
    chat_name = message.chat.title
    user_id = message.from_user.id
    user_username = message.from_user.username
    user_status = bot.get_chat_member(chat_id, user_id).status
    update_chat_data(chat_id, chat_name, user_id, user_username)
    message_text = clean_message(message.text)  # Очистить текст сообщения
    current_earn = get_group_earn(chat_id)
    current_good_text = get_group_good_text(chat_id)
    key = get_group_key(chat_id)
    if key == "non":
        pass
    else:
        words_list = [word.strip() for word in key.split(',')]
        if is_similar_to_key(message_text, words_list):
            bot.delete_message(chat_id, message.message_id)

    support_data = get_group_support(chat_id)
    support = support_data[0]  # Значение support
    spam = support_data[1]  # Значение spam
    fuck = support_data[2]  # Значение fuck
    flood = support_data[3]  # Значение flood
    duration_spam1 = support_data[4] 
    duration_spam2 = support_data[5] 
    duration_spam3 = support_data[6] 
    duration_fuck1 = support_data[7] 
    duration_fuck2 = support_data[8] 
    duration_fuck3 = support_data[9] 
    duration_flood1 = support_data[10] 
    duration_flood2 = support_data[11] 
    duration_flood3 = support_data[12]
    link = support_data[13]
    if flood == "on":
        save_last_message(chat_id, message.message_id, user_id, message_text)
        mod_message_more(chat_id, message.message_id, user_id, message_text, duration_flood1, duration_flood2, duration_flood3)
    else:
        pass

    save_message(chat_id, message.message_id)  # Сохранение идентификатора сообщения чата
    print(f"Received message: {message_text} from user {user_username} in chat {chat_name}")
            
    create_spam_db()
    spam_keywords = load_spam_keywords()
    goodmorning_keywords = load_good_keywords()
    fuck_keywords = load_fuck_keywords()
    language = get_chat_language(chat_id) 
    try:
        if message.chat.type != "private":
            # Параметры сообщения
            if support == "off":
                if is_similar_to_spam(message_text, spam_keywords):
                    if spam == "on":
                        bot.delete_message(chat_id, message.message_id)
                        spam1 = data['notification_text'][language]['spam']
                        spam2 = data['notification_text'][language]['mute']
                        spam3 = data['notification_text'][language]['delete']
                        notification(user_username, chat_id, user_id, chat_name, language, spam1, spam2, spam3, duration_spam1, duration_spam2, duration_spam3)
                    else:
                        pass

                # Проверяем, похоже ли сообщение на доброе утро
                elif is_similar_to_gm(message_text, goodmorning_keywords):
                    # Отправляем сообщение пользователю 2031010965
                    if current_good_text == "good_off":
                        bot.delete_message(chat_id, message.message_id)
                    else:
                        pass
                # Проверяем, похоже ли сообщение на ругательство
                elif contains_links(message_text):
                    if link == "on":
                        if user_status not in ('creator', 'administrator'):
                            bot.delete_message(message.chat.id, message.message_id)
                        else:
                            pass
                    else:
                        pass
                elif is_similar_to_fuck(message_text, fuck_keywords):
                    # Если чат имеет идентификатор -1001693817908
                    if fuck == "on":
                        bot.delete_message(message.chat.id, message.message_id)
                        fuck1 = data['notification_text'][language]['fuck']
                        fuck2 = data['notification_text'][language]['mute']
                        fuck3 = data['notification_text'][language]['delete']
                        notification(user_username, chat_id, user_id, chat_name, language, fuck1, fuck2, fuck3, duration_fuck1, duration_fuck2, duration_fuck3)
                    else:
                        pass
                        
                # Получаем creator_id и level_count для данного чата
                creator_info = get_creator_id(chat_id)

                # Проверяем, если creator_info не равен None
                if creator_info:
                    creator_id, level_count = creator_info
                else:
                    # Если creator_info равен None, то присваиваем creator_id и level_count значение None
                    creator_id, level_count = None, None

                # Проверяем тип чата
                if current_earn == "on_earn":
                    if current_good_text == "good_on":
                        process_group_message(chat_id, chat_name, user_id, creator_id, level_count, user_username, message_text)  # Передача очищенного сообщения
                    else:
                        process_group_message_nogrand(chat_id, chat_name, user_id, user_username, message_text)  # Передача очищенного сообщения
                else:
                    process_group_message_nogrand(chat_id, chat_name, user_id, user_username, message_text)  # Передача очищенного сообщения
            else:
                pass

        else:
            pass
    
    except Exception as e:
        # В этом месте используем message_text
        error_message = (
            f"⚠️ Произошла ошибка при обработки сообщения в чате:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• Chat ID: {message.chat.id}\n"
            f"• Chat name: {message.chat.title}\n"
            f"• User ID: {message.from_user.id}\n"
            f"• Username: @{message.from_user.username}\n"
            f"• Сообщение: {message_text}\n"
            f"• Время: {datetime.now()}"
        )

        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)


# Функция для получения grand_count пользователя из базы данных по chat_id
def get_admin_grand_count(chat_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT grand_count FROM chats WHERE chat_id = ?", (chat_id,))
    grand_count = cursor.fetchone()
    conn.close()
    # Если grand_count не найден, устанавливаем значение по умолчанию '1'
    if grand_count is None:
        return '1'
    else:
        return grand_count[0]

# Функция для получения языка пользователя из базы данных
def get_warn_count(chat_id, user_id):
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT warn_count FROM users WHERE chat_id=? AND user_id=?", (chat_id, user_id))
    warn_count = cursor.fetchone()
    conn.close()
    # Если язык не найден, устанавливаем значение по умолчанию 'rus'
    if warn_count is None:
        return '0'
    else:
        return warn_count[0]


def create_users_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (chat_id INTEGER, 
                      chat_name TEXT, 
                      user_id INTEGER, 
                      user_username TEXT, 
                      message_count INTEGER, 
                      bonus_count INTEGER, 
                      word_count INTEGER, 
                      reactions_count INTEGER,
                      warn_count INTEGER,
                      PRIMARY KEY (chat_id, user_id))''')

def add_user_if_not_exists(cursor, chat_id, chat_name, user_id, user_username):
    cursor.execute('''INSERT OR IGNORE INTO users 
                      (chat_id, chat_name, user_id, user_username, message_count, bonus_count, word_count, reactions_count, warn_count) 
                      VALUES (?, ?, ?, ?, 0, 0, 0, 0, 0)''', (chat_id, chat_name, user_id, user_username))


def update_user_info_nogrand(cursor, chat_id, user_id, words_count):
    try:
        cursor.execute('''UPDATE users 
                          SET message_count = message_count + 1,
                              word_count = word_count + ?
                          WHERE chat_id = ? AND user_id = ?''', (words_count, chat_id, user_id))
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обновлении статистики пользователю без бонуса:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Chat name: {chat_id.chat.title}\n"
            f"• User ID: {user_id}\n"
            f"• Username: @{user_id.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )
        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        
        pass  # Пропустить обновление информации для этого пользователя

def update_user_info(cursor, chat_id, user_id, words_count, level_count):
    warn_count = get_warn_count(chat_id, user_id)
    grand_count = get_admin_grand_count(chat_id)
    if level_count == 0:
        bonus_coefficient = 0
    else:
        if warn_count == 0:
            bonus_coefficient = float(grand_count) * 1
        elif warn_count == 1:
            bonus_coefficient = (float(grand_count) * 0.5) * 1
        elif warn_count == 2:
            bonus_coefficient = (float(grand_count) * 0.25) * 1
        else:
            bonus_coefficient = (float(grand_count) * 0.1) * 1
    try:
        cursor.execute('''UPDATE users 
                          SET message_count = message_count + 1,
                              word_count = word_count + ?,
                              bonus_count = bonus_count + ?
                          WHERE chat_id = ? AND user_id = ?''', (words_count, words_count * bonus_coefficient, chat_id, user_id))
        
        print(f"Пополнение {chat_id}. Bonus: {grand_count}")
        
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обновлении статистики пользователю:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Chat name: {chat_id.chat.title}\n"
            f"• User ID: {user_id}\n"
            f"• Username: @{user_id.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )
        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        
        pass  # Пропустить обновление информации для этого пользователя


def update_creator_bonus(cursor, chat_id, creator_id, words_count, user_id, level_count):
    grand_count = get_admin_grand_count(chat_id)
    warn_count = get_warn_count(chat_id, user_id)
    if user_id != creator_id:
        if level_count <= 10:
            if warn_count == 0:
                bonus_coefficient = float(grand_count) * level_count * 0.01
            elif warn_count == 1:
                bonus_coefficient = (float(grand_count) * 0.5) * level_count * 0.01
            elif warn_count == 2:
                bonus_coefficient = (float(grand_count) * 2.5) * level_count * 0.01
            else:
                bonus_coefficient = (float(grand_count) * 0.1) * level_count * 0.01
        else:
            bonus_coefficient = 0.1
    else:
        bonus_coefficient = 0
    
    try:
        cursor.execute('''UPDATE creators 
                          SET bonus_count = bonus_count + ?
                          WHERE creator_id = ? AND chat_id = ?''', (words_count * bonus_coefficient, creator_id, chat_id))
        print(f"Пополнение создателя {chat_id}. Bonus coefficient: {bonus_coefficient}, {grand_count}")
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обновлении статистики создателя:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Chat name: {chat_id.chat.title}\n"
            f"• Creator ID: {creator_id}\n"
            f"• Username: @{creator_id.from_user.username}\n"
            f"• Время: {datetime.now()}"
        )
        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        
        pass  # Пропустить обновление бонуса для этого создателя



def update_chat_info_nogrand(cursor, chat_id, words_count):
    try:
        cursor.execute('''UPDATE chats 
                          SET message_count = message_count + 1,
                              word_count = word_count + ?
                          WHERE chat_id = ?''', (words_count, chat_id))
        
        print(f"Пополнение {chat_id}. Слов: {words_count}")
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обновлении статистики чата без бонуса:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Chat name: {chat_id.chat.title}\n"
            f"• Время: {datetime.now()}"
        )
        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        
        pass  # Пропустить обновление информации для этого чата

def update_chat_info(cursor, chat_id, words_count, user_id, level_count):
    warn_count = get_warn_count(chat_id, user_id)
    grand_count = get_admin_grand_count(chat_id)
    creator_info = get_creator_id(chat_id)
    if creator_info:
        creator_id, level_count = creator_info
    else:
        creator_id, level_count = None, 0  # Установите уровень по умолчанию

    try:
        if user_id == creator_id:
            user_role = "creator"
            if level_count == 0:
                bonus_coefficient = 0
            else:
                if warn_count == 0:
                    bonus_coefficient = float(grand_count) * 1
                elif warn_count == 1:
                    bonus_coefficient = (float(grand_count) * 0.5) * 1
                elif warn_count == 2:
                    bonus_coefficient = (float(grand_count) * 0.25) * 1
                else:
                    bonus_coefficient = (float(grand_count) * 0.1) * 1
        else:
            user_role = "user"
            if level_count == 0:
                bonus_coefficient = 0
            elif level_count == 1:
                if warn_count == 0:
                    bonus_coefficient = float(grand_count) + (float(grand_count) * 0.01)
                elif warn_count == 1:
                    bonus_coefficient = (float(grand_count) * 0.5) + (float(grand_count) * 0.5 * 0.01)
                elif warn_count == 2:
                    bonus_coefficient = (float(grand_count) * 0.25) + (float(grand_count) * 0.25 * 0.01)
                else:
                    bonus_coefficient = (float(grand_count) * 0.1) + (float(grand_count) * 0.1 * 0.01)
            elif level_count == 2:
                if warn_count == 0:
                    bonus_coefficient = float(grand_count) + (float(grand_count) * 0.02)
                elif warn_count == 1:
                    bonus_coefficient = (float(grand_count) * 0.5) + (float(grand_count) * 0.5 * 0.02)
                elif warn_count == 2:
                    bonus_coefficient = (float(grand_count) * 0.25) + (float(grand_count) * 0.25 * 0.02)
                else:
                    bonus_coefficient = (float(grand_count) * 0.1) + (float(grand_count) * 0.1 * 0.02)
            elif level_count == 3:
                if warn_count == 0:
                    bonus_coefficient = float(grand_count) + (float(grand_count) * 0.03)
                elif warn_count == 1:
                    bonus_coefficient = (float(grand_count) * 0.5) + (float(grand_count) * 0.5 * 0.03)
                elif warn_count == 2:
                    bonus_coefficient = (float(grand_count) * 0.25) + (float(grand_count) * 0.25 * 0.03)
                else:
                    bonus_coefficient = (float(grand_count) * 0.1) + (float(grand_count) * 0.1 * 0.03)
            elif level_count == 4:
                if warn_count == 0:
                    bonus_coefficient = float(grand_count) + (float(grand_count) * 0.04)
                elif warn_count == 1:
                    bonus_coefficient = (float(grand_count) * 0.5) + (float(grand_count) * 0.5 * 0.04)
                elif warn_count == 2:
                    bonus_coefficient = (float(grand_count) * 0.25) + (float(grand_count) * 0.25 * 0.04)
                else:
                    bonus_coefficient = (float(grand_count) * 0.1) + (float(grand_count) * 0.1 * 0.04)
            elif level_count == 5:
                if warn_count == 0:
                    bonus_coefficient = float(grand_count) + (float(grand_count) * 0.05)
                elif warn_count == 1:
                    bonus_coefficient = (float(grand_count) * 0.5) + (float(grand_count) * 0.5 * 0.05)
                elif warn_count == 2:
                    bonus_coefficient = (float(grand_count) * 0.25) + (float(grand_count) * 0.25 * 0.05)
                else:
                    bonus_coefficient = (float(grand_count) * 0.1) + (float(grand_count) * 0.1 * 0.05)
            elif level_count == 6:
                if warn_count == 0:
                    bonus_coefficient = float(grand_count) + (float(grand_count) * 0.06)
                elif warn_count == 1:
                    bonus_coefficient = (float(grand_count) * 0.5) + (float(grand_count) * 0.5 * 0.06)
                elif warn_count == 2:
                    bonus_coefficient = (float(grand_count) * 0.25) + (float(grand_count) * 0.25 * 0.06)
                else:
                    bonus_coefficient = (float(grand_count) * 0.1) + (float(grand_count) * 0.1 * 0.06)
            elif level_count == 7:
                if warn_count == 0:
                    bonus_coefficient = float(grand_count) + (float(grand_count) * 0.07)
                elif warn_count == 1:
                    bonus_coefficient = (float(grand_count) * 0.5) + (float(grand_count) * 0.5 * 0.07)
                elif warn_count == 2:
                    bonus_coefficient = (float(grand_count) * 0.25) + (float(grand_count) * 0.25 * 0.07)
                else:
                    bonus_coefficient = (float(grand_count) * 0.1) + (float(grand_count) * 0.1 * 0.07)
            elif level_count == 8:
                if warn_count == 0:
                    bonus_coefficient = float(grand_count) + (float(grand_count) * 0.08)
                elif warn_count == 1:
                    bonus_coefficient = (float(grand_count) * 0.5) + (float(grand_count) * 0.5 * 0.08)
                elif warn_count == 2:
                    bonus_coefficient = (float(grand_count) * 0.25) + (float(grand_count) * 0.25 * 0.08)
                else:
                    bonus_coefficient = (float(grand_count) * 0.1) + (float(grand_count) * 0.1 * 0.08)
            elif level_count == 9:
                if warn_count == 0:
                    bonus_coefficient = float(grand_count) + (float(grand_count) * 0.09)
                elif warn_count == 1:
                    bonus_coefficient = (float(grand_count) * 0.5) + (float(grand_count) * 0.5 * 0.09)
                elif warn_count == 2:
                    bonus_coefficient = (float(grand_count) * 0.25) + (float(grand_count) * 0.25 * 0.09)
                else:
                    bonus_coefficient = (float(grand_count) * 0.1) + (float(grand_count) * 0.1 * 0.09)
            elif level_count == 10:
                if warn_count == 0:
                    bonus_coefficient = float(grand_count) + (float(grand_count) * 0.1)
                elif warn_count == 1:
                    bonus_coefficient = (float(grand_count) * 0.5) + (float(grand_count) * 0.5 * 0.1)
                elif warn_count == 2:
                    bonus_coefficient = (float(grand_count) * 0.25) + (float(grand_count) * 0.25 * 0.1)
                else:
                    bonus_coefficient = (float(grand_count) * 0.1) + (float(grand_count) * 0.1 * 0.1)
            else:
                if warn_count == 0:
                    bonus_coefficient = float(grand_count) + (float(grand_count) * 0.1)
                elif warn_count == 1:
                    bonus_coefficient = (float(grand_count) * 0.5) + (float(grand_count) * 0.5 * 0.1)
                elif warn_count == 2:
                    bonus_coefficient = (float(grand_count) * 0.25) + (float(grand_count) * 0.25 * 0.1)
                else:
                    bonus_coefficient = (float(grand_count) * 0.1) + (float(grand_count) * 0.1 * 0.1)

        cursor.execute('''UPDATE chats 
                          SET message_count = message_count + 1,
                              word_count = word_count + ?,
                              bonus_count = bonus_count + ?
                          WHERE chat_id = ?''', (words_count, words_count * bonus_coefficient, chat_id))
        
        print(f"Пополнение {chat_id}. Слов: {words_count}, Написал: {user_role}, Бонус коэф: {bonus_coefficient}, {grand_count}")
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при обновлении статистики чата:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• Chat ID: {chat_id}\n"
            f"• User ID: {user_id}\n"
            f"• Username: {user_id.from_user.username}\n"
            f"• Chat name: {chat_id.chat.title}\n"
            f"• Время: {datetime.now()}"
        )
        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        
        pass  # Пропустить обновление информации для этого чата


def process_group_message_nogrand(chat_id, chat_name, user_id, user_username, message_text):
    conn = None
    cursor = None
    
    try:
        # Подключение к базе данных
        conn = connect_to_db('chat_data.db')
        cursor = conn.cursor()
        # Создание таблицы пользователей, если ее нет
        create_users_table(cursor)

        # Добавление пользователя, если его нет
        add_user_if_not_exists(cursor, chat_id, chat_name, user_id, user_username)

        # Разбиваем сообщение на слова
        words = message_text.split()

        # Получение количества слов в сообщении
        words_count = len(words)



        # Обновление информации о пользователе
        update_user_info_nogrand(cursor, chat_id, user_id, words_count)

        # Обновление информации о чате
        update_chat_info_nogrand(cursor, chat_id, words_count)

        # Применяем изменения
        conn.commit()


    except sqlite3.OperationalError as e:
        print("Произошла ошибка:", e)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при выполнение функции по обновлению статистики без бонуса:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Chat name: {chat_name}\n"
            f"• User ID: {user_id}\n"
            f"• Username: @{user_username}\n"
            f"• Message: {message_text}\n"
            f"• Время: {datetime.now()}"
        )
        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        

    finally:
        # Закрываем курсор и соединение с базой данных
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def process_group_message(chat_id, chat_name, user_id, creator_id, level_count, user_username, message_text):
    conn = None
    cursor = None
    
    try:
        # Подключение к базе данных
        conn = connect_to_db('chat_data.db')
        cursor = conn.cursor()

        # Создание таблицы пользователей, если ее нет
        create_users_table(cursor)

        # Добавление пользователя, если его нет
        add_user_if_not_exists(cursor, chat_id, chat_name, user_id, user_username)

        # Разбиваем сообщение на слова
        words = message_text.split()

        # Получение количества слов в сообщении
        words_count = len(words)

        # Обновление информации о пользователе
        update_user_info(cursor, chat_id, user_id, words_count, level_count)

        # Добавление бонусов создателю чата
        update_creator_bonus(cursor, chat_id, creator_id, words_count, user_id, level_count)

        # Обновление информации о чате
        update_chat_info(cursor, chat_id, words_count, user_id, level_count)

        # Применяем изменения
        conn.commit()


    except sqlite3.OperationalError as e:
        print("Произошла ошибка:", e)

    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при выполнение функции по обновлению статистики:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Chat name: {chat_name}\n"
            f"• User ID: {user_id}\n"
            f"• Username: @{user_username}\n"
            f"• Creator ID: {creator_id}\n"
            f"• Message: {message_text}\n"
            f"• Время: {datetime.now()}"
        )
        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        

    finally:
        # Закрываем курсор и соединение с базой данных
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Функция для создания подключения к базе данных SQLite и создания таблиц, если их еще нет
def create_connection():
    conn = connect_to_db('chat_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS chats
                   (chat_id INTEGER PRIMARY KEY, 
                   chat_name TEXT, 
                   creator_id INTEGER, 
                   creator_username TEXT, 
                   language TEXT, 
                   active_users INTEGER, 
                   message_count INTEGER, 
                   bonus_count INTEGER, 
                   word_count INTEGER, 
                   reactions_count INTEGER,
                   warn_count INTEGER, 
                   level_count INTEGER, 
                   sent_messages INTEGER, 
                   earn TEXT,  
                   hi_text TEXT, 
                   good_text TEXT,  
                   grand_count INTEGER, 
                   support TEXT,
                   spam TEXT,
                   fuck TEXT,
                   flood TEXT,
                   duration_spam1 INTEGER,
                   duration_spam2 INTEGER,
                   duration_spam3 INTEGER,
                   duration_fuck1 INTEGER,
                   duration_fuck2 INTEGER,
                   duration_fuck3 INTEGER,
                   duration_flood1 INTEGER,
                   duration_flood2 INTEGER,
                   duration_flood3 INTEGER,
                   link TEXT,
                   key TEXT,
                   prefix TEXT 
                   )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS active_chats
                      (chat_id INTEGER PRIMARY KEY)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS creators
                   (creator_id INTEGER, 
                   creator_username TEXT,chat_id INTEGER PRIMARY KEY, 
                   chat_name TEXT, language TEXT, message_count INTEGER, 
                   bonus_count INTEGER, word_count INTEGER,  
                   reactions_count INTEGER,
                   warn_count INTEGER, level_count INTEGER)''')
    return conn, cursor

# Функция для закрытия подключения к базе данных SQLite
def close_connection(conn):
    conn.commit()
    conn.close()

def add_chat_to_db(cursor, conn, chat_id, chat_name, creator_id, creator_username, language, hi_text, earn, good_text, support, spam, fuck, flood, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3, duration_flood1, duration_flood2, duration_flood3, link, key, prefix):
    # Проверка наличия всех необходимых значений и их корректности
    if not all((chat_id, chat_name, creator_id, creator_username, language, hi_text)):
        logging.error("Не все необходимые данные переданы для добавления чата в базу данных или они некорректны")
        return False

    try:
        cursor.execute("INSERT INTO chats VALUES (?, ?, ?, ?, ?, 0, 0, 0, 0, 0, 0, 0, 0, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (chat_id, chat_name, creator_id, creator_username, language, earn, hi_text, good_text, support, spam, fuck, flood, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3, duration_flood1, duration_flood2, duration_flood3, link, key, prefix))
        conn.commit()
        return True
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при записи данных чата:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Chat name: {chat_name}\n"
            f"• Creator ID: {creator_id}\n"
            f"• Creatorname: @{creator_username}\n"
            f"• Время: {datetime.now()}"
        )
        logging.error(error_message)
        
        return False


def add_active_chat_to_db(cursor, conn, chat_id):
    # Проверка наличия всех необходимых значений и их корректности
    if not chat_id:
        logging.error("Не все необходимые данные переданы для добавления активного чата в базу данных или они некорректны")
        return False

    try:
        cursor.execute("INSERT INTO active_chats VALUES (?)", (chat_id,))
        conn.commit()
        return True
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при Добавлении активного чата в базу данных:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Время: {datetime.now()}"
        )
        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        
        return False


# Функция для добавления нового создателя в базу данных
def add_creator_to_db(cursor, conn, creator_id, creator_username, chat_id, chat_name, language):
    # Проверка наличия всех необходимых значений и их корректности
    if not all((creator_id, creator_username, chat_id, chat_name, language)):
        logging.error("Не все необходимые данные переданы для добавления создателя в базу данных или они некорректны")
        return False

    try:
        cursor.execute("INSERT INTO creators VALUES (?, ?, ?, ?, ?, 0, 0, 0, 0, 0, 0)", (creator_id, creator_username, chat_id, chat_name, language))
        conn.commit()
        return True
    except Exception as e:
        error_message = (
            f"⚠️ Произошла ошибка при Добавлении создателя в базу данных:\n"
            f"• Тип ошибки: {e.__class__.__name__}\n"
            f"• Описание: {e}\n"
            f"• Строка: {e.__traceback__.tb_lineno}\n"
            f"• Creator ID: {creator_id}\n"
            f"• Creatorname: @{creator_username}\n"
            f"• Chat ID: {chat_id}\n"
            f"• Chat name: {chat_name}\n"
            f"• Language: {language}\n"
            f"• Время: {datetime.now()}"
        )
        # Используйте библиотеку logging для записи сообщения об ошибке
        logging.error(error_message)
        
        return False


# Функция для получения языка создателя по его идентификатору
def get_creator_language(creator_id):
    # Подключение к базе данных database.db
    conn_db = connect_to_db('database.db')
    cursor_db = conn_db.cursor()
    
    cursor_db.execute("SELECT language FROM users WHERE user_id=?", (creator_id,))
    creator_language = cursor_db.fetchone()
    
    # Закрываем подключение к базе данных
    cursor_db.close()
    conn_db.close()
    
    return creator_language[0] if creator_language else None

def get_creator_prefix(creator_id):
    # Подключение к базе данных database.db
    conn_db = connect_to_db('database.db')
    cursor_db = conn_db.cursor()
    
    cursor_db.execute("SELECT prefix FROM users WHERE user_id=?", (creator_id,))
    creator_prefix = cursor_db.fetchone()
    
    # Закрываем подключение к базе данных
    cursor_db.close()
    conn_db.close()
    
    return creator_prefix[0] if creator_prefix else None

# Функция для получения приветственного текста на основе языка создателя
def get_hi_text(creator_id):
    creator_language = get_creator_language(creator_id)
    if creator_language == "en":
        return "Welcome! Be active and earn GRAND bonus!"
    else:
        return "добро пожаловать! Проявляй активность и получай бонус GRAND!"




# Обработчик события добавления новых участников в чат
@bot.message_handler(content_types=['new_chat_members'])
def welcome_message(message):
    try:
        chat_id = message.chat.id
        chat_name = message.chat.title
        creator_id = message.from_user.id
        creator_username = message.from_user.username
        username = message.from_user.username

        # Создаем подключение к базе данных
        conn, cursor = create_connection()

        # Получаем информацию о добавленном пользователе
        language = get_creator_language(creator_id)
        prefix = get_creator_prefix(creator_id)
        hi_text = get_hi_text(creator_id)
        earn = "on_earn"
        good_text = "good_on"
        support = "off"
        spam = "on"
        fuck = "on"
        flood = "on"
        duration_spam1 = 3600
        duration_spam2 = 10800
        duration_spam3 = 86400
        duration_fuck1 = 3600
        duration_fuck2 = 10800
        duration_fuck3 = 86400
        duration_flood1 = 3600
        duration_flood2 = 10800
        duration_flood3 = 86400
        link = "on"
        key = "non"
        new_members = message.new_chat_members

        for member in new_members:
            try:
                if member.is_bot:
                    # Если добавленный пользователь - бот, выполняем код приветствия и добавления информации о чате в базу данных
                    print("Бот был добавлен в чат")

                    # Проверяем, есть ли чат уже в базе данных
                    cursor.execute("SELECT * FROM chats WHERE chat_id=?", (chat_id,))
                    chat_exists = cursor.fetchone()

                    if not chat_exists:
                        add_chat_to_db(cursor, conn, chat_id, chat_name, creator_id, creator_username, language, hi_text, earn, good_text, support, spam, fuck, flood, duration_spam1, duration_spam2, duration_spam3, duration_fuck1, duration_fuck2, duration_fuck3, duration_flood1, duration_flood2, duration_flood3, link, key, prefix)
                        print("Чат успешно добавлен в базу данных")
                    else:
                        print("Чат уже существует в базе данных")

                    # Проверяем, активирован ли уже бот в чате
                    cursor.execute("SELECT * FROM active_chats WHERE chat_id=?", (chat_id,))
                    active_chat_exists = cursor.fetchone()

                    if not active_chat_exists:
                        # Если чат не активирован, активируем его и добавляем в базу данных
                        add_active_chat_to_db(cursor, conn, chat_id)
                        print("Чат успешно активирован")
                    else:
                        print("Бот уже активирован в этом чате")

                    # Проверяем, есть ли создатель в базе данных
                    cursor.execute("SELECT * FROM creators WHERE creator_id=? AND chat_id=?", (creator_id, chat_id))
                    creator_exists = cursor.fetchone()

                    if not creator_exists:
                        # Если создателя нет в базе данных, добавляем его
                        add_creator_to_db(cursor, conn, creator_id, creator_username, chat_id, chat_name, language)
                        print("Создатель успешно добавлен в базу данных")
                    else:
                        print("Создатель уже существует в базе данных")

                    # Отправляем приветственное сообщение
                    if language == 'en':
                        bot.send_message(chat_id, 'Hi! Be active in chat and get a GRAND bonus for it!\n\n TESTING - POSSIBLE FAILURES')
                    else:
                        bot.send_message(chat_id, 'Привет! Проявляй активность в чате и получай за это бонус GRAND!\n\n ТЕСТИРОВАНИЕ - ВОЗМОЖНЫ СБОИ')
                else:
                    try:
                        # Если добавленный пользователь - не бот, отправляем сообщение с приветствием
                        print("Неизвестный пользователь был добавлен в чат")
                        cursor.execute("SELECT hi_text, earn, language FROM chats WHERE chat_id=?", (chat_id,))
                        hi_text_row = cursor.fetchone()
                        earn_row = cursor.fetchone()
                        language_row = cursor.fetchone()
                        user_mention = f'<a href="tg://user?id={member.id}">{member.first_name}</a>'
                        if hi_text_row:
                            welcome_message = f'{user_mention}, {hi_text_row[0]}'
                            bot.send_message(chat_id, welcome_message, parse_mode='HTML')
                        else:
                            if earn_row == "on_earn":
                                if language_row == "rus":
                                    welcome_message = f'{user_mention}, Добро пожаловать! Проявляй активность и получай бонус GRAND!'
                                else:
                                    welcome_message = f'{user_mention}, Welcome! Be active and earn GRAND bonus!'
                                bot.send_message(chat_id, welcome_message, parse_mode='HTML')
                            else: 
                                if language_row == "rus":
                                    welcome_message = f'{user_mention}, Добро пожаловать!'
                                else:
                                    welcome_message = f'{user_mention}, Welcome!'
                                bot.send_message(chat_id, welcome_message, parse_mode='HTML')

                    except Exception as e:
                        error_message = (
                            f"⚠️ Произошла ошибка при Добавлении бота в чат:\n"
                            f"• Тип ошибки: {e.__class__.__name__}\n"
                            f"• Описание: {e}\n"
                            f"• Строка: {e.__traceback__.tb_lineno}\n"
                            f"• Chat ID: {chat_id}\n"
                            f"• Chat name: {chat_name}\n"
                            f"• Creator ID: {creator_id}\n"
                            f"• Creatorname: @{username}\n"
                            f"• Message: {message}\n"
                            f"• Время: {datetime.now()}"
                        )
                        # Используйте библиотеку logging для записи сообщения об ошибке
                        logging.error(error_message)
            except Exception as e:
                error_message = (
                    f"⚠️ Произошла ошибка при Добавлении бота в чат:\n"
                    f"• Тип ошибки: {e.__class__.__name__}\n"
                    f"• Описание: {e}\n"
                    f"• Строка: {e.__traceback__.tb_lineno}\n"
                    f"• Chat ID: {chat_id}\n"
                    f"• Chat name: {chat_name}\n"
                    f"• Creator ID: {creator_id}\n"
                    f"• Creatorname: @{username}\n"
                    f"• Message: {message}\n"
                    f"• Время: {datetime.now()}"
                )
                # Используйте библиотеку logging для записи сообщения об ошибке
                logging.error(error_message)
                
                bot.send_message(chat_id, "⚠️ Произошла ошибка при добавлении. Пожалуйста, напишите @VadimBussS и опишите проблему.") 

                    
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных SQLite: {e}")


    finally:
        # Закрываем подключение к базе данных
        if 'conn' in locals() and conn:
            close_connection(conn) 



try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)