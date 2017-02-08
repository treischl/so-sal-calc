import sqlite3
import os
from typing import Iterable, Tuple

def _readsql():
    execdir = os.path.dirname(os.path.realpath(__file__))
    sqlpath = os.path.join(execdir, 'sql')
    sqldirs = [name for name in os.listdir(sqlpath) if os.path.isdir(os.path.join(sqlpath, name))]

    sql = dict()
    for dirname in sqldirs:
        sql[dirname] = dict()
        sqlfiles = [name for name in os.listdir(os.path.join(sqlpath, dirname)) if name.endswith('.sql')]
        for fname in sqlfiles:
            with open(os.path.join(sqlpath, dirname, fname)) as fh:
                sql[dirname][os.path.splitext(fname)[0]] = fh.read()
    return sql
_sql = _readsql()
_droporder = ['Salary',
              'Country',
              'Skill',
              'Experience',
              'Position',
              'Currency']
_createorder = ['Currency',
                'Position',
                'Experience',
                'Skill',
                'Country',
                'Salary']

class Database:
    def __init__(self,
                 dbname='data.db'):
        self._dbname = dbname

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self._conn = sqlite3.connect(self._dbname)

    def close(self):
        self._conn.commit()
        self._conn.close()

    def drop_all(self):
        """
        Drops all database tables
        """

        tbl_stmts = map(lambda tbl: _sql[tbl]['drop_table'], _droporder)
        joined_script = ';'.join(tbl_stmts)
        self._conn.executescript(joined_script)

    def create_all(self):
        """
        Creates all database tables
        """
        stmts = list(map(lambda tbl: _sql[tbl]['create_table'], _createorder))
        joined_script = str.join(';', stmts)
        self._conn.executescript(joined_script)

    def reset_all(self):
        """
        Drops and recreates all database tables
        """

        self.drop_all()
        self.create_all()

    def create_positions(self, positions: Iterable[Tuple[str,int]]):
        """
        Adds rows to the Position table
        positions -> Iterable((name, value))
        """

        self._conn.executemany(_sql['Position']['insert_one'], positions)

    def read_positions(self):
        """
        Returns all rows in the Position table
        """

        return self._conn.execute(_sql['Position']['read_all']).fetchall()

    def create_experiences(self, yearsexp: Iterable[Tuple[int]]):
        """
        Adds rows to the Experience table
        yearsexp -> Iterable((years,))
        """

        self._conn.executemany(_sql['Experience']['insert_one'], yearsexp)

    def read_experiences(self):
        """
        Returns all rows in the Experience table
        """

        return self._conn.execute(_sql['Experience']['read_all']).fetchall()

    def create_skilllevels(self, skilllevels : Iterable[Tuple[float]]):
        """
        Adds rows to the Skill table
        skilllevels -> Iterable((level))
        """

        self._conn.executemany(_sql['Skill']['insert_one'], skilllevels)

    def read_skilllevels(self):
        """
        Returns all rows in the Skill table
        """

        return self._conn.execute(_sql['Skill']['read_all']).fetchall()

    def create_countries(self, countries: Iterable[Tuple[str, int, int]]):
        """
        Adds rows to the Country table
        countries -> Iterable((name, value, currency_id))
        """

        self._conn.executemany(_sql['Country']['insert_one'], countries)
            
    def read_countries(self):
        """
        Returns all rows in the Country table
        """

        return self._conn.execute(_sql['Country']['read_all']).fetchall()
            
    def create_salaries(self, salaries: Iterable[Tuple[int, int, int, int, int, int]]):
        """
        Adds or replaces rows to/in the Salary table
        salaries -> Iterable((country_id, pos_id, exp_id, skill_id, with_city, amount))
        """

        self._conn.executemany(_sql['Salary']['insert_one'], salaries)
    
    def read_salaries(self):
        """
        Returns all rows in the Salary table
        """

        return self._conn.execute(_sql['Salary']['read_all']).fetchall()

    def populate_salaries(self):
        """
        Populates the Salary table with all possible salary combinations.
        Existing rows are ignored, not replaced.
        """

        self._conn.execute(_sql['Salary']['populate_table'])