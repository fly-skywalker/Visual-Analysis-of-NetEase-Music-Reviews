import json
import pandas as pd
from tqdm import tqdm


def generate_info():
    singers_info = pd.read_csv("singers.csv")
    songs_info = pd.read_csv("songs.csv")

    print(singers_info)
    print(songs_info)

    music_info = {}

    # ---------- "全部歌手" ---------------------
    songs = set(songs_info['songid'])
    singers = set(songs_info['artistid'])
    cats = set(songs_info['catid'])
    music_info[0] = f'&nbsp 全部歌手&nbsp <br> 歌手类型数:{len(cats)}&nbsp 歌手数:{len(singers)}&nbsp 单曲数:{len(songs)}'
    print(music_info)

    # ---------- "cat" ---------------------
    cats_list1 = list(singers_info['catid'])
    cats_list = list(songs_info['catid'])
    for i, catid in enumerate(cats):
        idx = cats_list.index(catid)
        music_info[catid] = f'&nbsp {songs_info.loc[idx, "cat"]} <br> &nbsp 歌手数:{cats_list1.count(catid)}&nbsp ' \
                            f'单曲数:{cats_list.count(catid)}'

        if i < 10:
            print(f"歌手类型{i}-", f'&nbsp {songs_info.loc[idx, "cat"]} <br> &nbsp 歌手数:{cats_list1.count(catid)}&nbsp'
                               f' 单曲数:{cats_list.count(catid)}')

    # ---------- "singers" ---------------------
    singers_list = list(songs_info['artistid'])
    # print(len(singers_list))
    for i, singer_id in enumerate(singers):
        idx = singers_list.index(singer_id)
        music_info[singer_id] = f'&nbsp {songs_info.loc[idx, "artist"]} <br> &nbsp ({songs_info.loc[idx, "cat"]})' \
                                f'&nbsp 单曲数:{singers_list.count(singer_id)}'

        if i < 10:
            print(f"歌手{i}-", f'&nbsp {songs_info.loc[idx, "artist"]} <br> &nbsp ({songs_info.loc[idx, "cat"]}) '
                  f'&nbsp 歌数:{singers_list.count(singer_id)}')

    # ---------- "songs" ---------------------
    songs_list = list(songs_info['songid'])
    for i, song_id in enumerate(songs):
        idx = songs_list.index(song_id)
        music_info[song_id] = f'&nbsp 《{songs_info.loc[idx, "song"]}》 <br> &nbsp 歌手: {songs_info.loc[idx, "artist"]}' \
                              f'&nbsp({songs_info.loc[idx, "cat"]})'

        if i < 10:
            print(f"歌{i}-", f'&nbsp 《{songs_info.loc[idx, "song"]}》 <br> &nbsp 歌手: {songs_info.loc[idx, "artist"]}'
                  f'&nbsp ({songs_info.loc[idx, "cat"]})')

    with open("music_info.json", 'w', encoding="utf-8") as f:
        json.dump(music_info, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    generate_info()
