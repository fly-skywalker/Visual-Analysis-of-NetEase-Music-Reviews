import json

import pandas as pd

tree = []
tree.append({'Id': '0', 'text': '全部歌手', 'nodes': []})

tree[0]['nodes'].append({'Id': '1001', 'text': '华语男歌手', 'nodes': []})
tree[0]['nodes'].append({'Id': '1002', 'text': '华语女歌手', 'nodes': []})
tree[0]['nodes'].append({'Id': '1003', 'text': '华语组合/乐队', 'nodes': []})
tree[0]['nodes'].append({'Id': '2001', 'text': '欧美男歌手', 'nodes': []})
tree[0]['nodes'].append({'Id': '2002', 'text': '欧美女歌手', 'nodes': []})
tree[0]['nodes'].append({'Id': '2003', 'text': '欧美组合/乐队', 'nodes': []})
tree[0]['nodes'].append({'Id': '6001', 'text': '日本男歌手', 'nodes': []})
tree[0]['nodes'].append({'Id': '6002', 'text': '日本女歌手', 'nodes': []})
tree[0]['nodes'].append({'Id': '6003', 'text': '日本组合/乐队', 'nodes': []})
tree[0]['nodes'].append({'Id': '7001', 'text': '韩国男歌手', 'nodes': []})
tree[0]['nodes'].append({'Id': '7002', 'text': '韩国女歌手', 'nodes': []})
tree[0]['nodes'].append({'Id': '7003', 'text': '韩国组合/乐队', 'nodes': []})
tree[0]['nodes'].append({'Id': '4001', 'text': '其他男歌手', 'nodes': []})
tree[0]['nodes'].append({'Id': '4002', 'text': '其他女歌手', 'nodes': []})
tree[0]['nodes'].append({'Id': '4003', 'text': '其他组合/乐队', 'nodes': []})

catmap = {1001: 0, 1002: 1, 1003: 2, 2001: 3, 2002: 4, 2003: 5, 6001: 6, 6002: 7, 6003: 8, 7001: 9, 7002: 10, 7003: 11, 4001: 12, 4002: 13, 4003: 14}

data = pd.read_csv("data/songid/songs.csv", encoding = 'utf-8')

print(data)

artistid_buf = -1

for _, r in data.iterrows():
    artistid = r['artistid']
    songid = r['songid']
    song = r['song']
    catid = r['catid']

    if artistid != artistid_buf:
        ### new artist
        artist = r['artist']
        artistid_buf = artistid
        tree[0]['nodes'][catmap[catid]]['nodes'].append({'Id': str(artistid), 'text': artist, 'nodes': [{'Id': str(songid), 'text': song}]})
    else:
        ### existed artist
        tree[0]['nodes'][catmap[catid]]['nodes'][-1]['nodes'].append({'Id': str(songid), 'text': song})




with open('../data/songid/song_tree.json', 'w', encoding='utf-8') as f:
    json.dump(tree, f, indent = 4, ensure_ascii = False)


### 需要手动修复！！！！否则json无法读取！！！！