def simple_hash(value):
    """
    Simple hash function
    :param value: some string
    :return: hash of string from 0 to 4294967295
    """
    hash = 0
    for num, char in enumerate(value):
        hash += ord(char)**(num+1) % 4294967296
    return hash % 4294967296


def rs(value):
    """
    RS hash function
    :param value: some string
    :return: hash of string from 0 to 4294967295
    """
    b, a, hash = 378551, 63689, 0
    for i in value:
        hash = (hash*a+ord(i)) % 4294967296
        a *= b
    return hash % 4294967296

if __name__ == '__main__':
    from time import clock
    start = clock()
    hash1 = simple_hash('12-30 23:59')
    hash2 = simple_hash('05-12 22:13')
    print(clock()-start)
    print(hash1)
    print(hash2)
    start = clock()
    hash1 = rs('12-30 23:59')
    hash2 = rs('05-12 22:13')
    print(clock() - start)
    print(hash1)
    print(hash2)