from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from aiogram.utils.markdown import hbold
import json
from aiogram.dispatcher.filters import Text
from main import check_news_update
import asyncio
import pymysql

bot = Bot(TOKEN=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

try:
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='mysql',
        password='mysql',
        database='test'
    )
    print('ok')
    cursor = connection.cursor()
except Exception as ex:
    print('not ok')
    print(ex)
#список пользователей

cursor.execute("SELECT user_id from user")
users = list((cursor.fetchall()))
cursor.connection.commit()
cursor.connection.close()
users_list = []
for i in users:
    for j in i:
        users_list.append(int(j))
print(users_list)


@dp.message_handler(Text(equals="/start"))
async def start(msg: types.Message):
    start_buttons = ['Все новости', 'Свежие новости']
    second_buttons = ['Подписаться на рассылку', 'Отписаться от рассылки']
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(*start_buttons)
    kb.add(*second_buttons)
    await msg.answer('Лента новостей', reply_markup=kb)
    try:
        cursor.execute("INSERT INTO user (user_id) VALUES ({0})".format(msg.from_user.id))
        cursor.connection.commit()
        cursor.connection.close()
    except Exception as ex:
        print('dublicate))')

@dp.message_handler(Text(equals='Подписаться на рассылку'))
async def sub(msg: types.Message):
    await msg.answer("Вы подписаны")
    try:
        cursor.execute("UPDATE user SET sub_status = 1")
        cursor.connection.commit()
        cursor.connection.close()
    except Exception as ex:
        print(ex)

@dp.message_handler(Text(equals='Отписаться от рассылки'))
async def sub(msg: types.Message):
    await msg.answer("Вы отписаны")
    try:
        cursor.execute("UPDATE user SET sub_status = NULL")
        cursor.connection.commit()
        cursor.connection.close()
    except Exception as ex:
        print(ex)

@dp.message_handler(Text(equals="Все новости"))
async def get_all_news(msg: types.Message):
    with open('news_dict.json', encoding='utf-8') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news = f"{hbold(v['title'])}\n\n" \
               f"{v['url'][0:34]}"
        await msg.answer(news)

@dp.message_handler(Text(equals="Свежие новости"))
async def get_new_news(msg: types.Message):
    fresh_news = check_news_update()

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"{hbold(v['title'])}\n\n" \
                   f"{v['url'][0:34]}"
            await msg.answer(news)
    else:
        await msg.answer('Пока нет свежих новостей')

async def news_every_minute():
    print('push')

    while True:
        fresh_news = check_news_update()

        if len(fresh_news) >= 1:
            for i in users_list:
                for k, v in sorted(fresh_news.items()):
                    news = f"{hbold(v['title'])}\n\n" \
                           f"{v['url'][0:34]}"
                    await bot.send_message(f'{i}', news, disable_notification=False)
                    print(news)

        else:
            print('нч')
        await asyncio.sleep(30)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)
