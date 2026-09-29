import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F, html
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

# Токен береться зі змінних оточення Railway (Environment Variables)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8938367602:AAHK5WxE5nqk9m0Aag_18Nofk4Hf3AMrcWg")

CHANNEL_ID = "@ScriptWare_s"
CHANNEL_URL = "https://t.me/ScriptWare_s"
SCRIPT_KEY = "Release"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

TEXTS = {
    "ru": {
        "welcome": "👋 Привет, <b>{name}</b>!\n\nДобро пожаловать в <b>Doorware Hub</b>.\nЗдесь ты можешь получить актуальный ключ доступа к скрипту.",
        "btn_key": "🔑 Получить ключ",
        "btn_channel": "📢 Наш канал",
        "btn_lang": "🌐 Сменить язык / Change language",
        "key_msg": "🔑 <b>Твой ключ для Doorware:</b>\n\n<code>{key}</code>\n\n📌 <i>Нажми на ключ, чтобы скопировать его, и вставь в окно скрипта в игре!</i>",
        "sub_required": "⚠️ <b>Для получения ключа необходимо подписаться на наш канал!</b>\n\nПожалуйста, подпишитесь на канал ниже и нажмите кнопку «Проверить подписку».",
        "btn_sub": "📢 Подписаться на ScriptWare",
        "btn_check_sub": "✅ Проверить подписку",
        "sub_error": "❌ Вы всё ещё не подписались на канал! Попробуйте снова."
    },
    "en": {
        "welcome": "👋 Hello, <b>{name}</b>!\n\nWelcome to <b>Doorware Hub</b>.\nHere you can get the current access key for the script.",
        "btn_key": "🔑 Get Key",
        "btn_channel": "📢 Our Channel",
        "btn_lang": "🌐 Change language / Сменить язык",
        "key_msg": "🔑 <b>Your key for Doorware:</b>\n\n<code>{key}</code>\n\n📌 <i>Click on the key to copy it, then paste it into the script in-game!</i>",
        "sub_required": "⚠️ <b>You must subscribe to our channel to get the key!</b>\n\nPlease subscribe to the channel below and click the \"Check subscription\" button.",
        "btn_sub": "📢 Subscribe to ScriptWare",
        "btn_check_sub": "✅ Check Subscription",
        "sub_error": "❌ You are still not subscribed to the channel! Please try again."
    }
}

async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        logging.info(f"User {user_id} status in {CHANNEL_ID}: {member.status}")
        
        # Перевірка: користувач має бути творцем, адміном або підписником
        if member.status in ["creator", "administrator", "member"]:
            return True
        else:
            return False
    except TelegramBadRequest as e:
        logging.error(f"TelegramBadRequest: Переконайся, що бот є адміном у {CHANNEL_ID}. Помилка: {e}")
        return False
    except Exception as e:
        logging.error(f"Помилка перевірки підписки для {user_id}: {e}")
        return False

def get_language_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский / RU", callback_data="lang_ru"),
                InlineKeyboardButton(text="🇬🇧 English / EN", callback_data="lang_en")
            ]
        ]
    )

def get_main_keyboard(lang: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=TEXTS[lang]["btn_key"], callback_data="get_key")],
            [InlineKeyboardButton(text=TEXTS[lang]["btn_channel"], url=CHANNEL_URL)],
            [InlineKeyboardButton(text=TEXTS[lang]["btn_lang"], callback_data="change_lang")]
        ]
    )

def get_sub_keyboard(lang: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=TEXTS[lang]["btn_sub"], url=CHANNEL_URL)],
            [InlineKeyboardButton(text=TEXTS[lang]["btn_check_sub"], callback_data="check_sub")]
        ]
    )

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "🌐 <b>Выберите язык / Choose language:</b>",
        reply_markup=get_language_keyboard(),
        parse_mode="HTML"
    )

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

@dp.callback_query(F.data == "change_lang")
async def process_change_lang(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🌐 <b>Выберите язык / Choose language:</b>",
        reply_markup=get_language_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()

@dp.callback_query(F.data == "get_key")
async def process_get_key(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get("lang", "ru")

    is_subscribed = await check_subscription(callback.from_user.id)

    if is_subscribed:
        key_text = TEXTS[lang]["key_msg"].format(key=SCRIPT_KEY)
        await callback.message.answer(key_text, parse_mode="HTML")
    else:
        await callback.message.answer(
            TEXTS[lang]["sub_required"],
            reply_markup=get_sub_keyboard(lang),
            parse_mode="HTML"
        )
    
    await callback.answer()

@dp.callback_query(F.data == "check_sub")
async def process_check_sub(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    lang = user_data.get("lang", "ru")

    is_subscribed = await check_subscription(callback.from_user.id)

    if is_subscribed:
        await callback.answer("✅ Подписка подтверждена / Subscription confirmed!")
        key_text = TEXTS[lang]["key_msg"].format(key=SCRIPT_KEY)
        await callback.message.edit_text(key_text, parse_mode="HTML")
    else:
        await callback.answer(TEXTS[lang]["sub_error"], show_alert=True)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
