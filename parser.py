import logging
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
ua = UserAgent()

bot_token = "5269388867:AAEyW7KPQyqX_KZiDNJRDgFM-2jR_B70zKQ"
bot = Bot(token = bot_token)
dp = Dispatcher(bot)
logging.basicConfig(level = logging.INFO)


@dp.message_handler(commands="start")
async def cmd_test(message: types.Message):
    await message.answer('Список команд: \n/chek-проверяет товар на изменение цены')


@dp.message_handler(commands='chek')
async def chek(message: types.Message):
    await message.answer(f"{parse_gend()[0]}, {parse_gend()[1]}, {parse_gend()[2]}", reply_markup = types.ReplyKeyboardRemove())




def parse_gend():
    current_datetime = datetime.now()
    time = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
    url = 'http://gendalf.cf/'
    r = requests.get(url=url)
    r.encoding = 'utf-8'
    response = r.text
    soup = BeautifulSoup(response, 'lxml')
    body = soup.find('body')
    name = body.find('h1').text
    price = body.find('h2').text.replace('Цена: ', '').replace('₽', '').replace(' ', '')
    return time, int(price), name



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)