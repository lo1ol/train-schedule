import optparse
import sys
from time import clock

from schedule_maker import make_database
from source.train_schedule import Schedule


def main(log='log.txt', trace=False):
    """
    Make measure of two algorithms of sort and make log file according this measure
    Before making measure ask user about confidence in action
    Measure timing of computing 5, 10, 50, 100 and so on to 10**5 of records for insert sort and 10**7 for quick sort
    For each number generate random schedule in sqlite
    
    :param log: path to logfile
    :param trace: flag to showing measure in standard output stream
    :return: 0 
    """
    if input('Are you sure? All previous database and log will be removed(Type "Yes" if sure):') == 'Yes':
        logfile = open(log, 'w')

        for i in (int((10**(i//2))/2) if i % 2 == 0 else (10**(i//2)) for i in range(2, 15)):
            db_name = make_database(i)
            # For stop insert sort
            if i <= 10**5:
                schedule = Schedule(db_name)
                schedule.load_database()
                start = clock()
                schedule.insert_sort()
                print('Insert sort on %-7s records = %-22s sec' % (i, clock() - start), file=logfile)
                if trace:
                    print('Insert sort on %-7s records = %-22s sec' % (i, clock() - start))
                schedule.unload_database('results/insert_sort_schedule%s.db' % i)
            else:
                print('Insert sort on %-7s records = %-22s sec' % (i, 'more then 3 hours'), file=logfile)
                if trace:
                    print('Insert sort on %-7s records = %-22s sec' % (i, 'more then 3 hours'))
            logfile.flush()
            schedule = Schedule(db_name)
            schedule.load_database()
            start = clock()
            schedule.quick_sort()
            print('Quick  sort on %-7s records = %-22s sec' % (i, clock() - start), file=logfile)
            if trace:
                print('Quick  sort on %-7s records = %-22s sec' % (i, clock() - start))
            schedule.unload_database('results/quick_sort_schedule%s.db' % i)
            print('-'*50, file=logfile)
            if trace:
                print('-' * 60)
            logfile.flush()
            i = int(i*3.74)

        logfile.close()
        return 0

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-t', '--trace', action='store_true', help='Trace the measure in standard output, default is False',default =False)
    parser.add_option('-l', '--log', type='string', help='Logging measure in to FIlE, default in log.txt', default='log.txt')
    (options, args) = parser.parse_args(sys.argv)
    main(**options.__dict__)
