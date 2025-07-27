
import telebot
from telebot import types

TOKEN = "7653751280:AAE2J8DmUJcdYwSrRxZ6uuguLg5fLL11rAS0"
PDF_FILE = "brochure.pdf"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "🍃 Привет! Ты в *Твоём домашнем витаминном баре*\n\n"
    text += "Здесь собраны простые и вкусные рецепты, которые помогают заботиться о себе каждый день.\n\n"
    text += "📘 В брошюре — более 30 напитков для детокса, энергии, иммунитета и красоты кожи.\n\n"
    text += "💰 Стоимость: 9,90€\n💧 Выбери удобный способ оплаты ниже и получи свою брошюру автоматически.\n\n"
    text += "🌿 Я собрала эти рецепты с любовью, чтобы они стали частью твоих маленьких ритуалов заботы о себе."

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("💳 Оплатить Revolut", url="https://revolut.me/irynaswan/9.90")
    btn2 = types.InlineKeyboardButton("💳 Оплатить PayPal", url="https://www.paypal.me/krasotckina")
    btn3 = types.InlineKeyboardButton("📥 Получить PDF", callback_data="get_pdf")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "get_pdf")
def send_pdf(call):
    with open(PDF_FILE, "rb") as f:
        bot.send_document(call.message.chat.id, f)

bot.polling(none_stop=True)
