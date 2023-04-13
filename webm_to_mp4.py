import subprocess
import ffmpeg
import argparse
import os
from module_logger import get_logme

logger = get_logme()

# install ffmpeg https://www.mahailushu.com/essay/detail/oNAStNCH.html

class FFMConvertor:

    def convert_webm_mp4_subprocess(self, input_file, output_file):
        try:
            #command = 'C:\\usr\\bin\\ffmpeg\\bin\\ffmpeg.exe -i ' + input_file +' -c:v libx264 -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" '+ output_file + ' -y'
            command = '/usr/local/ffmpeg/bin/ffmpeg -i ' + input_file +' -c:v libx264 -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" '+ output_file + ' -y'
            print(command)
            subprocess.run(command)
        except:
            logger.exception('Some Exception')

    def convert_webm_mp4_module(self, input_file, output_file):
        #try:
        stream = ffmpeg.input(input_file)
        stream = ffmpeg.output(stream, output_file)
        ffmpeg.run(stream)
        #except:print('Some Exception')

def webm_to_mp4(input_file, output_file):
    ffm = FFMConvertor()
    #ffm.convert_webm_mp4_subprocess(r'C:\N-20S1PF344DFM-Data\yaweili\Downloads\2023-03-03.webm', r'C:\N-20S1PF344DFM-Data\yaweili\Downloads\2023-03-03-1.mp4')
    ffm.convert_webm_mp4_subprocess(input_file, output_file)
    #ffm.convert_webm_mp4_module(input_file, output_file)

def train_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", default='2023-03-03', type=str, help='csv file of the day')
    opt = parser.parse_args()
    return opt

if __name__ == "__main__":
    opt = train_options()

    #file_path = "C:\\N-20S1PF344DFM-Data\\yaweili\\Downloads\\"
    file_path = os.getcwd()+'/weibo/'
    webm_file = file_path + opt.day + '.webm'
    mp4_file = file_path + opt.day + '.mp4'
    #webm_to_mp4(webm_file, mp4_file)
    webm_to_mp4(webm_file, mp4_file)
# ffm.convert_webm_mp4_module(r*.webm', r'*.mp4')