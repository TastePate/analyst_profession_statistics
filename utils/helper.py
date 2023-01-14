import re
from decimal import Decimal

from pycbrf import ExchangeRates

currencies = {key: {
    'USD': int(ExchangeRates(str(key) + "-12-31")['USD'].rate) if not ExchangeRates(str(key) + "-12-31")['USD'] is None else
    int(ExchangeRates('2010-12-31')['USD'].rate),
    'UAH': int(ExchangeRates(str(key) + "-12-31")['UAH'].rate) if not ExchangeRates(str(key) + "-12-31")['UAH'] is None else
    int(ExchangeRates('2010-12-31')['UAH'].rate),
    'EUR': int(ExchangeRates(str(key) + "-12-31")['EUR'].rate) if not ExchangeRates(str(key) + "-12-31")['EUR'] is None else
    int(ExchangeRates('2010-12-31')['EUR'].rate),
    'KZT': int(ExchangeRates(str(key) + "-12-31")['KZT'].rate) if not ExchangeRates(str(key) + "-12-31")['KZT'] is None else
    int(ExchangeRates('2010-12-31')['KZT'].rate),
    'AZN': int(ExchangeRates(str(key) + "-12-31")['AZN'].rate) if not ExchangeRates(str(key) + "-12-31")['AZN'] is None else
    int(ExchangeRates('2011-12-31')['AZN'].rate),
    'UZS': int(ExchangeRates(str(key) + "-12-31")['UZS'].rate) if not ExchangeRates(str(key) + "-12-31")['UZS'] is None else
    int(ExchangeRates('2010-12-31')['UZS'].rate),
    'KGS': int(ExchangeRates(str(key) + "-12-31")['KGS'].rate) if not ExchangeRates(str(key) + "-12-31")['KGS'] is None else
    int(ExchangeRates('2010-12-31')['KGS'].rate),
    'RUR': Decimal(1),
    'BYR': Decimal(25.7)
} for key in range(2002, 2023)}

def get_currency_coefficient_by_year(year: int, currency: str):
    return currencies[year][currency]

def get_salary_by_years(vacancy):
    salary_by_years = {key: [] for key in range(2002, 2023)}
    records = vacancy.objects.values('salary_from', 'salary_to', 'salary_currency', 'published_at')
    for record in list(records):
        salary_from = Decimal(record['salary_from']) if not record['salary_from'] is None else None
        salary_to = Decimal(record['salary_to']) if not record['salary_to'] is None else None
        year = record['published_at'].year
        salary_currency = record['salary_currency']
        if not salary_currency == '':
            salary_currency = get_currency_coefficient_by_year(year, record['salary_currency']) \
                                                    if not record['salary_currency'] is None \
                                                    else None
            if salary_from is None:
                salary_by_years[year].append(salary_to * salary_currency)
            elif salary_to is None:
                salary_by_years[year].append(salary_from * salary_currency)
            else:
                salary_by_years[year].append(int((salary_from * salary_currency + salary_to * salary_currency) / 2))
    return dict({key: int(sum(value) / len(value)) for key, value in salary_by_years.items() if len(value) >= 5})

def get_vacancies_by_year(vacancy):
    records = list(map(lambda item: item['published_at'].year, vacancy.objects.values('published_at')))
    vacancies_by_years = {key: records.count(key) for key in range(2003, 2023)}
    return vacancies_by_years

def get_vacancies_by_cities(vacancy):
    records = list(map(lambda item: item['area_name'], vacancy.objects.values('area_name')))
    vacancies_by_cities = dict(sorted({key: str(round(records.count(key) / len(records) * 100, 2)) + '%' for key in set(records)}.items(),
                                 key=lambda item: float(item[1].replace('%', '')),
                                 reverse=True))
    return dict(list(vacancies_by_cities.items())[:10])

def get_salaries_by_city(vacancy):
    records = vacancy.objects.values('salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at')
    salary_by_areas = {re.sub(r'\([^()]*\)', '', key['area_name']): [] for key in records}
    for record in list(records):
        salary_from = Decimal(record['salary_from']) if not record['salary_from'] is None else None
        salary_to = Decimal(record['salary_to']) if not record['salary_to'] is None else None
        year = record['published_at'].year
        area = re.sub(r'\([^()]*\)', '', record['area_name'])
        salary_currency = record['salary_currency']
        if not salary_currency == '':
            salary_currency = get_currency_coefficient_by_year(year, salary_currency) \
                                                    if not salary_currency is None \
                                                    else None
            if salary_from is None:
                salary_by_areas[area].append(salary_to * salary_currency)
            elif salary_to is None:
                salary_by_areas[area].append(salary_from * salary_currency)
            else:
                salary_by_areas[area].append(int((salary_from * salary_currency + salary_to * salary_currency) / 2))
    return dict(sorted({key: int(sum(value) / len(value)) for key, value in salary_by_areas.items() if len(value) >= 5}.items(),
                      key=lambda item: item[1],
                      reverse=True)[:10])

def get_top_skills_by_years_lazily(vacancy):
    records = vacancy.objects.values('key_skills', 'published_at')
    r = []
    for year in range(2003, 2023):
        skills_count = {}
        for record in records:
            current_year = record['published_at'].year
            skills = record['key_skills'].split(',') if not record['key_skills'] is None else None
            if not skills is None and year == current_year:
                for skill in skills:
                    skill = skill.strip()
                    skill = skill.upper()
                    if skill in skills_count.keys():
                        skills_count[skill] += 1
                    else:
                        skills_count[skill] = 1
        skills_count = dict(sorted(skills_count.items(), key=lambda item: item[1], reverse=True)[:10])
        if len(skills_count) != 0:
            r.append(skills_count)
    return r


