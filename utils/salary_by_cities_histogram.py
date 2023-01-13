import re
import sqlite3
from decimal import Decimal

from matplotlib import pyplot as plt
from pycbrf.toolbox import ExchangeRates

from utils.helper import get_currency_coefficient_by_year

if __name__ == '__main__':
    try:
        sqlite_connection = sqlite3.connect('C:\\Users\\TastePate\\PycharmProjects\\Database\\VacanciesProject\\db.sqlite3')
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")

        sqlite_select_query = "select salary_from, salary_to, salary_currency, area_name, published_at " \
                              "from vacancies_vacancy"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()

        cities = list(set([re.sub(r'\([^()]*\)', '', i[3]) for i in record]))
        salaries_in_rur_by_cities = {key: [] for key in cities}
        for r in record:
            date = r[4][:10]
            current_city = re.sub(r'\([^()]*\)', '', r[3])
            if r[2] != '':
                salary_currency_coefficient = get_currency_coefficient_by_year(int(date[:4]), r[2])
                if r[0] is None:
                    salaries_in_rur_by_cities[current_city].append(Decimal(r[1]) * salary_currency_coefficient)
                elif r[1] is None:
                    salaries_in_rur_by_cities[current_city].append(Decimal(r[0]) * salary_currency_coefficient)
                else:
                    salaries_in_rur_by_cities[current_city].append((Decimal(r[0]) * salary_currency_coefficient +
                                                                    Decimal(r[1]) * salary_currency_coefficient) / 2)
        salaries_in_rur_by_cities = {key: round(sum(value) / len(value)) for key, value in salaries_in_rur_by_cities.items() if len(value) >= 5}
        print(salaries_in_rur_by_cities)
        salaries_in_rur_by_cities = dict(sorted(salaries_in_rur_by_cities.items(), key=lambda item: item[1], reverse=True))
        print(salaries_in_rur_by_cities)

        x = list(salaries_in_rur_by_cities.keys())[:10]
        y = list(salaries_in_rur_by_cities.values())[:10]

        print(x)
        print(y)
        fig, ax = plt.subplots()

        ax.bar(range(0, len(x)), y)

        ax.set_facecolor('seashell')

        fig.set_facecolor('floralwhite')
        fig.set_figwidth(12)
        fig.set_figheight(16)

        plt.xticks(ticks=range(0, len(x)), labels=x, rotation="vertical")
        plt.savefig('C:\\Users\\TastePate\\PycharmProjects\\Database\\VacanciesProject\\templates\\main\\resources\\salary_by_cities_histogram.png')
        plt.show()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")