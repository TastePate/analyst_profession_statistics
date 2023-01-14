import os

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render

from utils.csv_parsers import Parser
from multiprocessing import Pool

from utils.helper import get_salary_by_years, get_vacancies_by_year, get_vacancies_by_cities, get_salaries_by_city, \
    get_top_skills_by_years_lazily
from vacancies.models import Vacancy


def index(request):
    return render(request, 'main/index.html')

def demand(request):
    salary_by_years = get_salary_by_years(Vacancy)
    vacancies_by_years = get_vacancies_by_year(Vacancy)
    return render(request, 'main/demand.html', {'salary_by_years': salary_by_years,
                                                'vacancies_by_year': vacancies_by_years})

def geography(request):
    vacancies_by_cities = get_vacancies_by_cities(Vacancy)
    salaries_by_cities = get_salaries_by_city(Vacancy)
    return render(request, 'main/geography.html', {'vacancies_by_cities': vacancies_by_cities,
                                                   'salaries_by_cities': salaries_by_cities})

def skills(request):
    skills_count = get_top_skills_by_years_lazily(Vacancy)
    return render(request, 'main/skills.html',
                  {'years': list(map(lambda i: [str(i), f"resources/top_skills_by_{i}_year.png", skills_count[i-2015]],
                                     range(2015, 2023)))})

def main(request):
    return render(request, 'main/main.html')

def last_vacancies(request):
    return render(request, 'main/last_vacancies.html')


def create(request):
    if request.method == "POST":
        vacancy = Vacancy()
        vacancy.name = request.POST.get("name")
        vacancy.age = request.POST.get("age")
        vacancy.save()
    return HttpResponseRedirect("/")


# изменение данных в бд
def edit(request, id):
    try:
        vacancy = Vacancy.objects.get(id=id)

        if request.method == "POST":
            vacancy.name = request.POST.get("name")
            vacancy.age = request.POST.get("age")
            vacancy.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "main/index.html", {"vacancy": vacancy})
    except Vacancy.DoesNotExist:
        return HttpResponseNotFound("<h2>vacancy not found</h2>")


def delete(request, id):
    try:
        vacancy = Vacancy.objects.get(id=id)
        vacancy.delete()
        return HttpResponseRedirect("/")
    except Vacancy.DoesNotExist:
        return HttpResponseNotFound("<h2>vacancy not found</h2>")


def write_vacancy(vacancy: list[str]):
    Vacancy.objects.create(name=vacancy[0], key_skills=None if len(vacancy[2]) == 0 else vacancy[2],salary_from=None if len(vacancy[2]) == 0 else float(vacancy[2]),salary_to=None if len(vacancy[3]) == 0 else float(vacancy[3]),salary_currency=vacancy[4], area_name=vacancy[5], published_at=vacancy[6])


def import_data(request):
    parser = Parser("C:/Users/TastePate/Downloads/vacancies_with_skills.csv")
    data = parser.get_data_from_file()
    data.__next__()
    data = list(data)

    with Pool(4) as pool:
        pool.map(write_vacancy, data)
