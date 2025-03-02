import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def collect_user_rates(user_login):
    page_num = 1

    data = []

    while True:
        url = f'https://www.kinopoisk.ru/user/{user_login}/votes/list/vs/vote/page/{page_num}/#list'
        html_content = requests.get(url).text
        print(url)

        soup = BeautifulSoup(html_content, 'lxml')
        entries = soup.find_all('div', class_='item')

        if len(entries) == 0:  # Признак остановки
            print("Фильмов больше нет, либо их не удалось получить")
            break

        for entry in entries:
            div_film_details = entry.find('div', class_="nameRus")
            film_name = div_film_details.find('a').text

            watching_date = entry.find('div', class_='date').text   # достаем дату просмотра

            rating = entry.find('div', class_="vote").text  # достаем оценку фильма

            data.append({'Фильм': film_name, 'Дата просмотра': watching_date, 'Оценка': rating})

        page_num += 1  # Переходим на следующую страницу
        time.sleep(5)  # Выставил задержку, чтобы хоть как-то обойти защиту кинопоиска
    return data


user_rates = collect_user_rates(user_login='30814714')
df = pd.DataFrame(user_rates)

df.to_excel('user_rates.xlsx')