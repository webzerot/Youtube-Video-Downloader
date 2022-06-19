from pytube import YouTube
from tkinter import *
from threading import Thread
import speedtest
from time import sleep
from sys import argv
import signal
from os import _exit
from os import system
from os import path

# https://www.youtube.com/watch?v=rxGnonKB7TY ## sample video

videoLink = ""
videoRes = ""
pathToProgram = str( path.abspath(__file__) ).replace( argv[0],"" )

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
WINDOW_TITLE = "simple video downloader"
PROGRAM_TITLE = "Youtube Video Downloader"
WINDOW_BACKGROUND_COLOR = "#DEBAEE"

def bytes_to_mb(bytes):
    KB = 1024 # One Kilobyte is 1024 bytes
    MB = KB * 1024 # One MB is 1024 KB
    return int(bytes/MB)

def on_closing(Caller=""):
    if (Caller == "console"):
        _exit(1)
    else:
        window.destroy()
        _exit(1)

def OnExithandler(signum, frame):
    _exit(1)

internetSpeed = 0

# window declaration
try:
    if (str(argv[1]).lower() == "console"):
        pass
except:
    window = Tk()

    #GUI
    Text_TitleText = Label(font=("Elvetica",16),text=PROGRAM_TITLE,bg=WINDOW_BACKGROUND_COLOR)
    Text_TitleText.place(x=70, y=10)

    Text_StatusText = Label(font=("Elvetica",16),text="Status : Idle",bg=WINDOW_BACKGROUND_COLOR)
    #Text_StatusText.place(x=135, y=120)
    Text_StatusText.place(x=10,y=260)

    TextBox_VideoLink = Text(window, height = 1, width = 47,font=('Elvetica',11),bg="#ECE3C1")
    TextBox_VideoLink.place(x=10,y=70)

def MeasureInternetSpeed():
    global internetSpeed
    speed_test = speedtest.Speedtest()
    download_speed = bytes_to_mb(speed_test.download())
    internetSpeed = download_speed

def multiThreadDownloadGUI():
    Thread(target=DownloadVideoGUI).start()

def InternetSpeedThread():
    Thread(target=MeasureInternetSpeed).start()

def DownloadVideoGUI():
    global videoLink
    videoLink = str(TextBox_VideoLink.get(1.0, "end-1c"))

    try:
        video = YouTube(videoLink)
    except:
        return
    Text_StatusText.config(text="Status : Starting Download")
    if (internetSpeed == 0):
        sleep(2)
        Text_StatusText.config(text="Status : Downloading")
        pass
    else:
        Text_StatusText.config(text="Status : Downloading | "+str(internetSpeed)+ " Mbp/s")
    stream = video.streams.get_highest_resolution()
    stream.download()
    Text_StatusText.config(text="Status : Idle")
try:
    if (str(argv[1]).lower() == "console"):
        pass
except:
    Button_DownloadBtn = Button(width=25, height=5, text="DOWNLOAD",bg="#8FD7AC",command=multiThreadDownloadGUI)
    Button_DownloadBtn.place(x=107, y=150)

def mainGUI():
    InternetSpeedThread()
    #window properties
    window.title(WINDOW_TITLE)
    window.configure(width=WINDOW_WIDTH, height=WINDOW_HEIGHT,bg=WINDOW_BACKGROUND_COLOR)
    window.resizable(False,False)
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

def mainConsole():
    global videoRes
    global videoLink
    #InternetSpeedThread()
    def Welcome():
        system("cls")
        print(f"[{PROGRAM_TITLE}]\n\n")
    
    Welcome()
    videoLink = str(input("[+] Enter Video URL : "))

    while (True):
        videoRes = str(input("[+] Enter Video Resolution(low/high) : "))
        if (videoRes.lower() == "low" or videoRes.lower() == "high"):
            break

    try:
        video = YouTube(videoLink)
    except:
        print("[-] There was a problem")
        _exit(1)

    if (videoRes.lower() == "high"):
        print("\n[*] Downloading in high resolution..")
        stream = video.streams.get_highest_resolution()
    elif(videoRes.lower() == "low"):
        print("\n[*] Downloading in low resolution..")
        stream = video.streams.get_lowest_resolution()
    

    stream.download()

    print(f"\n[+] \"{video.title}\" downloaded successfully in: {pathToProgram}")


# handling ctrl+c
signal.signal(signal.SIGINT, OnExithandler)

if __name__ == "__main__":
    try:
        if (str(argv[1]).lower() == "console"):
            mainConsole()
            on_closing("console")
    except:
        mainGUI()
