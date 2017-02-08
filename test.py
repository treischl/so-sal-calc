import itertools
import requests
from bs4 import BeautifulSoup
from data import Database

r = requests.get('http://stackoverflow.com/company/salary/calculator')
s = BeautifulSoup(r.text, 'lxml')

with Database('debug.db') as db:
    db.reset_all()

    pos_vals = [(el.text, int(el.attrs['value'])) \
                for el in s.select('select#position')[0].find_all('option')]
    db.create_positions(pos_vals)
    pos = db.read_positions()
    print(len(pos))

    exp_vals = [(int(el.attrs['value']),) \
                for el in s.select('select#experience')[0].find_all('option')]
    db.create_experiences(exp_vals)
    exp = db.read_experiences()
    print(len(exp))

    skl_vals = [(float(el.attrs['value']),) \
                for el in s.select('select#skill')[0].find_all('option')]
    db.create_skilllevels(skl_vals)
    skl = db.read_skilllevels()
    print(len(skl))

    cnt_vals = [(el.text, int(el.attrs['value']), 1 if el.text in ['United Kingdom', 'United States'] else 0, None) \
                for el in s.select('select#country')[0].find_all('option') \
                if el.attrs['value'] != '0']
    db.create_countries(cnt_vals)
    cnt = db.read_countries()
    print(len(cnt))

    db.populate_salaries()
    sal = db.read_salaries()
    print(len(sal))