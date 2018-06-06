# Author: Linwood Creekmore
# April 19 2018
# Acknowledgements: https://docs.cherrypy.org/en/latest/tutorials.html#tutorial-7-give-us-a-rest

###########################
# Standard Library imports
###########################

import time
import json
import random
import string
import sqlite3
import os, os.path
from six import string_types

###########################
# Third party imports
###########################

import cherrypy
import webbrowser
from sklearn.externals import joblib
from sklearn.base import TransformerMixin, BaseEstimator

###########################
# Custom code imports
###########################

from utilities import textgetter


# set up custom tranformer for scikit
class DenseTransformer(BaseEstimator, TransformerMixin):
    def transform(self, X, y=None, **fit_params):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self


# load the machine learning model
clf = joblib.load('models/qb_model2.pkl')

# create a database
DB_STRING = "my.db"


# base class for simple user interface
class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')


# make the endpoint
@cherrypy.expose
class StringGeneratorWebService(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        with sqlite3.connect(DB_STRING) as c:
            cherrypy.session['ts'] = time.time()
            r = c.execute("SELECT value FROM user_string WHERE session_id=?",
                          [cherrypy.session.id])

            return r.fetchone()

    def POST(
            self,
            url='http://journalstar.com/sports/huskers/football/red-report-even-split-at-quarterback-on-saturday-held-remembers/article_081cf827-b967-5a0b-acce-b59a251428c6.html'
    ):
        try:
            call = next(textgetter(url))
        except:
            with sqlite3.connect(DB_STRING) as c:
                cherrypy.session['ts'] = time.time()
                c.execute(
                    "INSERT INTO user_string VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)",
                    [
                        cherrypy.session.id, url, "NULL", "NULL", "NULL",
                        "NULL", "NULL", url, "NULL", "NULL", "NULL", "NULL"
                    ])
            return json.dumps({"answer": "Unable to reach website"})
        article = call['text']
        if isinstance(article, string_types):
            prediction = clf.predict([article])

            if prediction[0] == 0:
                answer = "is NOT about a quarterback!"
            elif prediction[0] == 1:
                answer = "IS about a quarterback"

        # we could store all this in a backend database if we wanted
        cherrypy.session['url'] = url
        cherrypy.session['title'] = call['title']
        cherrypy.session['image'] = call['top_image']
        cherrypy.session['author'] = call['author']
        cherrypy.session['date'] = call['published_date']
        cherrypy.session['text'] = call['text']
        cherrypy.session['provider'] = call['provider']
        cherrypy.session['base'] = call['base']
        cherrypy.session['prediction'] = answer
        cherrypy.session['predicted'] = prediction[0]
        call['predicted'] = str(prediction[0])
        call['answer'] = "This article {}".format(answer)

        # here is where you would store things in database
        with sqlite3.connect(DB_STRING) as c:
            cherrypy.session['ts'] = time.time()
            c.execute(
                "INSERT INTO user_string VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)",
                [
                    cherrypy.session.id, url, cherrypy.session['image'],
                    cherrypy.session['title'], cherrypy.session['author'],
                    cherrypy.session['date'], cherrypy.session['text'],
                    cherrypy.session['url'], cherrypy.session['base'],
                    cherrypy.session['provider'],
                    cherrypy.session['predicted'],
                    cherrypy.session['prediction']
                ])


#         return "This article {}".format(answer)

# if you just wanted json output
        return json.dumps(call)

    def PUT(self, another_string):
        with sqlite3.connect(DB_STRING) as c:
            cherrypy.session['ts'] = time.time()
            c.execute("UPDATE user_string SET value=? WHERE session_id=?",
                      [another_string, cherrypy.session.id])

    def DELETE(self):
        cherrypy.session.pop('ts', None)
        with sqlite3.connect(DB_STRING) as c:
            c.execute("DELETE FROM user_string WHERE session_id=?",
                      [cherrypy.session.id])


def setup_database():
    """
    Create the `user_string` table in the database
    on server startup
    """
    with sqlite3.connect(DB_STRING) as con:
        try:
            con.execute(
                "CREATE TABLE user_string (session_id, value, image varchar,title varchar, author varchar, date numeric, text varchar, url varchar unique not null,base varchar, provider varchar,predicted integer,prediction varchar )"
            )
        except:
            pass


def cleanup_database():
    """
    Destroy the `user_string` table from the database
    on server shutdown.
    """
    with sqlite3.connect(DB_STRING) as con:
        con.execute("DROP TABLE user_string")


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    cherrypy.engine.subscribe('start', setup_database)
    cherrypy.engine.subscribe('stop', cleanup_database)

    webapp = StringGenerator()
    webapp.generator = StringGeneratorWebService()
    cherrypy.quickstart(webapp, '/', conf)
