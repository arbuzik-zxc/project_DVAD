import telebot
import os
from telebot import types
from deepface import DeepFace
import dbimg
import sqlite3 as sq


# остановились на username

### Ошибка в обновлении UPDATE!! исправлить на INSERT or UPDATE

API_TOKEN = '7860495879:AAFQAIElHv7iPrH1y9oGSxcqYFDlav3aYxU'  # поменять
bot = telebot.TeleBot(API_TOKEN)
print("Successful!")

main_dir = os.getcwd()


def get_user_folder(username):
    folder_path = os.path.join(main_dir,"data", username)    
    return folder_path

def add_user(username):
    dbimg.add_user(username)

def insert_image(username, img_path, original_or_check):
    dbimg.insert_image(username, img_path, original_or_check)




@bot.message_handler(commands=['start'])
def send_welcome(message):
    add_user(message.from_user.username)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Добавить фото")
    button2 = types.KeyboardButton("Сравнить фото")
    button3 = types.KeyboardButton("Удалить фото")
    markup.add(button1, button2, button3)
    bot.reply_to(message, "Привет! Я - демоверсия Telegram Bot для распознавания лиц от команды ДВАДЭ!", reply_markup=markup)




def handle_check_photo(message, original_file_path, check_file_path):
    if message.content_type == 'photo':
        # Получаем файл фотографии для сравнения
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Создаем папку для проверки, если она не существует
        os.makedirs(os.path.dirname(check_file_path), exist_ok=True)

        # Сохраняем загруженное фото для сравнения
        with open(check_file_path, "wb") as new_file:
            new_file.write(downloaded_file)

        insert_image(message.from_user.username, check_file_path, 'check')

        # Анализируем фотографии
        bot.reply_to(message, "Проводится анализ фото по базе, ожидайте...")
        
        try:
            result = DeepFace.verify(img1_path=original_file_path, img2_path=check_file_path)
            # Обработка результата
            if result['verified']:
                bot.send_message(message.chat.id, "Фотографии совпадают!")
            else:
                bot.send_message(message.chat.id, "Фотографии не совпадают!")
        except Exception as e:
            bot.send_message(message.chat.id, "Ошибка при анализе фотографий. Пожалуйста, попробуйте еще раз.")
            print(f"Ошибка: {e}")  # Выводим ошибку в консоль для отладки
    else:
        bot.reply_to(message, "Пожалуйста, отправьте фото для сравнения.")

@bot.message_handler(func=lambda message: message.text == "Добавить фото")
def ask_for_photo(message):
    username = message.from_user.username if message.from_user.username else "user_" + str(message.from_user.id)
    
    user_folder = get_user_folder(username)
    
    original_file_path = os.path.join(user_folder, "original.jpg")
    
        
    if os.path.exists(original_file_path):
        bot.reply_to(message, "Изображение уже добавлено в базу под вашим именем.")
    else:
        bot.reply_to(message, "Пожалуйста, отправьте мне фото.")
        bot.register_next_step_handler(message, handle_add_photo, original_file_path)
        

def handle_add_photo(message, file_path):
    if message.content_type == 'photo':
        # Получаем файл фотографии
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Создаем папку пользователя, если она не существует
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        

        # Сохраняем файл на локальном устройстве
        with open(file_path, "wb") as new_file:
            new_file.write(downloaded_file)

        insert_image(message.from_user.username, file_path, 'original')

        bot.reply_to(message, "Фото успешно загружено и сохранено!")
    else:
        bot.reply_to(message, "Пожалуйста, отправьте фото.")

@bot.message_handler(func=lambda message: message.text == "Сравнить фото")
def check_photos(message):
    username = message.from_user.username if message.from_user.username else "user_" + str(message.from_user.id)
    user_folder = get_user_folder(username)
    original_file_path = os.path.join(user_folder, "original.jpg")
    check_file_path = os.path.join(user_folder, "check", "check.jpg")

    if os.path.exists(original_file_path):
        bot.reply_to(message, "Пожалуйста, отправьте мне фото для сравнения.")
        bot.register_next_step_handler(message, handle_check_photo, original_file_path, check_file_path)
    else:
        bot.reply_to(message, "Вы не сохраняли свою фотографию.")


@bot.message_handler(func=lambda message: message.text == "Удалить фото")
def ask_for_photo_deletion(message):
    username = message.from_user.username if message.from_user.username else "user_" + str(message.from_user.id)
    user_folder = get_user_folder(username)
    original_file_path = os.path.join(user_folder, "original.jpg")

    if os.path.exists(original_file_path):
        os.remove(original_file_path)
        bot.reply_to(message, "Фото успешно удалено!")
    else:
        bot.reply_to(message, "Фото не найдено.")

if __name__ == '__main__':
    bot.polling()