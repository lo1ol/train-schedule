from train_schedule import Schedule
from time import clock


def sort_db():
    """
    Sort database, which path input from stdin
    :return: 0 
    """
    database = input('Input batadase name: ')
    type= input('Type of sort(quick/insert): ')
    schedule = Schedule(database)
    schedule.load_database()
    start = clock()
    if type == 'quick':
        schedule.quick_sort()
        print('Time of sorting %s' % (clock() - start))
    elif type == 'insert':
        schedule.insert_sort()
        print('Time of sorting %s' % (clock() - start))
    else:
        print('Unknown Sort!')
    sorted_data_base = input('Input name for out file or type "No" to continue without saving: ')
    if sorted_data_base != "No":
        schedule.unload_database(sorted_data_base)
    return 0

if __name__ == "__main__":
    sort_db()
