
import os
import avro.schema
import unicodecsv as csv

from StringIO import StringIO
from avro.datafile import DataFileWriter
from avro.io import DatumWriter
from collections import namedtuple
from datetime import datetime

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_PATH = os.path.join(BASE_PATH, "data", "funding.csv")
SCHEMA    = os.path.join(BASE_PATH, "funding.avsc")

fields = ("permalink","company","numEmps", "category","city","state","fundedDate", "raisedAmt","raisedCurrency","round")

class FundingRecord(namedtuple('FundingRecord_', fields)):

    @classmethod
    def parse(klass, row):
        row = list(row)                                # Make row mutable
        row[2] = int(row[2]) if row[2] else None       # Convert "numEmps" to an integer
        row[6] = datetime.strptime(row[6], "%d-%b-%y") # Parse the "fundedDate"
        row[7] = int(row[7])                           # Convert "raisedAmt" to an integer
        return klass(*row)

    def __str__(self):
        date = self.fundedDate.strftime("%d %b, %Y")
        return "%s raised %i in round %s on %s" % (self.company, self.raisedAmt, self.round, date)

def read_funding_data(path=DATA_PATH):
    with open(path, 'rU') as data:
        data.readline()            # Skip the header
        reader = csv.reader(data)  # Create a regular tuple reader
        for row in map(FundingRecord.parse, reader):
            yield row

def parse_schema(path=SCHEMA):
    with open(path, 'r') as data:
        return avro.schema.parse(data.read())

def serialize_records(records, outpath="funding.avro"):
    schema = parse_schema()
    # with open(outpath, 'wb') as out:
    out = StringIO()
    writer = DataFileWriter(out, DatumWriter(), schema)
    for record in records:
        record = dict((f, getattr(record, f)) for f in record._fields)
        record['fundedDate'] = record['fundedDate'].strftime('%Y-%m-%dT%H:M:S')
        writer.append(record)
    return out

if __name__ == "__main__":
    out = serialize_records(read_funding_data())
    print out.getvalue()
    # print parse_schema()
