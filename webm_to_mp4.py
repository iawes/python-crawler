import subprocess
import ffmpeg

class FFMConvertor:

    def convert_webm_mp4_subprocess(self, input_file, output_file):
        try:
            command = 'C:\\usr\\bin\\ffmpeg\\bin\\ffmpeg.exe -i ' + input_file +' -c:v libx264 -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" '+ output_file + ' -y'
            print(command)
            subprocess.run(command)
        except:print('Some Exception')

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

if __name__ == "__main__":
    webm_to_mp4(r'C:\N-20S1PF344DFM-Data\yaweili\Downloads\2023-03-03.webm', r'C:\N-20S1PF344DFM-Data\yaweili\Downloads\2023-03-03.mp4')
# ffm.convert_webm_mp4_module(r*.webm', r'*.mp4')