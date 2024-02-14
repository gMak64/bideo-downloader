from tkinter import filedialog
import tkinter as tk
import os
from pytube import YouTube

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll

    myappid = "stonkedd.yt.downloader"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


def download():
    resolution = get_resolution(resolution_choice.get())
    video_url = ent_video.get()
    video = YouTube(video_url)
    filename = video.title.replace(":", "-") + ".mp4"
    filename = filename.replace("/", "-")
    print(filename)

    if resolution == "Highest":
        video = video.streams.get_highest_resolution()
    else:
        video = video.streams.filter(res=resolution).first()

    try:
        video.download(output_path=folder_path.get(), filename=filename + ".mp4")
        print("Video was downloaded successfully")
        open_popup("Video was downloaded successfully")
    except:
        print("Failed to download video")
        open_popup("Failed to download video")


def download_audio():
    video_url = ent_video.get()
    video = YouTube(video_url)
    filename = video.title.replace(":", "-") + ".mp3"
    filename = filename.replace("/", "-")
    print(filename)

    video = video.streams.filter(only_audio=True).first()

    try:
        video.download(output_path=folder_path.get(), filename=filename)
        print("Audio was downloaded successfully")
        open_popup("Audio was downloaded successfully")
    except:
        print("Failed to download audio")
        open_popup("Failed to download audio")


def get_resolution(key):
    if key == 1:
        return "144p"
    if key == 2:
        return "360p"
    if key == 3:
        return "720p"
    if key == 4:
        return "Highest"


def get_folder_path():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)


def open_popup(text):
    top = tk.Toplevel(window)
    top.geometry("750x250")
    top.title("Download Status")
    tk.Label(top, text=text).place(x=150, y=80)


window = tk.Tk()
window.title("YouTube Downloader")
window.resizable(width=False, height=False)

resolution_choice = tk.IntVar()
folder_path = tk.StringVar()

lbl_video = tk.Label(window, text="YouTube URL")
ent_video = tk.Entry(window, width=75)

btn_convert_mp4 = tk.Button(
    master=window,
    text="MP4",
    command=download,
    width=10
)

btn_convert_mp3 = tk.Button(
    master=window,
    text="MP3",
    command=download_audio,
    width=10
)

lbl_folder = tk.Label(master=window, text="Save Location")
btn_folder = tk.Button(master=window, text="Browse Folder", command=get_folder_path)
ent_folder = tk.Entry(master=window, width=88, textvariable=folder_path)

res_label = tk.Label(window,
                     text="""Choose a resolution:""")

res_144p_button = tk.Radiobutton(window,
                                 text="144p",
                                 variable=resolution_choice,
                                 value=1)

res_360p_button = tk.Radiobutton(window,
                                 text="360p",
                                 variable=resolution_choice,
                                 value=2)

res_720p_button = tk.Radiobutton(window,
                                 text="720p",
                                 variable=resolution_choice,
                                 value=3)

res_highest_button = tk.Radiobutton(window,
                                    text="Highest",
                                    variable=resolution_choice,
                                    value=4)

lbl_folder.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
btn_folder.grid(row=0, column=1, pady=(20, 0), sticky="w")
ent_folder.grid(row=0, column=1, padx=(150, 0), pady=(20, 0), sticky="w")

lbl_video.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="w")
ent_video.grid(row=1, column=1, pady=(20, 0), sticky="w")
btn_convert_mp4.grid(row=1, column=1, padx=(700, 25), pady=(20, 0), sticky="w")
btn_convert_mp3.grid(row=1, column=1, padx=(825, 25), pady=(20, 0), sticky="w")

res_label.grid(row=2, column=0, padx=20, pady=(20, 10), sticky="w")
res_144p_button.grid(row=3, column=0, padx=30, pady=(5, 5), sticky="w")
res_360p_button.grid(row=4, column=0, padx=30, pady=5, sticky="w")
res_720p_button.grid(row=5, column=0, padx=30, pady=5, sticky="w")
res_highest_button.grid(row=6, column=0, padx=30, pady=(10, 20), sticky="w")

# window.iconbitmap("dratini.ico")
window.iconbitmap(os.path.join("./", "dratini.ico"))
window.mainloop()
