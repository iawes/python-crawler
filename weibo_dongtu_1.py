import csv
import time
import os
from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline, Grid
from pyecharts.globals import ThemeType, CurrentConfig
import pandas as pd

data = pd.read_csv('热榜.csv')
#print(data)
#print(data['时间'])
#print(list(data['时间']))
CurrentConfig.ONLINE_HOST = 'http://127.0.0.1:8000/assets/'

tl = Timeline()
for i in range(50):
    bar = (
        Bar()
        .add_xaxis(list(data['标题'])[i*10:i*10+10][::-1])
        .add_yaxis("微博热搜榜", list(data['热度'])[i*10:i*10+10][::-1])
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts("{}".format(list(data['时间'])[i*5]),pos_right='0%',pos_bottom='15%'),
            xaxis_opts=opts.AxisOpts(
                splitline_opts=opts.SplitLineOpts(is_show=True)),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True),
                                     axislabel_opts=opts.LabelOpts(color='#FF7F50')),)
        .set_series_opts(label_opts=opts.LabelOpts(position="right",color='#9400D3'))
    )
    grid = (
        Grid()
        .add(bar, grid_opts=opts.GridOpts(pos_left="25%",pos_right="0%"))
    )
    tl.add(grid, "{}年".format(i))  #设置标签
    tl.add_schema(
        play_interval=1000,   #播放速度
        is_timeline_show=False,  #是否显示 timeline 组件
        is_auto_play=True,
    )
#l.render_notebook()
tl.render('时间轮播图2.html')
