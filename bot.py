import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Токен твоего бота
BOT_TOKEN = "8938367602:AAEtzFvfhzwkxw8ug_iilulZ8Cmev2eW8XQ"

# ID или юзернейм канала (канал должен быть публичным, либо бот должен быть в нем админом)
CHANNEL_ID = "@your_channel_username"  # Замени на юзернейм своего канала (например, @my_channel) или ID (-100xxxxxxxxx)
CHANNEL_URL = "https://t.me/your_channel_username"  # Ссылка на канал для кнопки

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def check_subscription(user_id: int) -> bool:
    """Функция проверки, подписан ли пользователь на канал."""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # Пользователь считается подписанным, если его статус member, administrator или creator
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logging.error(f"Ошибка при проверке подписки: {e}")
        return False


def get_sub_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой подписки и проверки."""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться на канал", url=CHANNEL_URL)],
            [InlineKeyboardButton(text="✅ Я подписался", callback_data="check_sub")]
        ]
    )
    return keyboard


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    is_subscribed = await check_subscription(message.from_user.id)
    
    if is_subscribed:
        await message.answer("👋 Добро пожаловать! Вы подписаны на канал, доступ открыт.")
    else:
        await message.answer(
            "⚠️ Для использования бота необходимо подписаться на наш канал!",
            reply_markup=get_sub_keyboard()
        )


@dp.callback_query(F.data == "check_sub")
async def process_check_sub(callback: types.CallbackQuery):
    is_subscribed = await check_subscription(callback.from_user.id)
    
    if is_subscribed:
        await callback.message.edit_text("🎉 Спасибо за подписку! Теперь вам доступен весь функционал бота.")
        await callback.answer()
    else:
        await callback.answer("❌ Вы всё ещё не подписались на канал!", show_alert=True)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
