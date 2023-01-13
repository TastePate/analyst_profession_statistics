import sqlite3

from matplotlib import pyplot as plt

if __name__ == '__main__':
    try:
        sqlite_connection = sqlite3.connect('C:\\Users\\TastePate\\PycharmProjects\\Database\\VacanciesProject\\db.sqlite3')
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")

        sqlite_select_query = "select published_at from vacancies_vacancy"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()

        years = [i[0][:4] for i in record]
        years_to_histogram = sorted(list(set([i[0][:4] for i in record])))
        vacancies_count_by_years = [years.count(i) for i in years_to_histogram]

        x = years_to_histogram
        y = vacancies_count_by_years

        fig, ax = plt.subplots()

        ax.bar(x, y)

        ax.set_facecolor('seashell')

        fig.set_facecolor('floralwhite')
        fig.set_figwidth(12)
        fig.set_figheight(6)

        plt.xticks(x)
        plt.savefig('C:\\Users\\TastePate\\PycharmProjects\\Database\\VacanciesProject\\templates\\main\\resources\\vacancies_count_by_years.png')
        plt.show()

        print(years_to_histogram)
        print(vacancies_count_by_years)

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")