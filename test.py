import os
import re
import datetime
import sys
import os

name = 'DRG/DIP概念'
print(name)

name2 = re.sub('([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u007a])', '', name)
print(name2)

day = datetime.date.today().strftime("%Y-%m-%d")
print(day)
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(now)
yes = (datetime.datetime.now() + datetime.timedelta(days = -1)).strftime('%Y-%m-%d')
print(yes)

try:
    raise RuntimeError('这里有个报错')
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
