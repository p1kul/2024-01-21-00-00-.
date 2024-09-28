from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
api = 'ключ'
bot = Bot(api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup()
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button1)
kb.add(button2)
kb.resize_keyboard
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)
@dp.message_handler(text = 'Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(возраст=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def  set_weight(message, state):
    await state.update_data(рост=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(вес=message.text)
    data = await state.get_data()
    calories = 10*int(data['возраст'])+6.25*int(data['рост'])-5*int(data['вес'])+5
    await message.answer(f"Ваша норма калорий {calories}")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)
