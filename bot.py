import os
import telebot
from telebot import types

# 1) Токен берём из переменных окружения на Render
TOKEN = os.getenv("TOKEN")

# 2) Полный путь к PDF рядом с этим файлом
PDF_FILE = os.path.join(os.path.dirname(__file__), "brochure.pdf")
ACCESS_CODE = os.getenv("ACCESS_CODE", "VITAMIN-999")
pending_codes = set()  # здесь храним user_id, кому запросили код
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
    btn2 = types.InlineKeyboardButton("💳 Оплатить PayPal", url="https://paypal.me/IrynaKrasotkina754/9.90EUR")
    btn3 = types.InlineKeyboardButton("📥 Получить PDF", callback_data="get_pdf")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
@bot.callback_query_handler(func=lambda c: c.data == "get_pdf")
def ask_code(call):
    try:
        uid = call.from_user.id
        pending_codes.add(uid)
        bot.answer_callback_query(call.id)
        bot.send_message(
            uid,
            "🧾 Для получения PDF введите *код доступа* (его видно после оплаты).",
            parse_mode="Markdown"
        )
    except Exception as e:
        bot.answer_callback_query(call.id, "Не удалось открыть PDF 😔")
        print("PDF error:", e)

@bot.message_handler(func=lambda m: m.from_user.id in pending_codes)
def check_code(msg):
    code = msg.text.strip()
    if code == ACCESS_CODE:
        try:
            with open(PDF_FILE, "rb") as f:
                bot.send_document(
                    msg.chat.id,
                    f,
                    visible_file_name="Оздоровительные_напитки.pdf"
                )
            bot.send_message(msg.chat.id, "Готово! Спасибо за оплату 🌿")
        except Exception as e:
            bot.send_message(msg.chat.id, "Не удалось открыть PDF 😔")
            print("PDF error:", e)
        finally:
            # в любом случае убираем пользователя из «ожидающих кода»
            pending_codes.discard(msg.from_user.id)
    else:
        bot.reply_to(msg, "Код неверный — проверьте и попробуйте ещё раз 😉")

if __name__ == "__main__":
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
