import telebot
from telebot import types
from PIL import Image, ImageOps
import io


TOKEN = 'your_telegram_token'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "Вітаю! Надішліть мені фото, і я зменшу їх розмір.", reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    photo = message.photo[-1]

    file_info = bot.get_file(photo.file_id)
    file = bot.download_file(file_info.file_path)

    image = Image.open(io.BytesIO(file))
    size = (1080, 1080)
    image = image.resize(size)

    output_buffer = io.BytesIO()
    image.save(output_buffer, format='JPEG')
    output_buffer.seek(0)

    bot.send_photo(message.chat.id, output_buffer)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Вибачте, я розумію тільки фото.")


if __name__ == "__main__":
    bot.polling(none_stop=True)

