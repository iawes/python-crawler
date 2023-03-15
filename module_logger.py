import sys

from loguru import logger

my_log_file_path = 'runtime_{time}.log'


class MyLogger:
    def __init__(self):
        self.logger = logger
        # 清空所有设置
        self.logger.remove()
        # 添加控制台输出的格式,sys.stdout为输出到屏幕;关于这些配置还需要自定义请移步官网查看相关参数说明
        self.logger.add(sys.stdout,
                        format="<green>{time:YYYYMMDD HH:mm:ss}</green> | "  # 颜色>时间
                               "{process.name} | "  # 进程名
                               "{thread.name} | "  # 进程名
                               "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
                               ":<cyan>{line}</cyan> | "  # 行号
                               "<level>{level}</level>: "  # 等级
                               "<level>{message}</level>",  # 日志内容
                        )

    def add_file(self,  log_file_path='.//'):
        # 输出到文件的格式,注释下面的add',则关闭日志写入
        log_file_path = log_file_path + my_log_file_path
        print(log_file_path)
        self.logger.add(log_file_path, level='INFO',
                        format='{time:YYYYMMDD HH:mm:ss} - '  # 时间
                               "{process.name} | "  # 进程名
                               "{thread.name} | "  # 进程名
                               '{module}.{function}:{line} - {level} -{message}',  # 模块名.方法名:行号
                        #rotation="100 kB")
                        rotation="1 day")

    def get_logger(self):
        return self.logger

logme = MyLogger()
#my_logger = MyLogger().get_logger()

def get_logme():
    return logme.get_logger()

def add_logme(file):
    logme.add_file(file)
    return logme.get_logger()

def ss():
    my_logger = get_logme('.//weibo//')

    my_logger.info(2222222)
    my_logger.debug(2222222)
    my_logger.warning(2222222)
    my_logger.error(2222222)
    my_logger.exception(2222222)

if __name__ == '__main__':
    ss()
