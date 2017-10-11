import random
import sqlite3


def make_database(name, db=None):
    """
        Make database on storage
        Record is id, train number, type, depart time, travel time
        
        :param:name : int if want to get *number* random records
                      or str, that consist path to database file
        :param:db: None, if set name with type int. Further get value of name
                      db, if want to get database store records in db  
        :return: -> name of created db
        
        If name is number and db is None create number of random records and return ""./data/random_schedule{name}.db
        If name is string and db is number, create number of random records and return name
        If name is string and db is list of records, return database with with records (with keeping order) and return name
    """
    if isinstance(name, int):
        db = name
        name = './data/random_schedule%s.db' % db
    if not db:
        raise RuntimeError('Expected number if records')

    connection = sqlite3.connect(name)
    cursor = connection.cursor()
    try:
        cursor.execute('DROP TABLE schedule;')
    except sqlite3.OperationalError:
        pass

    cmd_make_table = """
    CREATE TABLE schedule(
    id INTEGER PRIMARY KEY,
    train_number INTEGER,
    type_of_train VARCHAR(9),
    departure_time TIME,
    travel_time TIME
    )
    """
    cursor.execute(cmd_make_table)

    cmd_insert_field = """
    INSERT INTO schedule (id, train_number, type_of_train, departure_time, travel_time)
    VALUES (NULL, {train_number},"{type}", "{d_time}", "{t_time}")"""

    # Make database with records
    if isinstance(db, list):
        for train in db:
            cursor.execute(cmd_insert_field.format(**train.form()))
        connection.commit()
        connection.close()
        return name

    # Create random records and set in database
    for i in range(db):
        type = random.choice(['Express', 'Passenger'])
        n = random.randint(0, 1439)
        d_time = "%02d:%02d" % (n//60, n%60)
        if type == 'Express':
            n = random.randint(360, 540)
            t_time = "%02d:%02d" % (n//60, n%60)
        else:
            n = random.randint(480, 720)
            t_time = "%02d:%02d" % (n//60, n%60)

        cursor.execute(cmd_insert_field.format(train_number=i, type=type, d_time=d_time, t_time=t_time))

    connection.commit()
    connection.close()
    return name


if __name__ == '__main__':
    # For testing
    make_database(10**4)