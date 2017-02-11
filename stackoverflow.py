import time
import re
import requests
from typing import Iterable
from bs4 import BeautifulSoup

_url = 'http://stackoverflow.com/company/salary/calculator?p={}&e={}&s={}&l={}&c={}'

def _requestpage(position, experience, skill, country, with_city=0):
    req = requests.get(_url.format(position, experience, skill, country, with_city))
    time.sleep(1) # play nice with stackoverflow's servers
    
    return BeautifulSoup(req.text, 'lxml')

class SalaryCalculator:

    def get_mainstats(self):
        html = _requestpage(1, 0, 0, 0)
        positions = \
            [(el.attrs['value'], el.text) \
             for el in html.select('select#position')[0].find_all('option')]
        experiences = \
            [(el.attrs['value'],) \
             for el in html.select('select#experience')[0].find_all('option')]
        skills = \
            [(el.attrs['value'],) \
             for el in html.select('select#skill')[0].find_all('option')]
        countries = \
            [(el.attrs['value'], el.text) \
             for el in html.select('select#country')[0].find_all('option') \
             if el.attrs['value'] != '0']
        
        return (positions, experiences, skills, countries)

    def get_currencies_and_countries(self, country_values):
        """
        Gets currency and country data for a list of countries
        country_values -> Iterable[value]
        """
        
        countries = list()
        currencies = dict()
        
        for val in country_values:
            html = _requestpage(1, 0, 0, val)
            curr_name = html.find_all('p', class_='currency-label')[0].text.strip()
            curr_symb = re.search(r'[^\s\.,\d]+', html.find_all('div', class_='salary-value')[0].text).group(0)
            currency = '{} ({})'.format(curr_name, curr_symb)
            country = [ \
                html.select('select#country')[0].find_all('option', selected=True)[0].text, \
                val, \
                1 if (len(html.select('input#city')) > 0) else 0, \
                currency]

            countries.append(country)
            currencies[currency] = [curr_name, curr_symb]
            print('{}: {}'.format(country[0], currency))
        
        return (list(currencies.values()), countries)
