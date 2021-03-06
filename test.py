import itertools
import requests
from bs4 import BeautifulSoup
from data import Database
from stackoverflow import SalaryCalculator

salcalc = SalaryCalculator()
(pos, exp, skl, cnt) = salcalc.get_mainstats()
(cur, cnt) = salcalc.get_currencies_and_countries([int(c[0]) for c in cnt])

with Database('debug.db') as db:
    db.reset_all()

    db.create_positions([(p[1], int(p[0])) for p in pos])
    pos = db.read_positions()
    print(len(pos))

    db.create_experiences([(int(e[0]),) for e in exp])
    exp = db.read_experiences()
    print(len(exp))

    db.create_skilllevels([(float(s[0]),) for s in skl])
    skl = db.read_skilllevels()
    print(len(skl))

    db.create_countries([(c[0], c[1], c[2], None) for c in cnt])
    cnt = db.read_countries()
    print(len(cnt))

    db.populate_salaries()
    sal = db.read_salaries()
    print(len(sal))
    