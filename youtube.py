import logging
from aiogram import Bot, Dispatcher, executor, types
import requests
from bs4 import BeautifulSoup

bot_token = "5384011512:AAFqHf9uN_j46Se5Tdm3rtVdF2sK5zsR8eU"
bot = Bot(token = bot_token)
dp = Dispatcher(bot)
logging.basicConfig(level = logging.INFO)

@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    await message.answer("Список команд: \n/info - выводит информацию о фотоаппарате")


@dp.message_handler(commands="info")
async def cmd_test1(message: types.Message):
    await message.answer_photo('https://items.s1.citilink.ru/1144223_v01_b.jpg')
    await message.answer(f'{price_checker()[0]}\n {price_checker()[1]}')




def price_checker():
    url = 'https://www.citilink.ru/product/zerkalnyi-fotoapparat-canon-eos-250d-kit-ef-s-18-55mm-f-1-4-5-6-is-stm-1144223/'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.3.852 Yowser/2.5 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    response = req.text
    soup = BeautifulSoup(response, 'lxml')
    name = soup.find("div", class_="product_data__gtm-js product_data__pageevents-js ProductCardLayout__product js--ProductCardLayout__product").find('div', class_="ProductCardLayout__product-description").find('h1').text.strip()
    price = soup.find('div', class_="ProductHeader__price-default").text.strip().replace('\n', ': ', 1).replace('\n', '').replace(':', '').replace('                                                 ₽', '')
    return name, price




if __name__ == "__main__":
    # print(price_checker())
    executor.start_polling(dp, skip_updates = True)

