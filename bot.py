import logging
from aiogram import Bot, Dispatcher, executor, types
import requests
from bs4 import BeautifulSoup

bot_token = "5141087158:AAFq0VulhrM8a1vkedQ67UUJrCsgUhWBEvE"
bot = Bot(token = bot_token)
dp = Dispatcher(bot)
logging.basicConfig(level = logging.INFO)

@dp.message_handler(commands="start")
async def cmd_test1(message: types.Message):
    await message.answer("Введите название фильма, чтобы получить информацию о нём.")

@dp.message_handler()
async def kino(message: types.Message):
    await message.answer('IMDB \nНазвание: ' + parse_imdb(message.text)[0] + '\nРейтинг: ' + parse_imdb(message.text)[1] + '\nКинопоиск \nНазвание: ' + parse_kinopoisk(message.text)[0] + '\nРейтинг: ' + parse_kinopoisk(message.text)[1], reply_markup = types.ReplyKeyboardRemove())

def parse_imdb(film):
    try:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36'
        }
        film = film.split()
        req = requests.get(f'https://www.imdb.com/find?q={"+".join(film)}&ref_=nv_sr_sm', headers = headers)
        resp = req.text
        soup = BeautifulSoup(resp, 'lxml')
        href = 'https://www.imdb.com' + soup.find('table', class_ = 'findList').find('tr', class_ = 'findResult odd').find('td',class_ = 'result_text').find('a').get("href")
        if href is not None:
            req_film = requests.get(href, headers = headers)
            soup = BeautifulSoup(req_film.text, 'lxml')
            name = soup.find(attrs = {"data-testid": "hero-title-block__title"})
            rait = soup.find(attrs = {"data-testid": "hero-rating-bar__aggregate-rating__score"}).find('span', class_='sc-7ab21ed2-1 jGRxWM')
            return name.text, rait.text
    except:
        print('Упс, что-то пошло не так(')

def parse_kinopoisk(film):
    film = film.split()
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.119 YaBrowser/22.3.0.2430 Yowser/2.5 Safari/537.36'
    }
    req = requests.get(f'https://www.kinopoisk.ru/index.php?kp_query={"+".join(film)}', headers=headers)
    response = req.text
    soup = BeautifulSoup(response, 'lxml')
    name = soup.find('div', class_='element most_wanted').find('div', class_='info').find('p', class_='name').text
    reit = soup.find('div', class_='element most_wanted').find('div', class_='right').find('div',class_='rating ratingGreenBG').text
    return name, reit

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)


















