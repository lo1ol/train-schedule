import optparse
import sys
import os
os.chdir('../')
from schedule_maker import make_database

from source.train_schedule import Schedule


def search(log='logs/log_collision.txt', trace=False):
    """
    Make measure of number collisions in by hash in three hash function
    Measure timing of computing 5, 10, 50, 100 and so on to 10**5 of sorted records

    :param log: path to logfile
    :param trace: flag to showing measure in standard output stream
    :return: 0 
    """
    logfile = open(log, 'w')

    for i in (int((10 ** (i // 2)) / 2) if i % 2 == 0 else (10 ** (i // 2)) for i in range(2, 15)):
        db_name = make_database(i)
        schedule = Schedule(db_name)
        schedule.load_database()
        sp_hash_number = rs_hash_number = dt_hash_number = 0
        hash_dict_sp = {}
        hash_dict_rs = {}
        hash_dict_dt = {}
        for train in schedule.db:
            sp_hash = train.hash1
            rs_hash = train.hash2
            dt_hash = train.d_time.__hash__()
            for hash, dict, n in ((sp_hash, hash_dict_sp, 1), (rs_hash, hash_dict_rs, 2), (dt_hash, hash_dict_dt, 3)):
                if hash in dict:
                    if train.d_time not in dict[hash]:
                        if n == 1:
                            sp_hash_number += 1
                        elif n == 2:
                            rs_hash_number += 1
                        else:
                            dt_hash_number += 1
                        dict[hash].append(train.d_time)
                else:
                    dict[hash] = [train.d_time]

        print('Simple  hash has on %-7s records = %-5s collisions' % (i, sp_hash_number), file=logfile)
        print('RS      hash has on %-7s records = %-5s collisions' % (i, rs_hash_number), file=logfile)
        print('Default hash has on %-7s records = %-5s collisions' % (i, dt_hash_number), file=logfile)
        if trace:
            print('Simple  hash has on %-7s records = %-5s collisions' % (i, sp_hash_number))
            print('RS      hash has on %-7s records = %-5s collisions' % (i, rs_hash_number))
            print('Default hash has on %-7s records = %-5s collisions' % (i, dt_hash_number))
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
                      default='logs/log_collision.txt')
    (options, args) = parser.parse_args(sys.argv)
    search(**options.__dict__)
