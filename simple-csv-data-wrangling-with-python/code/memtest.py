import csv
import uuid
import time
import random
import codecs

from collections import namedtuple
from datetime import datetime, timedelta

def load_names(path):
    with codecs.open('names.txt', 'r', 'utf8') as data:
        for line in data:
            yield line.strip()

def random_date(start=datetime(1980, 1, 1), end=datetime.now()):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def generate_record():
    names = list(load_names())
    return {
        'name': random.choice(names),
        'uuid': str(uuid.uuid1()),
        'page': random.randint(1, 10000),
        'lat': random.random()*180 - 90,
        'lng': random.random()*360 - 180,
        'date': random_date().strftime('%Y-%m-%dT%H:%M:%S')
    }

Record = namedtuple('Record', ('uuid', 'name', 'date', 'page', 'lat', 'lng'))

if __name__ == '__main__':
    fields  = ('uuid', 'name', 'date', 'page', 'lat', 'lng')
    records = []

    start = time.time()
    with open('../data/testdata.csv', 'rU') as data:
        # reader = csv.DictReader(data, fields)
        # for row in reader:
        reader = csv.reader(data)
        for row in map(Record._make, reader):
            records.append(row)


    finit = time.time()
    delta = finit - start
    print "Read took %0.3f seconds" % delta

    v = input("Ready? ")
