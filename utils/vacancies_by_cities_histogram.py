import sqlite3

from matplotlib import pyplot as plt

if __name__ == '__main__':
    try:
        sqlite_connection = sqlite3.connect('C:\\Users\\TastePate\\PycharmProjects\\Database\\VacanciesProject\\db.sqlite3')
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")

        sqlite_select_query = "select area_name from vacancies_vacancy"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()

        areas = [i[0] for i in record]
        areas_to_histogram = dict(sorted({key: (int(areas.count(key) / len(areas) * 100)) for key in set(areas)}.items(),
                                         key=lambda item: item[1],
                                         reverse=True))

        x = list(areas_to_histogram.keys())[:10]
        y = list(areas_to_histogram.values())[:10]

        fig, ax = plt.subplots()

        ax.bar(x, y)

        ax.set_facecolor('seashell')

        plt.xticks(ticks=range(0, len(x)), labels=x, rotation="vertical")
        plt.yticks(ticks=range(0, 101, 5), labels=list(map(lambda item: str(item) + '%', range(0, 101, 5))))
        fig.set_facecolor('floralwhite')
        fig.set_figwidth(12)
        fig.set_figheight(16)
        plt.savefig('C:\\Users\\TastePate\\PycharmProjects\\Database\\VacanciesProject\\templates\\main\\resources\\vacancies_percentage_by_cities.png')
        plt.show()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")