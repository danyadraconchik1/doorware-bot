import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8449897374:AAFWjG3tHiwt6cveCvF87WMQRqjNwNVbjNA"
CHANNEL_URL = "https://t.me/ScriptWare_s"
SCRIPT_KEY = "Release"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔑 Получить ключ", callback_data="get_key")],
            [InlineKeyboardButton(text="📢 Наш канал", url=CHANNEL_URL)]
        ]
    )

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    first_name = types.html.quote(message.from_user.first_name)
    welcome_text = (
        f"👋 Привет, <b>{first_name}</b>!\n\n"
        "Добро пожаловать в официальный бот <b>Doorware Hub</b>.\n"
        "Здесь ты можешь получить актуальный ключ доступа к скрипту."
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML")

@dp.callback_query(F.data == "get_key")
async def process_get_key(callback: types.CallbackQuery):
    key_text = (
        f"🔑 <b>Твой ключ для Doorware:</b>\n\n"
        f"<code>{SCRIPT_KEY}</code>\n\n"
        f"📌 <i>Нажми на ключ, чтобы скопировать его, и вставь в окно скрипта в игре!</i>"
    )
    await callback.message.answer(key_text, parse_mode="HTML")
    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
