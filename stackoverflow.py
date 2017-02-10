import time
import re
import requests
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
        