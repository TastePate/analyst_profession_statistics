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

