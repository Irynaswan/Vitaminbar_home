import os
import telebot
from telebot import types

# 1) Токен берём из переменных окружения на Render
TOKEN = os.getenv("TOKEN")

# 2) Полный путь к PDF рядом с этим файлом
PDF_FILE = os.path.join(os.path.dirname(file), "brochure.pdf")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text  = "🍃 Привет! Ты в *Твоём домашнем витаминном баре*\n\n"
    text += "Здесь собраны простые и вкусные рецепты, которые помогают заботиться о себе каждый день.\n"
    text += "📘 В брошюре — более 30 напитков для детокса, энергии, иммунитета и красоты кожи.\n"
    text += "🔥 Стоимость: 9,90€\n"
    text += "💧 Выбери удобный способ оплаты ниже и получи свою брошюру автоматически.\n"
    text += "🌿 Я собрала эти рецепты с любовью, чтобы они стали частью твоих маленьких ритуалов заботы о себе."

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("💳 Оплатить Revolut", url="https://revolut.me/irynaswan/9.90")
    btn2 = types.InlineKeyboardButton("💳 Оплатить PayPal", url="https://www.paypal.me/krasotckina")
    btn3 = types.InlineKeyboardButton("📥 Получить PDF", callback_data="get_pdf")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda c: c.data == "get_pdf")
def send_pdf(call):
    try:
        with open(PDF_FILE, "rb") as f:
            bot.send_document(
                call.message.chat.id,
                f,
                visible_file_name="Оздоровительные_напитки.pdf"
            )
        bot.answer_callback_query(call.id)
    except Exception as e:
        bot.answer_callback_query(call.id, "Не удалось открыть PDF 😕")
        print("PDF error:", e)

if name == "main":
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
