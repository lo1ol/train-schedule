import optparse
import sys
import os
os.chdir('../')
from random import randint
from time import clock
from source.train_schedule import Schedule


def hash_search(log='logs/log_hash.txt', trace=False):
    """
    Make measure of three algorithms of search in hash table and make log file according this measure
    Measure timing of computing 5, 10, 50, 100 and so on to 10**5 of sorted records

    :param log: path to logfile
    :param trace: flag to showing measure in standard output stream
    :return: 0 
    """
    logfile = open(log, 'w')

    for i in (int((10 ** (i // 2)) / 2) if i % 2 == 0 else (10 ** (i // 2)) for i in range(2, 15)):
        db_name = 'results\quick_sort_schedule%s.db' % i
        schedule = Schedule(db_name)
        schedule.load_database()
        simple_hash_time = rs_hash_time = map_time = 0
        schedule.convert_to_dict()
        schedule.convert_to_simple_hash_table()
        schedule.convert_to_rs_hash_table()
        for _ in range(100):
            time = randint(0, 1439)
            month = randint(1, 12)
            day = randint(1, 30)
            time = "%02d-%02d %02d:%02d" % (month, day, time // 60, time % 60)

            start = clock()
            schedule.simple_hash_search(time)
            simple_hash_time += clock() - start

            start = clock()
            schedule.rs_hash_search(time)
            rs_hash_time += clock() - start

            start = clock()
            schedule.map_search(time)
            map_time += clock() - start
        print('Simple  search on %-7s records = %-22s sec' % (i, simple_hash_time / 100), file=logfile)
        print('RS      search on %-7s records = %-22s sec' % (i, rs_hash_time / 100), file=logfile)
        print('Default search on %-7s records = %-22s sec' % (i, map_time / 100), file=logfile)
        if trace:
            print('Simple  search on %-7s records = %-22s sec' % (i, simple_hash_time / 100))
            print('RS      search on %-7s records = %-22s sec' % (i, rs_hash_time / 100))
            print('Default search on %-7s records = %-22s sec' % (i, map_time / 100))
        schedule.unload_database()
        print('-' * 50, file=logfile)
        if trace:
            print('-' * 50)
        logfile.flush()

    logfile.close()
    return 0


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-t', '--trace', action='store_true',
                      help='Trace the measure in standard output, default is False', default=False)
    parser.add_option('-l', '--log', type='string', help='Logging measure in to FIlE, default in logs/log_hash.txt',
                      default='logs/log_hash.txt')
    (options, args) = parser.parse_args(sys.argv)
    hash_search(**options.__dict__)
