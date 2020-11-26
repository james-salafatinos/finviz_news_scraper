from bs4 import BeautifulSoup as soup
import pandas as pd
import requests
import re, string
from nltk.corpus import stopwords
import nltk
import pickle
import time
import random
import datetime
from os import path
import sys
nltk.download('stopwords')
sys.setrecursionlimit(30000)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}

def save_obj(obj, name):
    with open("data/obj/" + name + ".pkl", "wb") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open("data/obj/" + name + ".pkl", "rb") as f:
        return pickle.load(f)


def get_page(url):
    content = requests.get(url, headers=HEADERS).text
    parsed = soup(content, "html.parser")
    parsed_news_block = parsed.findAll("tr", {"class": "nn"})
    return parsed_news_block


def parse_finviz_page(page):
    news_titles = []
    news_links = []
    for news_item in page:
        news_titles.append(news_item.findAll("a")[0].contents)
        news_links.append(news_item.findAll("a", href=True)[0]["href"])
    return news_titles, news_links


def to_df(titles, links):
    date_str = str(datetime.datetime.now().date())
    df = pd.DataFrame(list(zip(titles, links)))
    date_to_add = [date_str] * len(df)
    df["date"] = date_to_add
    return df


def write_to_csv(df, news_vocab=None):
    date_str = str(datetime.datetime.now().date())
    if news_vocab:
        df.to_csv(f"news_vocab/{date_str}.csv")
    else:
        df.to_csv(f"data/{date_str}.csv")
    return None


def scrape(url):
    df = to_df(*parse_finviz_page(get_page(url)))
    df.columns = ["title", "agency", "date"]
    write_to_csv(df)
    return df


def read(fp=None):
    if fp:
        df = pd.read_csv(fp)
    date_str = str(datetime.datetime.now().date())
    return pd.read_csv(f"data/{date_str}.csv")


def parse_news_article(link):
    content = requests.get(link, headers=HEADERS).text
    parsed = soup(content, "html.parser")
    return parsed.get_text(" ")


def clean_doc(doc):
    tokens = doc.split()
    re_punc = re.compile("[%s]" % re.escape(string.punctuation))
    tokens = [re_punc.sub("", w) for w in tokens]
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if len(word) > 4]
    tokens = [word.lower() for word in tokens]
    stop_words = set(stopwords.words("english"))
    tokens = [w for w in tokens if not w in stop_words]
    return tokens


def iterate_over_links(df, req_limit=1000):
    vocab = {}
    reqs = min(req_limit, len(df))

    for i, news_link in enumerate(df["agency"]):
        exception_counter = 0
        if i > req_limit:
            break
        try:
            vocab[i] = clean_doc(parse_news_article(news_link))
            # print('Success: ', news_link)

            if i % 10 == 0:
                print("Request: {}/{}-|-{}".format(i, reqs, df.iloc[i, 1]))
        except Exception as e:
            # print('Fail: ',news_link)
            r = random.randint(5, 10)
            time.sleep(r)
            vocab[i] = "#NA"
            exception_counter += 1
            if exception_counter > 5:
                continue
            print(e)
    return vocab


def get_vocab(df, redo=False):
    date_str = str(datetime.datetime.now().date())
    if (path.exists(f"data/obj/{date_str}.pkl")) & (not redo):
        return load_obj(date_str)
    else:
        print("Starting news scrape... ~2 minutes required")
        vocabulary = iterate_over_links(df)
        df["vocab"] = list(vocabulary.values())
        #save_obj(df, date_str)
        df.to_pickle(f'data/obj/{date_str}')
        return df

