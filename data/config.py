import logging
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
bot_token = "5314593440:AAFPrrMhDSOj1vGkfRnnKlTegITv8hNSwDY"
bot = Bot(token = bot_token)
dp = Dispatcher(bot)
logging.basicConfig(level = logging.INFO)

@dp.message_handler(commands="start")
async def cmd_test(message: types.Message):
    await message.answer('Список команд: \n/chek-проверяет товар на изменение цены')

@dp.message_handler(commands='chek')
async def chek(message: types.Message):
    await message.answer(f"{new_parse()[1]} \n{new_parse()[2]} \n{new_parse()[3]}", reply_markup = types.ReplyKeyboardRemove())




def new_parse():
    current_datetime = datetime.now()
    time = current_datetime.strftime("%d-%m-%Y %H:%M:%S")
    url = 'http://gendalf.cf:8080/product/игровая-консоль-nintendo-switch-32-gb/'
    r = requests.get(url=url)
    r.encoding = 'utf-8'
    response = r.text
    soup = BeautifulSoup(response, 'lxml')
    name = soup.find('div', class_='summary entry-summary').find('h1').text
    price = soup.find('div', class_='summary entry-summary').find('span', class_='woocommerce-Price-amount amount').find('bdi').text
    return time, name, int(price.split('.')[0])


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)