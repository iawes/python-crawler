import os
import re
import argparse

from module_logger import get_logme

logger = get_logme()

def delete_lines(filename, head,tail):
    fin = open(filename, 'r')
    a = fin.readlines()
    fout = open(filename, 'w')
    b = ''.join(a[head:-tail])
    #fout.write(b)
    #print(b)
    return b

def convert_video_js(file1, file2, h1, t1, h2, t2, video_file):
    fd1 = open(file1, 'r', encoding='utf-8')
    str1 = fd1.readlines()
    str_body  = ''.join(str1[h1:-t1])
    fd1.close()

    fd2 = open(file2, 'r', encoding='utf-8')
    str2 = fd2.readlines()
    str_head = ''.join(str2[:h2])
    str_tail = ''.join(str2[t2:])
    fd2.close()

    # 这种方式不能替换有换行的字符串
    #str_tail.replace("test_xxx", file_v)
    #print(str_tail)

    # 需要转移符， file_v有 / 符合，会报错
    # https://www.cnpython.com/qa/318557
    # https://blog.csdn.net/weixin_41813169/article/details/105702294
    #temp2 = repr(file_v)
    #print(temp2)
    #str_tail = re.sub(r"\btest_xxx.mp4\b", temp2, str_tail)
    #print(str_tail)

    #含有路径的名字无法打开
    file_name = os.path.basename(file1).strip('.csv.html')
    #print(file_name)
    str_tail = re.sub(r"\btest_xxx\b", file_name, str_tail)
    #print(str_tail)

    str_all = str_head + str_body + str_tail
    #print(str_all)

    #file_output = file1.replace("csv", "video")
    #print(video_file)

    fout = open(video_file, 'w')
    fout.write(str_all)
    fout.close()

#file1 = r'C:\usr\code\pytdx\weibo\2023-02-26.csv.html'
#file2 = r'C:\usr\code\pytdx\convert_video_template.html'
#
#get_lines(file1, file2, 15, 4, 30, 31)

def train_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_src", default=r'./weibo/2023-03-11.csv.html', type=str, help='pycharts html file path')
    parser.add_argument("--file_template", default=os.getcwd()+'/convert_video_template.html', type=str, help='video conert template html file path')
    parser.add_argument("--head_line_src", default=15, type=int, help='rm head lines of csv html')
    parser.add_argument("--tail_line_src", default=4, type=int, help='rm tail lines of csv html')
    parser.add_argument("--head_line_temp", default=30, type=int, help='add head lines of video html')
    parser.add_argument("--tail_line_temp", default=31, type=int, help='add tail lines of video html')
    parser.add_argument("--video_file", default=r'./weibo/2023-03-11.video.html', type=str, help='output video html file path')
    opt = parser.parse_args()
    return opt

if __name__ == "__main__":
    opt = train_options()
    logger.debug(opt)

    try:
        convert_video_js(opt.file_src, opt.file_template, opt.head_line_src, opt.tail_line_src, opt.head_line_temp, opt.tail_line_temp, opt.video_file)
    except:
        logger.exception('convert_video_js failed.')
#    except Exception as e:
#        except_type, except_value, except_traceback = sys.exc_info()
#        except_file = os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
#        exc_dict = {
#            "报错类型": except_type,
#            "报错信息": except_value,
#            "报错文件": except_file,
#            "报错行数": except_traceback.tb_lineno,
#        }
#        print(exc_dict)