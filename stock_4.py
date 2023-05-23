# 导入所需的库
#import tushare as ts
import akshare as ak
import talib as ta

# 定义判断股票是否经历了摸线行情某个阶段的函数
def is_touch_line(code, date, stage):
    # 获取股票数据
#    df = ts.get_k_data(code, start=date, end=date)
    df = ak.stock_zh_a_daily(symbol=code, start_date=date, end_date=date)
    # 计算boll线和均线
    df['upper'], df['middle'], df['lower'] = ta.BBANDS(df['close'], timeperiod=20)
    df['ma5'] = ta.MA(df['close'], timeperiod=5)
    df['ma10'] = ta.MA(df['close'], timeperiod=10)
    df['ma20'] = ta.MA(df['close'], timeperiod=20)
    df['ma30'] = ta.MA(df['close'], timeperiod=30)
    # 判断是否满足某个阶段的条件
    if stage == '摸5日线':
        # 条件：收盘价大于等于5日线，并且前一天收盘价小于5日线
        return df.iloc[-1]['close'] >= df.iloc[-1]['ma5'] and df.iloc[-2]['close'] < df.iloc[-2]['ma5']
    elif stage == '摸10日线':
        # 条件：收盘价大于等于10日线，并且前一天收盘价小于10日线
        return df.iloc[-1]['close'] >= df.iloc[-1]['ma10'] and df.iloc[-2]['close'] < df.iloc[-2]['ma10']
    elif stage == '摸20日线':
        # 条件：收盘价大于等于20日线，并且前一天收盘价小于20日线
        return df.iloc[-1]['close'] >= df.iloc[-1]['ma20'] and df.iloc[-2]['close'] < df.iloc[-2]['ma20']
    elif stage == '摸30日线':
        # 条件：收盘价大于等于30日线，并且前一天收盘价小于30日线
        return df.iloc[-1]['close'] >= df.iloc[-1]['ma30'] and df.iloc[-2]['close'] < df.iloc[-2]['ma30']
    elif stage == '摸boll线上轨':
        # 条件：收盘价大于等于boll线上轨，并且前一天收盘价小于boll线上轨
        return df.iloc[-1]['close'] >= df.iloc[-1]['upper'] and df.iloc[-2]['close'] < df.iloc[-2]['upper']
    elif stage == '开口笑四天':
        # 条件：boll线上轨开口向上扩张，并且连续四个交易日收阳
        return (df.iloc[-1]['upper'] - df.iloc[-2]['upper']) > (df.iloc[-2]['upper'] - df.iloc[-3]['upper']) and \
               (df.iloc[-2]['upper'] - df.iloc[-3]['upper']) > (df.iloc[-3]['upper'] - df.iloc[-4]['upper']) and \
               (df.iloc[-3]['upper'] - df.iloc[-4]['upper']) > (df.iloc[-4]['upper'] - df.iloc[-5]['upper']) and \
               all(df['close'] > df['open'])
    else:
        # 其他情况返回False
        return False

# 定义发送提醒信息的函数
def send_alert(code, date, stage):
    # 根据阶段名称生成提醒内容
    if stage == '摸5日线':
        content = f'{code}在{date}突破了5日线，并在5日线上企稳不跌，说明股票有了一定的反弹动能。'
    elif stage == '摸10日线':
        content = f'{code}在{date}突破了10日线，但可能会遇到较大的回落，需要耐心等待股票再次站稳5日线，并向上突破10日线。'
    elif stage == '摸20日线':
        content = f'{code}在{date}突破了20日线，但可能会遇到较强的阻力，导致股票出现较大的调整，甚至二次探底。需要坚定信心，等待股票再次向上突破20日线。'
    elif stage == '摸30日线':
        content = f'{code}在{date}突破了30日线，但可能会遇到较强的阻力，导致股票出现较大的回落。需要谨慎操作，等待股票再次向上突破30日线。'
    elif stage == '摸boll线上轨':
        content = f'{code}在{date}突破了boll线上轨，但可能会遇到较强的阻力，导致股票出现较大的回调。需要灵活应变，等待股票在boll线中轨附近获得支撑，并再次向上突破boll线上轨。'
    elif stage == '开口笑四天':
        content = f'{code}在{date}突破了boll线上轨，并连续四个交易日收阳。这时候说明股票已经进入了强势上涨的趋势，并有可能沿着boll线中轨和boll线上轨一直往上攀升。可以考虑买入或者持有该股票。'
    else:
        # 其他情况返回空字符串
        content = ''
    # 打印提醒内容（可以改为其他方式发送）
    print(content)

# 定义主函数
def main(codes, start_date, end_date):
    # 定义摸线行情各个阶段的名称列表
    stages = ['摸5日线', '摸10日线', '摸20日线', '摸30日线', '摸boll线上轨', '开口笑四天']
    # 遍历所有股票代码
    for code in codes:
        # 获取股票数据
        #df = ts.get_k_data(code, start=start_date, end=end_date)
        df = ak.stock_zh_a_daily(symbol=code, start_date=start_date, end_date=end_date)
        # 定义当前股票处于哪个阶段的变量
        current_stage = 0
        # 遍历所有日期
        for date in df['date']:
            # 判断股票是否满足当前阶段的条件，并发送相应的提醒信息
            if is_touch_line(code, date, stages[current_stage]):
                send_alert(code, date, stages[current_stage])
                # 将当前阶段加一
                current_stage += 1
            # 如果已经经历了所有阶段，则给出买卖建议，并退出循环
            if current_stage == len(stages):
                print(f'{code}在{date}经历了所有摸线行情阶段，可以考虑买入或者持有该股票。')
# 测试函数
codes = ['300364']
start_date = '2021-01-01'
end_date = '2022-12-31'
main(codes, start_date, end_date)
