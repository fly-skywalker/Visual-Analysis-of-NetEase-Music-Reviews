import os
import time

import numpy as np
import pandas as pd
from tqdm import tqdm


def timeStamp(time_num):
    time_stamp = float(time_num / 1000)
    time_array = time.localtime(time_stamp)
    re_time = time.strftime("%Y/%m/%d %H:%M:%S", time_array)
    return re_time


import json
import math


def generate_river_data():
    os.makedirs("river", exist_ok=True)
    for root, _, files in os.walk("songdata"):
        for file in tqdm(files):
            df = pd.read_csv(os.path.join(root, file))
            # timestamp = np.array(df['time'])
            # print(timestamp, type(timestamp[0]))
            # print(max(timestamp) - min(timestamp))
            # diff = max(timestamp) - min(timestamp)
            # ms_of_1day = 24 * 60 * 60 * 1000
            # print(ms_of_1day)
            # print(diff / ms_of_1day)
            #
            # min_t = timeStamp(min(timestamp))
            # max_t = timeStamp(max(timestamp))
            # print(min_t)
            # print(max_t)

            #df['time'] = df['time'].map(lambda x: timeStamp(int(x))[:10])
            df['time'] = df['time'].astype(float)
            data = df[df['ishot'] == 0]
            data = data[['time', 'label', 'likes']]

            types = 0
            for i in range(10):
                if df[df['label'] == i].shape[0] == 0:
                    types = i
                    break

            timestamp = sorted(list(set(np.array(data)[:, 0])))

            #print(timestamp)
            '''
            t_max = timestamp[-1]
            t_min = timestamp[0]
            t_slices = 100

            t_step = (t_max - t_min) / t_slices

            keys = [t_min+t_step*(m+0.5) for m in range(t_slices+1)]

            res_l = [{label: 0 for label in range(types)} for m in range(t_slices+1)]
            '''

            res = {t: {label: 0 for label in range(types)} for t in timestamp}
            

            for i in data.index:
                '''
                k = t_min
                k_i = -1
                while data.loc[i, 'time'] >= k:
                    k += t_step
                    k_i += 1

                '''
                total = 1
                res[data.loc[i, 'time']][int(data.loc[i, 'label'])] += total
                '''
                if 1:
                    res_l[k_i][int(data.loc[i, 'label'])] += 0.5 * total
                    if k_i - 1 >= 0:
                        res_l[k_i-1][int(data.loc[i, 'label'])] += 0.2 * total
                    if k_i - 2 >= 0:
                        res_l[k_i-2][int(data.loc[i, 'label'])] += 0.05 * total
                    if k_i < t_slices:
                        res_l[k_i+1][int(data.loc[i, 'label'])] += 0.2 * total
                    if k_i < t_slices-1:
                        res_l[k_i+2][int(data.loc[i, 'label'])] += 0.05 * total
                else:
                    res_l[k_i][int(data.loc[i, 'label'])] += total
                '''
           # res = {}
            #for i in range(t_slices + 1):
             #   res[keys[i]] = res_l[i]

            res_arr = [[t] + list(label2num.values()) for t, label2num in res.items()]


            #print(res_arr)

            '''
            final_arr = []
            for i in range(types):
                final_arr.append([])

            for arr in res_arr:
                y0 = -arr[-1]/2
                y1 = y0
                for i in range(types):
                    y1 = y0 + arr[i+1]
                    final_arr[i].append([arr[0], i, y0, y1])
                    y0 = y1
            
            #print(final_arr)
            
            '''
            with open(os.path.join('river', "tr_" + file[:-4]) + '.json', 'w', encoding='utf-8') as fout:
                json.dump(res_arr, fout, indent = 4, ensure_ascii = False)
        
            
            
            #res_df = pd.DataFrame(res_arr, columns=['time'] + ["cat" + str(label) for label in range(types)])

            # print(res)
            # print(res_arr)
            #print(res_df)
            
            #
            # print(data.shape)
            #
            # num_arr = [list(label2num.values()) for t, label2num in res.items()]
            # print(np.sum(num_arr))
            #res_df.to_csv(os.path.join('river', "tr_" + file[:-4]) + '.csv', index=False)


            

            #res_df.to_csv(os.path.join('river', file), index=False)


if __name__ == "__main__":
    generate_river_data()

