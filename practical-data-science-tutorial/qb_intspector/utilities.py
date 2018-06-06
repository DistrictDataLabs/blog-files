# Author: Linwood Creekmore
# Email: valinvescap@gmail.com
# Description:  Python script to pull content from a website (works on news stories).

# Notes
"""
23 Oct 2017: updated to include readability based on PyCon talk: https://github.com/DistrictDataLabs/PyCon2016/blob/master/notebooks/tutorial/Working%20with%20Text%20Corpora.ipynb


"""

###################################
# Standard Library imports
###################################

import re
import pytz
import datetime
from io import BytesIO

###################################
# Third party imports
###################################

import requests
import numpy as np
from newspaper import Article
from bs4 import BeautifulSoup
from readability.readability import Document as Paper
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


done = {}


def textgetter(url):
    """Scrapes web news and returns the content

    Parameters
    ----------

    url : str
        web address to news report

    Returns 
    -------
    
    answer : dict
        Python dictionary with key/value pairs for:
            text (str) - Full text of article
            url (str) - url to article
            title (str) - extracted title of article
            author (str) - name of extracted author(s)
            base (str) - base url of where article was located
            provider (str) - string of the news provider from url
            published_date (str,isoformat) - extracted date of article
            top_image (str) - extracted url of the top image for article

    """
    global done
    TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p', 'li']

    # regex for url check
    s = re.compile('(http://|https://)([A-Za-z0-9_\.-]+)')
    u = re.compile("(http://|https://)(www.)?(.*)(\.[A-Za-z0-9]{1,4})$")
    if s.search(url):
        site = u.search(s.search(url).group()).group(3)
    else:
        site = None
    answer = {}
    # check that its an url
    if s.search(url):
        if url in done.keys():
            return done[url]
            pass
        try:
            r = requests.get(url, verify=False, timeout=1)
        except:
            done[url] = "Unable to reach website."
            answer['author'] = None
            answer['base'] = s.search(url).group()
            answer['provider']=site
            answer['published_date']=None
            answer['text'] = "Unable to reach website."
            answer['title'] = None
            answer['top_image'] = None
            answer['url'] = url
            yield answer
                
        if r.status_code != 200:
            done[url] = "Unable to reach website."
            answer['author'] = None
            answer['base'] = s.search(url).group()
            answer['provider']=site
            answer['published_date']=None
            answer['text'] = "Unable to reach website."
            answer['title'] = None
            answer['top_image'] = None
            answer['url'] = url


        if len(r.content)>500:
            article = Article(url)
            article.download(input_html=r.content)
            article.parse()
            if len(article.text) >= 200:
                answer['author'] = ", ".join(article.authors)
                answer['base'] = s.search(url).group()
                answer['provider']=site
                answer['published_date'] = article.publish_date
                if isinstance(article.publish_date,datetime.datetime):
                    answer['published_date']=article.publish_date.astimezone(pytz.utc).isoformat()
                

                answer['text'] = article.text
                answer['title'] = article.title
                answer['top_image'] = article.top_image
                answer['url'] = url

                
            else:
                doc = Paper(r.content)
                data = doc.summary()
                title = doc.title()
                soup = BeautifulSoup(data, 'lxml')
                newstext = " ".join([l.text for l in soup.find_all(TAGS)])

                if len(newstext) > 200:
                    answer['author'] = None
                    answer['base'] = s.search(url).group()
                    answer['provider']=site
                    answer['published_date']=None
                    answer['text'] = newstext
                    answer['title'] = title
                    answer['top_image'] = None
                    answer['url'] = url
                else:
                    newstext = " ".join([
                        l.text
                        for l in soup.find_all(
                            'div', class_='field-item even')
                    ])
                    done[url] = newstext
                    answer['author'] = None
                    answer['base'] = s.search(url).group()
                    answer['provider']=site
                    answer['published_date']=None
                    answer['text'] = newstext
                    answer['title'] = title
                    answer['top_image'] = None
                    answer['url'] = url
        else:
            answer['author'] = None
            answer['base'] = s.search(url).group()
            answer['provider']=site
            answer['published_date']=None
            answer['text'] = 'No text returned'
            answer['title'] = None
            answer['top_image'] = None
            answer['url'] = url
            yield answer
        yield answer
        del r, data
    else:
        answer['author'] = None
        answer['base'] = s.search(url).group()
        answer['provider']=site
        answer['published_date']=None
        answer['text'] = 'This is not a proper url'
        answer['title'] = None
        answer['top_image'] = None
        answer['url'] = url
        yield answer
        