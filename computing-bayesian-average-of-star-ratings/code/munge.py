
import os
import pandas as pd

DATA_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "data", "ml-100k"))

UDATA = os.path.join(DATA_PATH, "u.data")
UITEM = os.path.join(DATA_PATH, "u.item")

def load(path, utype):
    utype = utype.upper()

    if utype == "UDATA":
        fields  = ('user_id', 'movie_id', 'rating')#, 'timestamp')
        delimit = "\t"
        cols    = [0,1,2]
    elif utype == "UITEM":
        fields  = ('movie_id', 'title')#, 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western')
        delimit = "|"
        cols    = [0,1]
    else:
        raise TypeError("Unknown data type, '%s'" % utype)

    return pd.DataFrame(pd.read_csv(path, names=fields, sep=delimit, usecols=cols))

def merge(udata=UDATA, uitem=UITEM):
    udata = load(udata, "udata")
    uitem = load(uitem, "uitem")
    return pd.merge(udata, uitem, on="movie_id", how="left")

if __name__ == '__main__':
    reviews = merge()
    reviews.to_csv('ratings.csv', index=False)
