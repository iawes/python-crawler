# 导入相关库
import pandas as pd
import numpy as np
import talib as ta
import tushare as ts

# 设置参数
N = 20 # 布林线中轨的移动平均周期
M = 2 # 布林线上下轨的标准差倍数
D = 3 # 突破中轨的持续天数
K = 5 # 5日均线

# 获取股票数据
stock_code = '300364' # 贵州茅台
start_date = '2021-01-01'
end_date = '2022-12-31'
df = ts.get_k_data(stock_code, start_date, end_date)

# 计算布林线指标
df['MA'] = ta.MA(df['close'], N) # 中轨
df['STD'] = ta.STDDEV(df['close'], N) # 标准差
df['UPPER'] = df['MA'] + M * df['STD'] # 上轨
df['LOWER'] = df['MA'] - M * df['STD'] # 下轨

# 计算5日均线
df['MA5'] = ta.MA(df['close'], K)

# 定义突破中轨的信号
df['BREAK'] = np.where((df['close'] > df['MA']) & (df['close'].shift(1) < df['MA'].shift(1)), 1, 0)

# 定义持续突破中轨的信号
df['CONTINUE'] = df['BREAK']
for i in range(1, D):
    df['CONTINUE'] += df['BREAK'].shift(i)

# 定义站上5日均线的信号
df['ABOVE'] = np.where(df['close'] > df['MA5'], 1, 0)

# 定义买入信号
df['BUY'] = np.where((df['CONTINUE'] == D) & (df['ABOVE'] == 1), 1, 0)

# 筛选出买入信号发出的日期和股价
buy_df = df[df['BUY'] == 1][['date', 'close']]
buy_df.columns = ['买入日期', '买入价格']

# 打印结果
print('基于布林线的股票策略')
print('股票代码：', stock_code)
print('回测区间：', start_date, '-', end_date)
print('买入信号：')
print(buy_df)
