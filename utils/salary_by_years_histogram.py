from decimal import Decimal
from matplotlib import pyplot as plt

from utils.helper import get_currency_coefficient_by_year

if __name__ == '__main__':
    import sqlite3
    from pycbrf.toolbox import ExchangeRates
    try:
        sqlite_connection = sqlite3.connect('C:\\Users\\TastePate\\PycharmProjects\\Database\\VacanciesProject\\db.sqlite3')
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")

        sqlite_select_query = "select salary_from, salary_to, salary_currency, published_at from vacancies_vacancy"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()

        years = sorted(list(set([i[3][:4] for i in record])))
        salaries_in_rur_by_years = []
        for year in years:
            salaries_by_year = []
            for r in record:
                current_year = r[3][:4]
                if current_year == year and r[2] != '':
                    if r[0] is None:
                        salaries_by_year.append(Decimal(r[1]) * get_currency_coefficient_by_year(int(current_year), r[2]))
                    elif r[1] is None:
                        salaries_by_year.append(Decimal(r[0]) * get_currency_coefficient_by_year(int(current_year), r[2]))
                    else:
                        salaries_by_year.append((Decimal(r[0]) * get_currency_coefficient_by_year(int(current_year), r[2]) +
                                                 Decimal(r[1]) * get_currency_coefficient_by_year(int(current_year), r[2])) / 2)
            salaries_in_rur_by_years.append(round(sum(salaries_by_year) / len(salaries_by_year), 0))
        salaries_in_rur_by_years = list(map(int, salaries_in_rur_by_years))
        years = list(map(int, years))

        x = years
        y = salaries_in_rur_by_years

        fig, ax = plt.subplots()

        ax.bar(x, y)

        ax.set_facecolor('seashell')

        fig.set_facecolor('floralwhite')
        fig.set_figwidth(12)
        fig.set_figheight(6)

        plt.xticks(x)
        plt.savefig('C:\\Users\\TastePate\\PycharmProjects\\Database\\VacanciesProject\\templates\\main\\resources\\mean_salary_by_years')
        plt.show()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
