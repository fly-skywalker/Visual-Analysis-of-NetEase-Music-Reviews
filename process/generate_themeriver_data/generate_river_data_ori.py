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

            df['time'] = df['time'].map(lambda x: timeStamp(int(x))[:10])

            data = df[df['ishot'] == 0]
            data = data[['time', 'label']]

            types = 0
            for i in range(10):
                if df[df['label'] == i].shape[0] == 0:
                    types = i
                    break

            timestamp = sorted(list(set(np.array(data)[:, 0])))

            res = {t: {label: 0 for label in range(types)} for t in timestamp}
            for i in data.index:
                res[data.loc[i, 'time']][int(data.loc[i, 'label'])] += 1
            res_arr = [[t] + list(label2num.values()) for t, label2num in res.items()]
            res_df = pd.DataFrame(res_arr, columns=['time'] + [str(label) for label in range(types)])

            # print(res)
            # print(res_arr)
            # print(res_df)
            #
            # print(data.shape)
            #
            # num_arr = [list(label2num.values()) for t, label2num in res.items()]
            # print(np.sum(num_arr))
            # res_df.to_csv(file.replace('.csv', '_river.csv'), index=False)

            res_df.to_csv(os.path.join('river', file), index=False)


if __name__ == "__main__":
    generate_river_data()

