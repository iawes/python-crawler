# 导入talib库和pandas库
import talib
import pandas as pd
import requests
import json
import re

# 定义一个函数，根据股票代码和日期范围获取股票数据
def get_stock_data(code, start_date, end_date):
    # 设置请求的url，这里是使用新浪财经的接口
    url = f"http://quotes.sina.cn/cn/api/jsonp_v2.php/=/CN_MarketDataService.getKLineData?symbol={code}&scale=240&ma=no&datalen=1023"
    # 发送get请求，获取网页内容
    response = requests.get(url)
    # 判断响应状态码是否为200，表示成功
    if response.status_code == 200:
        # 获取网页内容的文本格式，并去掉前后的无用字符
        text = response.text.strip("=/CN_MarketDataService.getKLineData();")
        # 将文本转换为json格式的数据
        data = json.loads(text)
        # 将数据转换为pandas的DataFrame格式，并设置日期为索引
        df = pd.DataFrame(data)
        df["day"] = pd.to_datetime(df["day"])
        df.set_index("day", inplace=True)
        # 根据日期范围筛选数据，并返回
        return df.loc[start_date:end_date]
    else:
        # 返回空的DataFrame
        return pd.DataFrame()

# 定义一个函数，根据股票数据计算涨跌幅，并返回涨跌幅列
def get_change(data):
    # 使用pct_change方法计算涨跌幅，参数为收盘价
    change = data["close"].pct_change()
    # 返回涨跌幅列
    return change

# 定义一个函数，根据股票数据和涨跌幅判断是否满足葛兰碧法则，并返回买入或卖出信号
def get_signal(data, change):
    # 创建一个空列表，用于存储信号
    signal = []
    # 遍历股票数据的每一行和对应的涨跌幅
    for i in range(len(data)):
        row = data.iloc[i]
        date = row.name.strftime("%Y-%m-%d")
        close = row["close"]
        chg = change[i]
        # 如果涨跌幅大于5%，表示暴涨或暴跌，信号为0，表示不操作
        if abs(chg) > 0.05:
            sig = 0
        # 如果涨跌幅小于5%，表示调整或反弹，判断前两天的涨跌幅是否都大于5%
        elif abs(chg) < 0.05:
            # 如果前两天的涨跌幅都大于5%，并且同号，表示连续两天暴涨或暴跌，根据葛兰碧法则判断买卖信号
            if i >= 2 and abs(change[i-1]) > 0.05 and abs(change[i-2]) > 0.05 and (change[i-1] * change[i-2] > 0):
                # 如果前两天都是暴涨，信号为-1，表示卖出股票
                if change[i-1] > 0 and change[i-2] > 0:
                    sig = -1
                # 如果前两天都是暴跌，信号为1，表示买入股票    
                elif change[i-1] < 0 and change[i-2] < 0:
                    sig = 1
            # 否则，信号为0，表示不操作    
            else:
                sig = 0
        # 将信号添加到列表中        
        signal.append(sig)
    # 返回信号列表    
    return signal

# 定义一个函数，根据股票代码、日期范围和初始资金模拟交易，并打印交易记录和最终收益率
def backtest(code, start_date, end_date, capital):
    # 获取股票数据
    data = get_stock_data(code, start_date, end_date)
    # 计算涨跌幅
    change = get_change(data)
    # 获取信号列表
    signal = get_signal(data, change)
    # 创建一个变量，用于存储持仓状态，初始为0，表示空仓
    position = 0
    # 创建一个变量，用于存储持仓数量，初始为0，表示没有持仓
    amount = 0
    # 创建一个变量，用于存储剩余资金，初始为初始资金
    balance = capital
    # 打印交易开始的信息
    print(f"开始回测{code}的策略，日期范围为{start_date}至{end_date}，初始资金为{capital}元")
    print("-" * 50)
    print("日期\t\t\t收盘价\t\t信号\t\t持仓\t\t数量\t\t余额")
    print("-" * 50)
    # 遍历股票数据的每一行和对应的信号
    for i in range(len(data)):
        row = data.iloc[i]
        date = row.name.strftime("%Y-%m-%d")
        close = row["close"]
        sig = signal[i]
        # 如果信号为1，表示买入条件满足，并且当前为空仓，则买入股票，并更新持仓状态、持仓数量和剩余资金
        if sig == 1 and position == 0:
            position = 1
            amount = int(balance / close / 100) * 100 # 取整百股
            balance -= amount * close * (1 + 0.0003) # 扣除买入金额和手续费（万分之三）
            print(f"{date}\t{close}\t\t{sig}\t\t{position}\t\t{amount}\t\t{balance:.2f}")
        # 如果信号为-1，表示卖出条件满足，并且当前为持仓，则卖出股票，并更新持仓状态、持仓数量和剩余资金    
        elif sig == -1 and position == 1:
            position = 0
            balance += amount * close * (1 - 0.0013 - 0.001) # 增加卖出金额并扣除手续费（千分之一点三）和印花税（千分之一）
            amount = 0 
            print(f"{date}\t{close}\t\t{sig}\t\t{position}\t\t{amount}\t\t{balance:.2f}")
        # 否则，不进行交易，维持原来的状态    
        else:
            print(f"{date}\t{close}\t\t{sig}\t\t{position}\t\t{amount}\t\t{balance:.2f}")
    
    print("-" * 50)
    
    # 计算最终收益率，并打印结果
    
    if position == 1: # 如果最后还有持仓，则按照最后一天的收盘价计算收益率
        
        final_balance = balance + amount * close * (1 - 0.0013 - 0.001)
        
    else: # 否则，按照剩余资金计算收益率
        
        final_balance = balance
    
    return_rate = (final_balance - capital) / capital * 100
    
    print(f"回测结束，最终收益率为{return_rate:.2f}%")

backtest("sz300364", "2021-01-01", "2021-12-31", 100000)
