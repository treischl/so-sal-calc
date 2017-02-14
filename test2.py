from data import Database
from stackoverflow import SalaryCalculator

salcalc = SalaryCalculator()

with Database('debug.db') as db:
    unpulled_salaries = db.read_unpulled_salaries()

    for sal in unpulled_salaries:
        amt = salcalc.pull_salary(sal[1], sal[2], sal[3], sal[4], sal[5])
        db.update_pulled_salary(sal[0], amt)
