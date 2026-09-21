import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Токен твоего бота
BOT_TOKEN = "8449897374:AAFWjG3tHiwt6cveCvF87WMQRqjNwNVbjNA"

# Актуальный ключ доступа
CURRENT_KEY = "Doorware2026"

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# Главное меню с кнопками
def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔑 Получить ключ", callback_data="get_key")
    builder.button(text="📢 Наш канал", url="https://t.me/your_channel")  # Замени на ссылку твоего канала/группы
    builder.adjust(1)
    return builder.as_markup()

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"👋 Привет, <b>{message.from_user.first_name}</b>!\n\n"
        "Добро пожаловать в официальный бот <b>Doorware Hub</b>.\n"
        "Здесь ты можешь получить актуальный ключ доступа к скрипту.",
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )

# Обработка нажатия на кнопку "Получить ключ"
@dp.callback_query(F.data == "get_key")
async def process_get_key(callback: types.CallbackQuery):
    text = (
        "🔑 <b>Твой ключ для Doorware:</b>\n\n"
        f"<code>{CURRENT_KEY}</code>\n\n"
        "📌 <i>Нажми на ключ, чтобы скопировать его, и вставь в окно скрипта в игре!</i>"
    )
    
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer("Ключ выдан!")

async def main():
    print("Бот Doorware успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())