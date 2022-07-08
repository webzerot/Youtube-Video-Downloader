from pytube import YouTube
import os
import threading
from os import _exit
from tkinter import *

# sample video : https://www.youtube.com/watch?v=OQ6R4TU5Vwo

APPLICATION_NAME = "youtube2MP3"
LOGGING = True

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
WINDOW_TITLE = APPLICATION_NAME
WINDOW_BACKGROUND_COLOR = "#DEBAEE"

# initializing window
MAIN_WINDOW = Tk()

# CheckBox Var
CheckBox_Var = IntVar()

class Status:
    @staticmethod
    def IDLE():
        return "Status : Idle"
    @staticmethod
    def STARTING():
        return "Status : Starting"
    @staticmethod
    def DOWNLOADING():
        return "Status : Downloading"

def LOG(value):
    if LOGGING == True:
        print(value)

def GUI_PROPERTIES():
    global MAIN_WINDOW
    MAIN_WINDOW.title(WINDOW_TITLE)
    MAIN_WINDOW.geometry(f"{str(WINDOW_WIDTH)}x{str(WINDOW_HEIGHT)}")
    MAIN_WINDOW.configure(bg=WINDOW_BACKGROUND_COLOR)
    MAIN_WINDOW.resizable(False,False)

#GUI ELEMENTS

Text_TitleText = Label(font=("Elvetica",16),text=APPLICATION_NAME,bg=WINDOW_BACKGROUND_COLOR)
Text_TitleText.pack()

Text_VideoLink = Label(font=("Elvetica",13),text="Video Link",bg=WINDOW_BACKGROUND_COLOR)
Text_VideoLink.pack()

Text_VideoPath = Label(font=("Elvetica",13),text="File Path (blank for current)",bg=WINDOW_BACKGROUND_COLOR)
Text_VideoPath.place(x=97,y=83)

TextBox_youtube_VideoLink = Text(MAIN_WINDOW, height = 1, width = 47,font=('Elvetica',11),bg="#ECE3C1")
TextBox_youtube_VideoLink.place(x=10,y=60)

TextBox_VideoPath = Text(MAIN_WINDOW, height = 1, width = 47,font=('Elvetica',11),bg="#ECE3C1")
TextBox_VideoPath.place(x=10,y=110)

Text_StatusText = Label(font=("Elvetica",16),text=Status.IDLE(),bg=WINDOW_BACKGROUND_COLOR)
Text_StatusText.place(x=10,y=260)

CheckBox_Mp4_Download = Checkbutton(MAIN_WINDOW, text = "MP4",variable=CheckBox_Var,bg=WINDOW_BACKGROUND_COLOR)
CheckBox_Mp4_Download.place(x=330,y=260)

def Download_Vid_To_Mp3():
    global TextBox_youtube_VideoLink
    global Text_StatusText
    global TextBox_VideoPath
    try:
        Text_StatusText.config(text=Status.STARTING())
        m_VideoLink = str(TextBox_youtube_VideoLink.get(1.0, "end-1c"))
        m_VideoPath = str(TextBox_VideoPath.get(1.0, "end-1c"))

        yt = YouTube(m_VideoLink)

        video = yt.streams.filter(only_audio=True).first()
        # starting download
        Text_StatusText.config(text=Status.DOWNLOADING())
        output_file = video.download(m_VideoPath)

        if (os.path.exists(str(output_file).replace(".mp4",".mp3"))):
            filePath = str(output_file).replace(".mp4",".mp3")
            os.remove(output_file)
            LOG(f"[+] File \"{filePath}\" already exists")
            Text_StatusText.config(text=Status.IDLE())
            return
        
        # converting mp4 to mp3
        base, ext = os.path.splitext(output_file)
        new_file = base + '.mp3'
        os.rename(output_file, new_file)

        Text_StatusText.config(text=Status.IDLE())
        LOG(f"[+] Succesfully downloaded: \"{new_file}\"")
    except:
        LOG("[+] Invalid Video Link")
        Text_StatusText.config(text=Status.IDLE())

def Download_Vid_To_Mp4():
    global TextBox_youtube_VideoLink
    global Text_StatusText
    global TextBox_VideoPath

    try:
        Text_StatusText.config(text=Status.STARTING())
        m_VideoLink = str(TextBox_youtube_VideoLink.get(1.0, "end-1c"))
        m_VideoPath = str(TextBox_VideoPath.get(1.0, "end-1c"))

        video = YouTube(m_VideoLink)
        
        stream = video.streams.get_highest_resolution()

        Text_StatusText.config(text=Status.DOWNLOADING())
        output_file = stream.download(m_VideoPath)
        
        LOG(f"[+] Succesfully downloaded: \"{output_file}\"")

        Text_StatusText.config(text=Status.IDLE())
    except:
        LOG("[+] Invalid Video Link")
        Text_StatusText.config(text=Status.IDLE())     

def Multi_Threaded_MP3_Downloader():
    downloader_Thread = threading.Thread(target=Download_Vid_To_Mp3)
    downloader_Thread.start()

def Multi_Threaded_MP4_Downloader():
    downloader_Thread = threading.Thread(target=Download_Vid_To_Mp4)
    downloader_Thread.start()

def DOWNLOAD():
    global CheckBox_Var
    if CheckBox_Var.get() == 1:
        Multi_Threaded_MP4_Downloader()
    elif CheckBox_Var.get() == 0:
        Multi_Threaded_MP3_Downloader()

def Main():
    global MAIN_WINDOW

    # button used to download the youtube video
    Button_DownloadBtn = Button(width=25, height=5, text="DOWNLOAD",bg="#8FD7AC",command=DOWNLOAD)
    Button_DownloadBtn.place(x=107, y=150)

    MAIN_WINDOW.mainloop()


if __name__ == "__main__":
    LOG(f"[+] [Thanks for using \"{APPLICATION_NAME}\"]\n")
    GUI_PROPERTIES()
    GUI_THREAD = threading.Thread(target=Main()).start()
