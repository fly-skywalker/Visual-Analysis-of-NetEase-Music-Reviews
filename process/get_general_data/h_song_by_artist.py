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
            ul_tag = soup.find_all('ul', 'f-hide')
            ul_tag = BeautifulSoup(str(ul_tag), 'html5lib')
            items = ul_tag.find_all('li')
            return items
    except RequestException as err:
        print(err)
        pass

def write_to_csv(df, items, artist, artistid, cat, catid):

    for item in items:
        song = item.a.text
        songid = item.a['href'].replace('/song?id=', '')
        row = {'artist' : artist, 'artistid' : artistid, 'cat' : cat, 'catid' : catid, 'song' : song, 'songid' : songid}
        df.loc[len(df)] = row

def main():
    data = pd.read_csv("singers.csv", encoding = "utf-8")
    df = pd.DataFrame(columns = ['artist', 'artistid', 'cat', 'catid', 'song', 'songid'])

    for i, r in data.iterrows():
        print("reading", r['artist'], i + 1, 'of 1500')
        items = parse_html_page("https://music.163.com/artist?id=" + str(r['artistid']))
        write_to_csv(df, items, r['artist'], str(r['artistid']), r['cat'], str(r['catid']))

        time.sleep(1 + random.random() * 3)
    
    print(df)
    df.to_csv("songs.csv", encoding = "utf-8", index = False)


if __name__ == "__main__":
    main()