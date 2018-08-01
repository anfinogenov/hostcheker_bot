import json
import time
import random
import requests

def load_settings(filename="config.json"):
    with open(filename) as fin:
        settings = json.load(fin)
    return settings


def panic(s):
    with open(f"panic{int(time.time())}", "w") as fout:
        fout.write(s)
    exit(1)


# User_agents: http://www.useragentstring.com/pages/useragentstring.php?typ=Browser
# https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
# TODO: automated parsing of latest agents from links above
desktop_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36']


def random_headers():
    return {'User-Agent': random.choice(desktop_agents),
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def nothrow_get(url, **kwargs):
    try:
        r = requests.get(url, headers=random_headers(), **kwargs)
        return r
    except Exception as e:
        print(e)
        return None
