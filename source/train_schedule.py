import sys

from source.train import Train

import schedule_maker
from source.sqlwrap import DatabaseWrap

"""
Module consist implamentation class Schedule
"""


class Schedule:
    """
    Attribute database consist wrapping database with type DatabaseWrap
    :param database_name: is str, consist path to database
    Class consist 
    Attribute db: contain all data, before using call method load_database
    Attribute database: contain connection with database
    Special Method __init__,
    Method load_database for establish connection with database and load all records in list
    Method unload_database for sever connection with database and load all records in db to sqlite database
    Method insert_sort for insert sorting, 
    Method quick_sort for quick sorting,
    Method-generator get_schedule for getting format string of records
    """
    def __init__(self, database_name):
        """
        :param database_name: is str, consist path to database
        """
        self.database = DatabaseWrap(database_name)

    def load_database(self):
        """
        Establish connection with database and load all records in attribute db
        :return: None
        """
        self.database.open()
        db = self.database
        self.db = [Train(*db[i]) for i in range(db.get_size())]

    def unload_database(self, name):
        """
        Sever connection with database and load all records from db to sqlite database
        :param name: name of database
        :return:  None
        :raise raise RunrimeError if attribute db doesn't exist
        """
        try:
            self.db
        except NameError:
            raise RuntimeError('load_database must be called firstly')

        schedule_maker.make_database(name, self.db)
        self.database.close()
        self.database = DatabaseWrap(name)

    def insert_sort(self, autounload_into=None):
        """
        Implementation of insert sort
        sort attribute db via insert sor
        :param autounload_into: if consist path to file name, automatically load db in database
        :return None
        :raise raise RunrimeError if attribute db doesn't exist
        """
        try:
            self.db
        except NameError:
            raise RuntimeError('load_database must be called firstly')

        for i in range(len(self.db)-1):
            train = self.db[i]
            next_train = self.db[i+1]
            if train < next_train:
                j = i
                while j != -1 and self.db[j+1] > self.db[j]:
                    temp = self.db[j+1]
                    self.db[j+1] = self.db[j]
                    self.db[j] = temp
                    j -= 1

        if autounload_into:
            self.unload_database(autounload_into)

    def quick_sort(self, db=None, first=True, autounload_into=None):
        """
        Implamentation og quick sort,
        sort db via quick sort algorithm
        :param db: for recursion call 
        :param first: for mark first call
        :param autounload_into: if consist path to file name, automatically load db in database
        :return: None
        :raise raise RunrimeError if attribute sb doesn't exist
        """
        try:
            self.db
        except NameError:
            raise RuntimeError('load_database must be called firstly')

        if db == []:
            return []
        if first:
            db = self.db
        # Sort all records on three groups
        center = db[len(db)//2]
        left = []
        right = []
        mid = []

        for i in db:
            if i > center: left.append(i)
            elif i < center: right.append(i)
            else: mid.append(i)

        try:
            db = self.quick_sort(left, first=False)+mid+self.quick_sort(right,first=False)
        except RecursionError:
            sys.setrecursionlimit(sys.getrecursionlimit()*1.5)

        if not first: return db
        self.db = db

        if autounload_into:
            self.unload_database()

    def get_schedule(self):
        """
        Method-generator for getting format string of records
        :return: format string of records
        :raise raise RunrimeError if attribute sb doesn't exist
        """
        try:
            self.db
        except NameError:
            raise RuntimeError('load_database must be called firstly')

        for i in self.db:
            yield '{type:<10} train № {train_number:04} departs on {d_time} and will be {t_time[0]}{t_time[1]} hours {t_time[3]}{t_time[4]} minutes in travel'.format(**i.form())