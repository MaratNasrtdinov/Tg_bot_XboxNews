import json

import requests
from bs4 import BeautifulSoup

news_dict = {}
def get_first_news():
    url = 'https://gamemag.ru/news/platform/xsex'
    headers = {
        'accept': 'application/json, text/plain, */*',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36",
        'Accept - Encoding': 'gzip, deflate, br'
    }
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    ar_cards = soup.find_all('div', class_='news-item')
    for a in ar_cards:
        try:
            a_title = a.find('a', class_='news-item__text').text
            a_url = f'https://gamemag.ru{a.find("a", class_="news-item__text").get("href")}'
        except:
            pass
        a_id = a_url.split('/')[4]
        print(f"{a_title} | {a_url}")

        news_dict[a_id] = {
            'title': a_title,
            'url': a_url
        }
    with open("news_dict.json", 'w', encoding='utf-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

def check_news_update():
    with open("news_dict.json", encoding='utf-8') as file:
        news_dict = json.load(file)

    url = 'https://gamemag.ru/news/platform/xsex'
    headers = {
        'accept': 'application/json, text/plain, */*',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36",
        'Accept - Encoding': 'gzip, deflate, br'
    }
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    ar_cards = soup.find_all('div', class_='news-item')
    fresh_news = {}
    for a in ar_cards:
        try:
            a_title = a.find('a', class_='news-item__text').text
            a_url = f'https://gamemag.ru{a.find("a", class_="news-item__text").get("href")}'
        except:
            pass
        a_id = a_url.split('/')[4]

        if a_id in news_dict:
            continue
        else:
            try:
                a_title = a.find('a', class_='news-item__text').text
                a_url = f'https://gamemag.ru{a.find("a", class_="news-item__text").get("href")}'
            except:
                pass
            a_id = a_url.split('/')[4]

            news_dict[a_id] = {
                'title': a_title,
                'url': a_url
            }
            fresh_news[a_id] = {
                'title': a_title,
                'url': a_url
            }
    with open("news_dict.json", 'w', encoding='utf-8') as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news
def main():
    #get_first_news()
    print(check_news_update())

if __name__ == '__main__':
    main()





