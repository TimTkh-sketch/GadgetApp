
import asyncio
import json
import os
import random
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8081320331:AAHPf2stF6Vs_I0yH3WICmHcFK6CNzThP5U"

bot = Bot(token=TOKEN)
dp = Dispatcher()

DATA_FILE = "stats.json"

# Загрузка данных
def load_data():
    if not os.path.exists(DATA_FILE):
        base = random.randint(7, 100)
        return {
            "base_value": base,
            "current_value": base,
            "last_update": datetime.now().strftime("%Y-%m-%d"),
            "increase_time": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # Гарантируем, что current_value не None
    if data.get("current_value") is None:
        data["current_value"] = data.get("base_value", random.randint(100, 200))

    return data

# Сохранение
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# Обновление статистики
def update_stats():
    global data

    today = datetime.now().strftime("%Y-%m-%d")

    # Обновление раз в день
    if data["last_update"] != today:
        base = random.randint(100, 200)
        data["base_value"] = base
        data["current_value"] = base
        data["last_update"] = today
        data["increase_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        save_data(data)
        return

    # Увеличение раз в 3 часа
    last_inc = datetime.strptime(data["increase_time"], "%Y-%m-%d %H:%M")
    if datetime.now() - last_inc >= timedelta(hours=3):
        data["current_value"] += 5
        data["increase_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        save_data(data)

# Клавиатура
def start_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Наш канал 💌", url="https://t.me/gadgetmarketpro"),
                InlineKeyboardButton(text="Спросить? 🧑‍💼", url="https://t.me/gadget_perm")
            ],
            [
                InlineKeyboardButton(text="Оставить отзыв ✍️", url="https://yandex.ru/maps/-/CHRuBT00")
            ]
        ]
    )

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    update_stats()

    user_name = message.from_user.first_name
    counter = data["current_value"]

    photo_url = "https://i.yapx.ru/c3k1M.png"

    caption = (
        f"{user_name}, добро пожаловать в *GadgetMarket App*— удобного бота, который позволяет"
        "быстро и удобно выбрать и заказать оригинальную технику в Telegram.\n\n"
        f"Сегодня заказов оформлено: *{counter}* 📦\n\n"
        "Нам доверяют сотни постоянных клиентов, ценящих качество и надёжность сервиса.\n"
        "Попробуйте и вы — это легко, комфортно и занимает минимум времени."
    )
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=caption,
        reply_markup=start_keyboard(),
        parse_mode="Markdown"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
