import sys

from source.train import Train

import schedule_maker
from source.sqlwrap import DatabaseWrap
from re import fullmatch
from collections import defaultdict
from source.hasher import *

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
    Method print_schedule for printing formatted schedule
    Method _format_record for formatting record to string
    Method linear_search for linear search in database
    Method binary_search for binary search in database
    Method convert_to_dict for add opportunity of search by key
    Method map_search for search by key
    """
    def __init__(self, database_name):
        """
        :param database_name: is str, consist path to database
        """
        self.database = DatabaseWrap(database_name)

    def __getattr__(self, item):
        if item == 'db' and 'db' not in self.__dict__:
            raise RuntimeError('load_database must be called firstly')
        if item == 'db_dict' and 'db_dict not'  in self.__dict__:
            raise RuntimeError('convert_to_dict must be called firstly')

    def load_database(self):
        """
        Establish connection with database and load all records in attribute db
        :return: None
        """
        self.database.open()
        db = self.database
        self.db = [Train(*db[i]) for i in range(len(db))]

    def unload_database(self, name=None):
        """
        Sever connection with database and load all records from db to sqlite database
        :param name: name of database or None (if doesn't want to save changes)
        :return:  None
        :raise raise RunrimeError if attribute db doesn't exist
        """
        if not name:
            self.database.close()
            return None
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

    def print_schedule(self):
        """
        Method for print in stdio format string of records
        :return: format string of records
        :raise raise RunrimeError if attribute sb doesn't exist
        """
        for i in self.db:
            print(self._format_record(i))

    @staticmethod
    def _format_record(record):
        """
        Method for getting formatted string from record
        :return: format string of records
        :raise raise RunrimeError if attribute sb doesn't exist
        """
        return '{type:<10} train № {train_number:04} departs on {d_time} and will be {t_time[0]}{t_time[1]} hours {t_time[3]}{t_time[4]} minutes in travel'.format(**record.form())

    @staticmethod
    def _verify_time_format(time):
        """
        Method raise exception while format of time is incorrect
        :param time: time for check
        :raise raise RunrimeError format of time is incorrect
        """
        if not fullmatch('\d{2}-\d{2} \d{2}:\d{2}', time):
            raise RuntimeError('Incorrect Time Format!')

    @staticmethod
    def _show_result(result):
        """
        Method for printing result in stdio
        :param result: result of search
        """
        if not result:
            print('Not found')
        else:
            for train in result:
                print(train)

    def linear_search(self, time, show=False):
        """
        Method for linear search
        :param time: for search by time in field time
        :param show: for print formatted results in stdio (if no one fits print 'Not found')
        :return: list of results
        """
        suitable = []
        self._verify_time_format(time)

        for train in self.db:
            if train.d_time == time:
                suitable.append(self._format_record(train))
        if show:
            self._show_result(suitable)
        return suitable

    @staticmethod
    def _binary_search(db, time):
        """
        Method for binary search
        :param time: for search by time in field time
        :return: list of results
        """
        suitable = []
        first = 0
        last = len(db)-1
        while first <= last:
            mid = (first+last) >> 1
            if db[mid].d_time == time:
                break
            if db[mid].d_time < time:
                last = mid-1
            else:
                first = mid+1
        else:
            # if no one found
            return suitable
        # searching first suitable train
        first = mid
        while first >= 0 and db[first].d_time == time:
            first -= 1
        first += 1
        # create list of suitable train
        while first < len(db) and db[first].d_time == time:
            suitable.append(db[first])
            first += 1
        return suitable

    def binary_search(self, time, show=False):
        """
        Method for binary search
        :param time: for search by time in field time
        :param show: for print formatted results in stdio (if no one fits print 'Not found')
        :return: list of results
        """
        self._verify_time_format(time)
        result = self._binary_search(self.db, time)
        result = list(map(Schedule._format_record, result))
        if show:
            self._show_result(result)
        return result

    def convert_to_dict(self):
        """
        Method convert_to_dict for add opportunity of search by key
        :return: 
        """
        self.db_dict = defaultdict(list)
        for train in self.db:
            self.db_dict[train.d_time].append(train)

    def map_search(self, time, show=False):
        """
        Method for search by key
        :param time: for search by time in field time
        :param show: for print formatted results in stdio (if no one fits print 'Not found')
        :return: list of results
        """
        self._verify_time_format(time)

        result = self.db_dict[time]
        suitable = list(map(self._format_record, result))
        if show:
            self._show_result(suitable)
        return suitable

    def convert_to_simple_hash_table(self):
        """
        Method convert array to hash table using simple hash function
        """
        self.hash_size = len(self.db)
        self.simple_hash_table = [[] for _ in range(self.hash_size)]
        for train in self.db:
            self.simple_hash_table[train.hash1 % self.hash_size].append(train)

    def convert_to_rs_hash_table(self):
        """
        Method convert array to hash table using rs hash function
        """
        self.hash_size = len(self.db)
        self.rs_hash_table = [[] for _ in range(self.hash_size)]
        for train in self.db:
            self.rs_hash_table[train.hash2 % self.hash_size].append(train)

    def simple_hash_search(self, time, show=False):
        """
        Method for search in to hash table by time hashing via simple hash
        :param time: for search by time in field time
        :param show: for print formatted results in stdio (if no one fits print 'Not found')
        :return: list of results
        """
        self._verify_time_format(time)
        guess = self.simple_hash_table[simple_hash(time) % self.hash_size]
        result = self._binary_search(guess, time)
        result = list(map(self._format_record, result))
        if show:
            self._show_result(result)
        return result

    def rs_hash_search(self, time, show=False):
        """
        Method for search in to hash table by time hashing via rs hash
        :param time: for search by time in field time
        :param show: for print formatted results in stdio (if no one fits print 'Not found')
        :return: list of results
        """
        self._verify_time_format(time)
        guess = self.rs_hash_table[rs(time) % self.hash_size]
        result = self._binary_search(guess, time)
        result = list(map(self._format_record, result))
        if show:
            self._show_result(result)
        return result
