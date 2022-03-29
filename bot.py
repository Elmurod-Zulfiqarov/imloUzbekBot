import logging

from aiogram import Bot, Dispatcher, executor, types
from checkWord import checkWord
from transliterate import to_cyrillic, to_latin

API_TOKEN = 'Your bot token'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.reply("imloUzbek Botiga Xush Kelibsiz!")

@dp.message_handler(commands='help')
async def help_user(message: types.Message):
    await message.reply("Botdan foydalanish uchun so'z yuboring.")

@dp.message_handler()
async def checkImlo(message: types.Message):
    word = message.text
    # javob = lambda msg: to_cyrillic(word) if msg.isascii() else to_latin(word)
    # bot.reply_to(message, javob(msg))
    is_latin = False
    if word.isascii():
        word = to_cyrillic(word)
        is_latin = True

    result = checkWord(word)
    if result['available']:
        response = f"✅ {word.capitalize()}"
    else:
        response = f"❌{word.capitalize()}\n"
        for text in result['matches']:
            response += f"✅ {text.capitalize()}\n"

    if is_latin:
        response = to_latin(response)
        await message.answer(response)
    else:
        await message.answer(response)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
