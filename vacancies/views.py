import os

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render

from utils.csv_parsers import Parser
from multiprocessing import Pool
from django.conf import settings
import django
from vacancies.models import Vacancy


def index(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'main/index.html', {"vacancies": vacancies})


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
