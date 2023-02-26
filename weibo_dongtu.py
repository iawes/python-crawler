import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline, Grid
from pyecharts.globals import ThemeType, CurrentConfig
import argparse
import os
import sys

def new_charts(file_path):
    factor = 10
    #CurrentConfig.ONLINE_HOST = 'D:/python/pyecharts-assets-master/assets/'
    CurrentConfig.ONLINE_HOST = 'http://127.0.0.1:8000/assets/'
    df1 = pd.read_csv(file_path)
    #print(df1)
    #df1 = df.groupby(df['时间'])
    #print(df1)
    #print(df['时间'])
    #print(list(df['时间']))
    # print(df.info())
    t = Timeline(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))  # 定制主题
    #print(range(20))

    #print(list(df['排名']))
    #print(df1.loc[df1['排名'].isin(range(11))])
    df = df1.loc[df1['排名'].isin(range(11))]
    n = list(df['排名']).count(1)
    print(n)

    for i in range(n):
        #print(i)
        #print(list(df['时间'])[i*factor])
        #print(list(df['标题'])[i*factor: i*factor+10])
        #print(list(df['标题'])[i*factor: i*factor+10][::-1])
    #    print(df['标题'][i*factor: i*factor+10][0:9:1])
    #    print(df['热度'][i*factor: i*factor+10])
    #    print(df['热度'][i*factor: i*factor+10][0:9:1])
        bar = (
            Bar()
            #.add_xaxis(list(df['标题'][i*10: i*10+10][::-1]))         # x轴数据
            .add_xaxis(list(df['标题'])[i*factor: i*factor+10][::-1])         # x轴数据
            .add_yaxis('微博热搜榜', list(df['热度'])[i*factor: i*factor+10][::-1])   # y轴数据
            #.add_yaxis('热度', list(df['热度'][i*10: i*10+10][::-1]))   # y轴数据
            .reversal_axis()     # 翻转
            .set_global_opts(    # 全局配置项
                title_opts=opts.TitleOpts(  # 标题配置项
                    title=f"{list(df['时间'])[i*factor]}",
                    pos_right="5%", pos_bottom="15%",
                    title_textstyle_opts=opts.TextStyleOpts(
                        #font_family='KaiTi', font_size=24, color='#FF1493'
                        font_family='KaiTi', font_size=24, color='#FF1493'
                    )
                ),
                xaxis_opts=opts.AxisOpts(   # x轴配置项
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
                yaxis_opts=opts.AxisOpts(   # y轴配置项
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    #axislabel_opts=opts.LabelOpts(color='#DC143C')
                    axislabel_opts=opts.LabelOpts(font_size=18, color='#DC143C')
                )
            )
            .set_series_opts(    # 系列配置项
                label_opts=opts.LabelOpts(  # 标签配置
                    #position="right", color='#9400D3')
                    position="right", font_size=18, color='#9400D3')
            )
        )
        grid = (
            Grid()
                #.add(bar, grid_opts=opts.GridOpts(pos_left="24%"))
                .add(bar, grid_opts=opts.GridOpts(pos_left="36%"))
        )
        t.add(grid, "")
        t.add_schema(
            play_interval=200,          # 轮播速度
            is_timeline_show=False,     # 是否显示 timeline 组件
            is_auto_play=True,          # 是否自动播放
        )

    html_path = file_path + '.html'
    t.render(html_path)

def train_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default='./weibo/热榜4.csv', type=str, help='csv file path')
    opt = parser.parse_args()
    return opt

if __name__ == "__main__":
    opt = train_options()
    print(opt)

    try:
        new_charts(opt.file)
    except Exception as e:
        except_type, except_value, except_traceback = sys.exc_info()
        except_file = os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
        exc_dict = {
            "报错类型": except_type,
            "报错信息": except_value,
            "报错文件": except_file,
            "报错行数": except_traceback.tb_lineno,
        }
        print(exc_dict)