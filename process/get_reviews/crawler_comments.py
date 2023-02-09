# coding = utf-8

from Crypto.Cipher import AES
import base64
import requests

import pandas as pd
import math
import argparse
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import os
import time


def get_args_parser():
    parser = argparse.ArgumentParser('COMMENTS', add_help=False)

    # task
    parser.add_argument('--task', default='', type=str)
    
    # generate file
    parser.add_argument('--catid', default=0, type=int)
    parser.add_argument('--songs_num_per_artist', default=10, type=int)
    parser.add_argument('--srcfile', default='songs', type=str)
    parser.add_argument('--desfile', default='temp', type=str)
    # parser.add_argument('--songsfile', default='songs', type=str)
    parser.add_argument('--songsfile', default='华语男歌手10', type=str)
    
    # thread
    parser.add_argument('--usethread', action='store_true')
    parser.add_argument('--threadnum', default=2, type=int)

    # crawler outer control
    parser.add_argument('--onlyhot', action='store_true')
    parser.add_argument('--overload', action='store_true')
    parser.add_argument('--output_dir', default='', type=str)

    return parser


def generate_target_songs(args):
    songs_info = pd.read_csv(f"songid/{args.srcfile}.csv", encoding='utf-8')
    songs_info['artist_songs_idx'] = pd.Series(dtype='str')
    songs_num = songs_info.shape[0]
    songs_info_res = []
    artists = set()
    artist = ''
    artist_songs_num = 0
    for i in range(songs_num):
        if songs_info.loc[i, 'catid'] != args.catid:
            continue
        artists.add(songs_info.loc[i, 'artist'])
        if artist != songs_info.loc[i, 'artist']:
            artist_songs_num = 1
            artist = songs_info.loc[i, 'artist']
        if artist_songs_num > args.songs_num_per_artist:
            continue
        songs_info.loc[i, 'artist_songs_idx'] = artist_songs_num
        songs_info_res.append(songs_info.iloc[i])
        artist_songs_num += 1
    print(len(songs_info_res))
    print(len(artists))
    songs_info_des = pd.DataFrame(songs_info_res)
    songs_info_des.to_csv(f"songid/{args.desfile}.csv", encoding='utf-8', index=False)


class Crawler:
    def __init__(self, args):

        # fixed params
        self.headers = {
            'Cookie': 'appver=1.5.0.75771;',
            'Referer': 'http://music.163.com/'
        }
        self.first_key = "0CoJUm6Qyw8W8jud"
        self.second_key = 16 * 'F'
        self.iv = "0102030405060708"
        self.encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e388173" \
                         "6d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f724" \
                         "9b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
        self.max_comments_num = 20020
        self.dumponce = 100

        # args
        self.args = args

        self.if_desc = True
        if self.args.usethread:
            self.if_desc = False

        # songinfo
        self.songid = 0
        self.url = ''
        self.songname = ''
        self.filepath = ''
        self.songidx = 0
        self.total = 0
        self.pages = 0

        # change with page
        self.page = 0
        self.msg = ''
        self.params = ''
        self.html = {}
        self.song_info = {}

    def get_url(self):
        self.url = f"http://music.163.com/weapi/v1/resource/comments/R_SO_4_{self.songid}/?csrf_token="

    def get_filepath(self):
        self.filepath = os.path.join(self.args.output_dir, f"{self.songname}.json")

    def renew_msg(self):
        self.msg = '{"offset":' + str(self.page - 1) + ',"total":"True","limit":"20","csrf_token":""}'

    def renew_params(self):
        h_encText = self.AES_encrypt(self.msg, self.first_key, self.iv)
        self.params = self.AES_encrypt(h_encText.decode(), self.second_key, self.iv)

    def get_json(self):
        data = {
            "params": self.params,
            "encSecKey": self.encSecKey
        }
        response = requests.post(self.url, headers=self.headers, data=data)
        return response.content

    @staticmethod
    def AES_encrypt(text, key, iv):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        encrypt_text = encryptor.encrypt(text.encode())
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text

    @staticmethod
    def timeStamp(timeNum):
        timeStamp = float(timeNum / 1000)
        timeArray = time.localtime(timeStamp)
        reTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return reTime

    def process(self, songid, songname, songidx):
        self.songid = int(songid)
        self.get_url()
        self.songname = songname
        self.get_filepath()
        self.songidx = songidx

        self.init()
        self.step()
        t = tqdm(range(self.page, self.pages + 1))
        for self.page in t:
            self.step()
            self.get_comments()
            if self.if_desc:
                t.set_description(
                    f"正在获取第{songidx}首歌《{songname}》第{self.page}页..."
                    f"(共{self.pages}页)（共{self.args.songs_num}首）"
                )
            if self.page % self.dumponce == 1:
                # print('---Dump...')
                # time.sleep(2 + random.random())
                self.song_info['comments_num'] = len(self.song_info['comments'])
                if self.song_info['comments_num'] == self.max_comments_num:
                    self.song_info['finished'] = True
                    self.dump()
                    return
                self.dump()
        self.song_info['comments_num'] = len(self.song_info['comments'])
        if self.page == self.pages:
            self.args.finished = True
            self.song_info['finished'] = True
        self.dump()

    def init(self):
        if os.path.exists(self.filepath) and not self.args.overload:
            self.load()
            self.page = self.song_info['page'] + 1
            self.pages = self.song_info['pages_num']
        else:
            self.page = 1
            self.song_info = {}
            self.step()
            self.total = self.html['total']
            self.pages = math.ceil(self.total / 20)
            self.song_info['songname'] = self.songname
            self.song_info['songid'] = self.songid
            self.song_info['filepath'] = self.filepath
            self.song_info['page'] = 0
            self.song_info['finished'] = False
            self.song_info['pages_num'] = self.pages
            self.song_info['hot_comments_num'] = 0
            self.song_info['comments_num'] = 0
            self.song_info['hot_comments'] = []
            self.get_hotcomments()
            self.song_info['hot_comments_num'] = len(self.song_info['hot_comments'])
            self.song_info['comments'] = []
            if self.args.onlyhot:
                print(f"正在获取第{self.songidx}首歌《{self.songname}》热门评论...")
                self.song_info['finished'] = True
                self.dump()
                exit()
            self.dump()

    def step(self):
        self.renew_msg()
        self.renew_params()
        self.html = json.loads(self.get_json())

    def get_hotcomments(self):
        # 精彩评论
        # 键在字典中则返回True, 否则返回False
        if 'hotComments' in self.html:
            n = 0
            for item in self.html['hotComments']:
                self.song_info['hot_comments'].append({
                    'user': item['user']['nickname'],
                    'content': item['content'],
                    'likedCount': item['likedCount'],
                    't': item['time']
                })
                n += 1
            # print(f"hotComments num = {n}.")

    def get_comments(self):
        for item in self.html['comments']:
            self.song_info['comments'].append({
                'user': item['user']['nickname'],
                'content': item['content'],
                'likedCount': item['likedCount'],
                't': item['time']
            })
        self.song_info['page'] = self.page

    def dump(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.song_info, f, indent=4, ensure_ascii=False)

    def load(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.song_info = json.load(f)
            
            
def spider_comments(args):
    songs_info = pd.read_csv(f"songid/{args.songsfile}.csv", encoding='utf-8')
    songs_num = songs_info.shape[0]
    args.songs_num = songs_num
    print(f"\"{args.songsfile}\"共有{args.songs_num}首歌!")
    args.comments_type = ''
    if args.onlyhot:
        args.comments_type = '热门'

    if not args.output_dir:
        if args.onlyhot:
            args.output_dir = "songs_hot_comments/"
        else:
            args.output_dir = "songs_comments/"
    os.makedirs(args.output_dir, exist_ok=True)

    if args.usethread:
        threadPool = ThreadPoolExecutor(max_workers=args.threadnum, thread_name_prefix="WYY")

        for thread_i in range(args.threadnum):
            threadPool.submit(spider_comments_pipline, args, songs_info, thread_i, args.threadnum)
        threadPool.shutdown(wait=True)

        # threads = []
        # for thread_i in range(args.threadnum):
        #     threads.append(threading.Thread(target=spider_comments_pipline,
        #                                     args=(args, songs_info, thread_i, args.threadnum)))
        # for t in threads:
        #     t.setDaemon(True)
        #
        # for t in threads:
        #     t.start()
        #
        # for t in threads:
        #     t.join()

    else:
        spider_comments_pipline(args, songs_info)


def spider_comments_pipline(args, songs_info, offset=0, step=1):
    crawler = Crawler(args)
    for i in range(offset, args.songs_num, step):
        spider_comments_of_1song(crawler, songs_info, args, i)


def spider_comments_of_1song(crawler, songs_info, args, i):
    artist = songs_info.loc[i, 'artist']
    artist_songs_idx = songs_info.loc[i, 'artist_songs_idx']
    songid = songs_info.loc[i, 'songid']
    songname = songs_info.loc[i, 'song']
    songidx = i
    if not args.overload:
        filepath = os.path.join(args.output_dir, f"{songname}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                if json.load(f)['finished']:
                    print(f"第{songidx}首歌《{songname}》已完成！")
                    return
    print(f"正在获取{artist}第{artist_songs_idx}首歌《{songname}》{args.comments_type}评论...")

    while True:
        try:
            crawler.process(songid, songname, songidx)
            return
        except KeyError:
            time.sleep(1)
            print(f"WAITING...已存{crawler.song_info['comments_num']}条评论")


if __name__ == "__main__":
    
    main_args = get_args_parser().parse_args()
    print(main_args)
    if main_args.task == 'gen':
        generate_target_songs(main_args)
    else:
        spider_comments(main_args)
