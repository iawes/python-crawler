### 导包
import akshare as ak
import pandas as pd
import numpy as np
import os

### 设置工作路径
mypath=r"..."
stock_zh_spot_df = ak.stock_zh_a_spot_em() ## 获取实时数据
stock_zh_spot_data=stock_zh_spot_df[stock_zh_spot_df['名称']!=''] ## 去除名称为空值的数据
codes_names=stock_zh_spot_data[['代码','名称']]

length=len(codes_names)
all_data = pd.DataFrame([])
for i in range(length):
    try:
        data_df = ak.stock_zh_a_hist(symbol=codes_names['代码'][i], period="daily", start_date="20150101", adjust="hfq") ## 日度数据，后复权
        data_df['stock_id']=codes_names['代码'][i]
        all_data=all_data.append(data_df)
    except:
        KeyError()


all_data.to_csv(os.path.join(mypath+'\\'+'All_Data.csv'),encoding='utf_8_sig') ## 数据导出为csv文件

all_data.to_csv(os.path.join(mypath+'\\'+'All_Data.txt'),sep="\t",index=True) ## 数据导出为txt文件