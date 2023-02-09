import os
import pandas as pd

songs_info = pd.read_csv("songid/songs.csv")
print(songs_info.shape)
songs_id = list(songs_info['songid'])
# print(songs_id)

artists = set()
for root, _, files in os.walk("songdata"):
    get_n = 0
    for i, file in enumerate(files):
        song_id = int(file.replace('.csv', ''))
        song_idx = songs_id.index(song_id)
        if songs_info.loc[song_idx, 'catid'] == 1002:
            pass
            print(i, song_idx, songs_info.loc[song_idx, 'song'], songs_info.loc[song_idx, 'artist'])
        # if songs_info.loc[song_idx, 'catid'] == 1001:
        # if songs_info.loc[song_idx, 'cat'] == "日本女歌手":
        # if songs_info.loc[song_idx, 'artist'] == "Taylor Swift":
        # if "Reol" in songs_info.loc[song_idx, 'artist']:
        #     artists.add(songs_info.loc[song_idx, 'artist'])
        # if songs_info.loc[song_idx, 'artist'] == '刘德华':

        # if i == 962:
        #     print(i, '---------------------------------------')
        #     print(songs_info.loc[songs_id.index(song_id)])
        #     get_n += 1
        #     print(get_n)
        #     if get_n >= 10:
        #         break

        if '苏州河' in songs_info.loc[song_idx, 'song']:
            print(i, '---------------------------------------')
            print(songs_info.loc[songs_id.index(song_id)])
            get_n += 1
            print(get_n)
            if get_n >= 10:
                break
