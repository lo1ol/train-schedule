import sqlite3

"""
Module contains class DatabaseWrap
"""


class DatabaseWrap:
    """
    :argument database_name:
    Attribute database_name
    Attribute connection contain connect with database
    Attribute cursor conatin cursor with database
    2 Special-methods for index operator
    Methods open, clods and getsize
    """
    def __init__(self, database_name):
        """
        :param database_name: must contain database name if database doesn't exist make new
        """
        self.database_name = database_name

    def __getitem__(self, item):
        """
        Provide access to database
        :param item: is id-1 of record, which return
        :return: tuple contain record with id == item+1 (without id)
        """
        cmd_select = """SELECT * FROM schedule WHERE id = %s"""
        self.cursor.execute(cmd_select % (item+1))
        return self.cursor.fetchone()[1:]

    def __setitem__(self, key, value):
        """
        Replace or make new record with id == key + 1 with values == value in database 
        :param key: is id-1
        :param value: tuple (train_number, type_of_train, departure_time, travel_time)
        :return: None
        """
        cmd_replace = """REPLACE INTO schedule (id, train_number, type_of_train, departure_time, travel_time)
                        VALUES ({0}, {1}, "{2}", "{3}","{4}") """
        self.cursor.execute(cmd_replace.format(key+1, *value))

    def __len__(self):
        """
        :return: count of records in database
        """
        self.cursor.execute("SELECT COUNT(*) FROM schedule")
        return self.cursor.fetchone()[0]

    def close(self):
        """
        Close connection with database and commit changes
        :return: None
        """
        self.connection.commit()
        self.cursor.close()

    def open(self):
        """
        Open connection with database and commit changes
        and put in attribute connection connection with database
        and in attribute cursor -- cursor
        :return: None
        """
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
