import optparse
import sys
from time import clock
from random import randint
from source.train_schedule import Schedule


def search_test(log='log_search.txt', trace=False):
    """
    Make measure of two algorithms of search and make log file according this measure
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
        linear_sum = binary_sum = map_sum = 0
        schedule.convert_to_dict()
        for _ in range(100):
            n = randint(0, 1439)
            time = "%02d:%02d" % (n // 60, n % 60)

            start = clock()
            schedule.linear_search(time)
            linear_sum += clock() - start

            start = clock()
            schedule.binary_search(time)
            binary_sum += clock() - start

            start = clock()
            schedule.map_search(time)
            map_sum += clock() - start

        print('Linear search on %-7s records = %-22s sec' % (i, linear_sum / 100), file=logfile)
        print('Binary search on %-7s records = %-22s sec' % (i, binary_sum / 100), file=logfile)
        print('Map    search on %-7s records = %-22s sec' % (i, map_sum / 100), file=logfile)
        if trace:
            print('Linear search on %-7s records = %-22s sec' % (i, linear_sum / 100))
            print('Binary search on %-7s records = %-22s sec' % (i, binary_sum / 100))
            print('Map search    on %-7s records = %-22s sec' % (i, map_sum / 100))
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
    parser.add_option('-l', '--log', type='string', help='Logging measure in to FIlE, default in log_search.txt',
                      default='log_search.txt')
    (options, args) = parser.parse_args(sys.argv)
    search_test(**options.__dict__)
