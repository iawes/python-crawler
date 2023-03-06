import time,webbrowser, pyautogui
import os

filename = 'file:///'+os.getcwd()+'/weibo/' + '2023-03-03.video.html'
print(filename)

#webbrowser.open_new_tab(filename)

def html_to_video(filename, interval):
    webbrowser.open_new_tab(filename)

def open_close(url="https://www.python.org/"):
    webbrowser.open(url)
    time.sleep(20)
    pyautogui.hotkey('ctrl', 'w')
    print("tab closed")

if __name__ == "__main__":
    open_close()