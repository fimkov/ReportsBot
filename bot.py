import logging
import sqlite3
from aiogram import Bot, Dispatcher, types, __version__
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
import os
import asyncio
import datetime
from aiogram.utils.exceptions import ChatNotFound, UserDeactivated, BotBlocked
import time
import hashlib
from urllib.parse import urlencode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import os
import requests
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# ——————— КОНФИГ ———————

TOKEN = "" # Токен бота
chat_username = "" # Юзернейм основной группы без @
chat_id =  # Айди группы модерации
anti_flood_time = 30 # Анти-флуд время

# ——————— ЛОГИРОВАНИЕ ———————
logging.basicConfig(level=logging.INFO)

# —————— ИНТАЛИЗАЦИЯ БОТА——————

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# ——————— АНТИ-ФЛУД ———————

async def anti_flood(*args, **kwargs):
    m = args[0]
    chat_id = m.from_user.id
    await m.reply("⛔ || Извините, но вы не можете так часто репортить бота\nПодождите!")

# ——————— ОСНОВА ———————

@dp.message_handler(commands=["claim", "report"])
@dp.throttled(anti_flood,rate=anti_flood_time)
async def report(message: types.Message):
	if message.reply_to_message:
		name = message.reply_to_message.from_user.get_mention(as_html=True)
		await message.reply(f"✅ Репорт на {name} отправлен модераторам на рассмотрение", parse_mode="HTML")
	else:
		await message.reply("❌ Эта команда должна использоваться в ответ на сообщение")
		return
	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton("✅ Принять", callback_data="accept"))
	more = message.text.replace("/claim", "")
	if more: 
	    more = more.replace("/report", "")
	    if more:
	    	pass
	    else:
	    	more == "Отсутствует"
	else:
		more == "Отсутствует"
	await bot.send_message(chat_id, f"""
⛔ Жалоба от пользователя

ℹ️ Информация
├ Подал жалобу: {message.from_user.get_mention(as_html=True)}
├ Нарушитель: {name}
├ Ссылка на нарушение: <a href='t.me/{chat_username}/{message.reply_to_message.message_id}'>Тык</a>
└ Подробности нарушения: {more}
""", reply_markup=keyboard, parse_mode="HTML")

@dp.callback_query_handler(lambda c: True)
async def button_callback_handler(callback_query: types.CallbackQuery):
    message = callback_query.message
    data = callback_query.data
    if data == "accept":
    	await callback_query.answer("✅ Принято")
    	name = callback_query.from_user.get_mention(as_html=True)
    	await message.edit_text(message.html_text + f"\n\n✅ {name} принял жалобу", parse_mode="HTML")
    else:
    	await callback_query.answer("Ты чо совсем тупой?")
    
# ——————— ЗАПУСК ———————

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)	
