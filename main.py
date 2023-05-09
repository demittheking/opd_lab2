from aiogram import types, Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import random
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

TOKEN= "6118730780:AAE620cckhXKA_KsZ9Ckzg3pH5a_DvQfJv0"
bot=Bot(token= TOKEN)
dp= Dispatcher(bot, storage=MemoryStorage())
fact=False
chislo=50
tries=6
n=50
point=0

class levels(StatesGroup):
    hardset=State()
    size= State()
    enter = State()
@dp.message_handler(commands=['start'],state=None)
async def command_start(message:types.message, state: FSMContext):
    await message.answer ('Добро пожаловать в игру "Угадай число" \n Тебе нужно угадать число,которое я тебе загадаю \n Напиши любой символ/слово, чтобы продолжить')
    await levels.hardset.set()

@dp.message_handler(state=levels.hardset)
async def hardset(message:types.message, state: FSMContext):
    await message.answer('Выбери сложность игры (диапазон чиссел \n 50 или 100 цифр?')
    await levels.size.set()

@dp.message_handler(state=levels.size)
async def echo_send1(message: types.message, state: FSMContext):
    global n
    global chislo
    global tries
    if int(message.text)==50 :
        n=50
        chislo = random.randint(1, 50)
        tries=6
        await message.answer('Угадай число от 1 до 50, у тебя есть 6 попыток')
    elif int(message.text)==100:
        n=100
        chislo=random.randint(1,100)
        tries=7
        await message.answer('Угадай число от 1 до 100, у тебя есть 7 попыток')
    else:
        await message.answer('Диапазон чисел выбран неверно, попробуйте снова')
        return
    await levels.enter.set()

@dp.message_handler(state=levels.enter)
async def echo_send2(message: types.message, state: FSMContext):
    global tries
    global chislo
    global point
    point=0
    if n==50:
        while(tries!=0):
            if int(message.text)>=1 and int(message.text)<=50 :
                if int(message.text) == chislo:
                    await message.answer('Вы угадали число')
                    tries=0
                    point=1
                    break
                elif int(message.text) > chislo:
                    await message.answer('Не угадали, число меньше')
                    tries-=1
                    if tries!=0:
                        return
                else:
                    await message.answer('Не угадали, число больше')
                    tries-=1
                    if tries!=0:
                        return
            else:
                await message.answer('Введено не число, либо число вне диапазона')
                return
        if point==1:
            await message.answer('Молодец! \n Напиши любой символ/слово, чтобы начать игру заново')
        else:
            await message.answer('Число попыток закончилось, вы не угадали число \n Напиши любой символ/слово, чтобы начать игру заново')

        tries=6
    elif n==100:
        while (tries != 0):
            if int(message.text)>=1 and int(message.text)<=100 :
                if int(message.text) == chislo:
                    await message.answer('Вы угадали число')
                    tries = 0
                    point = 1
                    break
                elif int(message.text) > chislo:
                    await message.answer('Не угадали, число меньше')
                    tries -= 1
                    if tries != 0:
                        return
                else:
                    await message.answer('Не угадали, число больше')
                    tries -= 1
                    if tries != 0:
                        return
            else:
                await message.answer('Введено не число, либо число вне диапазона')
                return
        if point==1:
            await message.answer('Молодец! \n Напиши любой символ/слово, чтобы начать игру заново')
        elif point==0:
            await message.answer('Число попыток закончилось, вы не угадали число \n Напиши любой символ/слово, чтобы начать игру заново')
        tries=7
    await levels.hardset.set()
    #await state.finish()



if __name__== "__main__":
    executor.start_polling(dp, skip_updates= True)