import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, html
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

BOT_TOKEN = "8938367602:AAHK5WxE5nqk9m0Aag_18Nofk4Hf3AMrcWg"
CHANNEL_URL = "https://t.me/ScriptWare_s"
SCRIPT_KEY = "Release"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Словарь со всеми текстами для двух языков
TEXTS = {
    "ru": {
        "welcome": "👋 Привет, <b>{name}</b>!\n\nДобро пожаловать в <b>Doorware Hub</b>.\nЗдесь ты можешь получить актуальный ключ доступа к скрипту.",
        "btn_key": "🔑 Получить ключ",
        "btn_channel": "📢 Наш канал",
        "btn_lang": "🌐 Сменить язык / Change language",
        "key_msg": "🔑 <b>Твой ключ для Doorware:</b>\n\n<code>{key}</code>\n\n📌 <i>Нажми на ключ, чтобы скопировать его, и вставь в окно скрипта в игре!</i>"
    },
    "en": {
        "welcome": "👋 Hello, <b>{name}</b>!\n\nWelcome to <b>Doorware Hub</b>.\nHere you can get the current access key for the script.",
        "btn_key": "🔑 Get Key",
        "btn_channel": "📢 Our Channel",
        "btn_lang": "🌐 Change language / Сменить язык",
        "key_msg": "🔑 <b>Your key for Doorware:</b>\n\n<code>{key}</code>\n\n📌 <i>Click on the key to copy it, then paste it into the script in-game!</i>"
    }
}

# Клавиатура выбора языка
def get_language_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
            ]
        ]
    )

# Главное меню на выбранном языке
def get_main_keyboard(lang: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=TEXTS[lang]["btn_key"], callback_data="get_key")],
            [InlineKeyboardButton(text=TEXTS[lang]["btn_channel"], url=CHANNEL_URL)],
            [InlineKeyboardButton(text=TEXTS[lang]["btn_lang"], callback_data="change_lang")]
        ]
    )

# Старт — сразу предлагаем выбрать язык
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "🌐 <b>Выберите язык / Choose language:</b>",
        reply_markup=get_language_keyboard(),
        parse_mode="HTML"
    )

# Обработка выбора языка
@dp.callback_query(F.data.startswith("lang_"))
async def process_language_choice(callback: types.CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    await state.update_data(lang=lang)
    
    first_name = html.quote(callback.from_user.first_name)
    welcome_text = TEXTS[lang]["welcome"].format(name=first_name)
    
    await callback.message.edit_text(
        welcome_text,
        reply_markup=get_main_keyboard(lang),
        parse_mode="HTML"
    )
    await callback.answer()

# Нажатие на кнопку смены языка из главного меню
@dp.callback_query(F.data == "change_lang")
async def process_change_lang(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🌐 <b>Выберите язык / Choose language:</b>",
        reply_markup=get_language_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

# Получение ключа
@dp.callback_query(F.data == "get_key")
async def process_get_key(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get("lang", "ru")  # По умолчанию Русский
    
    key_text = TEXTS[lang]["key_msg"].format(key=SCRIPT_KEY)
    await callback.message.answer(key_text, parse_mode="HTML")
    await callback.answer()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
