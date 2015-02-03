
import json
import unicodecsv as csv

INPATH  = "data/delicious-rss-1250k.json"
OUTPATH = "data/feeds.csv"

def transform(inpath=INPATH, outpath=OUTPATH):
    """
    Munges the data set and cleans it up for ease of use
    """
    with open(inpath, 'rU') as f:
        reader = csv.reader(f)
        reader.next()

        with open(outpath, 'w') as out:
            writer = csv.writer(out)
            for row in reader:
                writer.writerow(row)

def json_transform(inpath=INPATH, outpath=OUTPATH):
    """
    Munges JSON data
    """

    with open(inpath, 'r') as f:
        with open(outpath, 'w') as out:
            writer = csv.writer(out)

            for idx, line in enumerate(f):
                data  = json.loads(line)
                url   = data['links'][0]['href']
                user  = data['author']
                title = data['title']
                rowid = idx + 1
                date  = data['updated']

                writer.writerow((rowid,user,title,url,date))

def munge_flight_data(inpath, outpath):
    with open(inpath, 'r') as f:
        reader = csv.reader(f)
        blanks = 0
        total  = 0

        with open(outpath, 'w') as o:
            writer = csv.writer(o)

            for row in reader:
                total += 1
                blank = False
                ## Check for blanks
                for item in row[:11]:
                    if not item:
                        blank = True
                        break

                if blank:
                    blanks += 1
                    continue

                writer.writerow(row[:11])

    print "%d blanks from %d total (%0.3f%%)" % (blanks, total, float(blanks)/float(total))

def time_helper(inpath, outpath):
    """
    Convert time 2400 to 0000
    """

    with open(inpath, 'r') as f:
        reader = csv.reader(f)

        with open(outpath, 'w') as o:
            writer = csv.writer(o)

            for row in reader:

                # Time helper modification
                for idx in (5, 7):
                    if row[idx] == '2400':
                        row[idx] = '0000'

                writer.writerow(row)

if __name__ == "__main__":
    time_helper('data/ontime/flights.csv', 'data/ontime/flights-cleaned.csv')
