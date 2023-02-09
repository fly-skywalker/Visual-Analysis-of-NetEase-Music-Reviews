# from pyecharts.charts import ThemeRiver
# import pyecharts.options as opts

import numpy as np
import pandas as pd

### from github ###
import time


def timeStamp(timeNum):
    timeStamp = float(timeNum / 1000)
    timeArray = time.localtime(timeStamp)
    reTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
    return reTime


###################

df = pd.read_csv('../data/songdata/82177.csv', dtype='string')

df['time'] = df['time'].map(lambda x: timeStamp(int(x))[:10])

data = df[df['ishot'] == '0']

data = data[['time', 'label']]

types = 0
for i in range(10):
    if df[df['label'] == str(i)].shape[0] == 0:
        types = i
        break

print(types)

data.insert(loc=1, column='weight', value=[1] * data.shape[0])

print(data)

data_l = np.array(data).tolist()

timestamp = []
for i in data_l:
    if i[0] not in timestamp:
        timestamp.append(i[0])

# print(timestamp)

res = []
for t in timestamp:
    for l in range(types):
        res.append([t, 0, str(l)])
        for i in data_l:
            if i[0] == t and i[2] == str(l):
                res[-1][1] += 1

print(res)

exit()
c = (
    ThemeRiver(init_opts=opts.InitOpts(width="900px", height="600px"))
        .add(
        series_name=[str(i) for i in range(types)],
        data=res,
        singleaxis_opts=opts.SingleAxisOpts(
            pos_top="50", pos_bottom="50", type_="time"
        ),
    )
        .set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line")
    )
        .render("../themeriver.html")
)
