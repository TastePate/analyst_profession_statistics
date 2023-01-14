import sqlite3

from matplotlib import pyplot as plt

if __name__ == '__main__':
    try:
        sqlite_connection = sqlite3.connect(
            'C:\\Users\\TastePate\\PycharmProjects\\Database\\VacanciesProject\\db.sqlite3')
        cursor = sqlite_connection.cursor()
        print("База данных создана и успешно подключена к SQLite")

        sqlite_select_query = "select key_skills, published_at " \
                              "from vacancies_vacancy"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()

        years = sorted(list(set([i[1][:4] for i in record])))
        for year in years:
            skills_count = {}

            for r in record:
                if not r[0] is None and year == r[1][:4]:
                    skills = r[0].split(",")
                    for skill in skills:
                        skill = skill.strip()
                        skill = skill.upper()
                        if skill in skills_count.keys():
                            skills_count[skill] += 1
                        else:
                            skills_count[skill] = 1
            skills_count = dict(sorted(skills_count.items(), key=lambda item: item[1], reverse=True)[:10])
            if (len(skills_count) == 0):
                continue
            x = list(skills_count.keys())[:10]
            y = list(skills_count.values())[:10]

            print(x)
            print(y)
            fig, ax = plt.subplots()

            ax.bar(range(0, len(x)), y)

            ax.set_facecolor('seashell')

            fig.set_facecolor('floralwhite')
            fig.set_figwidth(12)
            fig.set_figheight(20)

            plt.xlabel("Skills")
            plt.ylabel("Count")
            plt.title("Top-10 skills by " + year)

            plt.xticks(ticks=range(0, len(x)), labels=x, rotation=90, fontsize=6)
            plt.savefig(f'C:\\Users\\TastePate\\PycharmProjects\\Database\\VacanciesProject\\templates\\main\\resources\\top_skills_by_{year}_year.png')
            plt.show()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")