### from https://github.com/zyingzhou/music163-spiders
### modified by hyh

# -*- coding: utf-8 -*-
import requests
import csv
from bs4 import BeautifulSoup
from requests import RequestException
import time

import numpy as np
import pandas as pd

import random


def parse_html_page(url):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             'Chrome/66.0.3359.181 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200 and r.text:
            r.encoding = 'utf-8'
            html = r.text
            # <ul class="m-cvrlst m-cvrlst-5 f-cb" id="m-artist-box">
            soup = BeautifulSoup(html, 'html5lib')
            ul_tag = soup.find_all('ul', 'm-cvrlst m-cvrlst-5 f-cb')
            ul_tag = BeautifulSoup(str(ul_tag), 'html5lib')
            items = ul_tag.find_all('li')
            return items
    except RequestException as err:
        print(err)
        pass

def write_to_csv(df, items, cat, catid):

    for item in items:
        artist = item.a['title'].replace('的音乐', '')
        artistid = item.a['href'].replace('/artist?id=', '')
        row = {'artist' : artist, 'artistid' : artistid, 'cat' : cat, 'catid' : catid}
        df.loc[len(df)] = row

def main():
    df = pd.DataFrame(columns=['artist','artistid','cat','catid'])
    cats = []
    cats.append(('华语男歌手', '1001'))
    cats.append(('华语女歌手', '1002'))
    cats.append(('华语组合/乐队', '1003'))
    cats.append(('欧美男歌手', '2001'))
    cats.append(('欧美女歌手', '2002'))
    cats.append(('欧美组合/乐队', '2003'))
    cats.append(('日本男歌手', '6001'))
    cats.append(('日本女歌手', '6002'))
    cats.append(('日本组合/乐队', '6003'))
    cats.append(('韩国男歌手', '7001'))
    cats.append(('韩国女歌手', '7002'))
    cats.append(('韩国组合/乐队', '7003'))
    cats.append(('其他男歌手', '4001'))
    cats.append(('其他女歌手', '4002'))
    cats.append(('其他组合/乐队', '4003'))

    for cat_i in cats:
        print("reading", cat_i)
        items = parse_html_page("https://music.163.com/discover/artist/cat?id=" + cat_i[1])
        write_to_csv(df, items, cat_i[0], cat_i[1])

        time.sleep(1 + random.random() * 3)
    print(df)
    df.to_csv("singers.csv", encoding = "utf-8", index = False)


if __name__ == "__main__":
    main()