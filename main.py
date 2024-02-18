from __future__ import unicode_literals
import os
from subprocess import call
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
import yt_dlp
from yt_dlp.utils import download_range_func

basedir = os.path.dirname(__file__)


class MyLogger:
    def debug(self, msg):
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


try:
    from ctypes import windll

    my_app_id = "stonkedd.yt.downloader"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
except ImportError:
    pass

# other_opts = {
#     'download_ranges': download_range_func(None, [(curr_time+start, curr_time+end)]),
# }


def download():
    videos = ent_video.get('1.0', 'end-1c').splitlines()
    names = ent_name.get('1.0', 'end-1c').splitlines()
    if len(names) < len(videos):
        with yt_dlp.YoutubeDL() as ydl:
            for video in videos:
                info = ydl.extract_info(video, download=False)
                name = info['title']
                name = name.replace(":", "-")
                name.replace("/", "-")
                names.append(name)

    resolution = get_resolution(resolution_choice.get())
    if resolution == "Highest":
        download_format = 'bv[ext=mp4]*+ba[ext=m4a]/b[ext=mp4]'
    else:
        download_format = 'wv[ext=mp4]*+wa[ext=m4a]/w[ext=mp4]'

    good_downloads = 0
    bad_downloads = 0

    for (video, name) in zip(videos, names):
        if video != '\n':
            mp4_opts = {
                'outtmpl': folder_path.get() + "\\" + name + ".mp4",
                'format': download_format,
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
            }
            try:
                with yt_dlp.YoutubeDL(mp4_opts) as ydl:
                    error_code = ydl.download(video)
                print("Video was downloaded successfully")
                good_downloads += 1
            except:
                print("Failed to download video")
                bad_downloads += 1

    if good_downloads > 0:
        call(["open", folder_path.get()])
        if good_downloads == 1:
            open_popup("Video was downloaded successfully")
        else:
            open_popup(f"{good_downloads} videos were downloaded successfully")

    if bad_downloads > 0:
        if bad_downloads == 1:
            open_popup("Failed to download video")
        else:
            open_popup(f"{bad_downloads} videos failed to download")


def download_audio():
    videos = ent_video.get('1.0', 'end-1c').splitlines()
    names = ent_name.get('1.0', 'end-1c').splitlines()
    if len(names) < len(videos):
        with yt_dlp.YoutubeDL() as ydl:
            for video in videos:
                info = ydl.extract_info(video, download=False)
                name = info['title']
                name = name.replace(":", "-")
                name.replace("/", "-")
                names.append(name)

    good_downloads = 0
    bad_downloads = 0

    for (video, name) in zip(videos, names):
        if video != '\n':
            mp3_opts = {
                'outtmpl': folder_path.get() + "\\" + name,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            try:
                with yt_dlp.YoutubeDL(mp3_opts) as ydl:
                    error_code = ydl.download(video)
                print("Audio was downloaded successfully")
                good_downloads += 1
            except:
                print("Failed to download audio")
                bad_downloads += 1

    if good_downloads > 0:
        call(["open", folder_path.get()])
        if good_downloads == 1:
            open_popup("Audio was downloaded successfully")
        else:
            open_popup(f"{good_downloads} audios were downloaded successfully")

    if bad_downloads > 0:
        if bad_downloads == 1:
            open_popup("Failed to download audio")
        else:
            open_popup(f"{bad_downloads} audios failed to download")


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


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now post-processing ...')


window = tk.Tk()
window.title("YouTube Downloader")
window.resizable(width=False, height=False)

resolution_choice = tk.IntVar()
folder_path = tk.StringVar()

lbl_videos = tk.Label(window, text="YouTube URLs")
lbl_names = tk.Label(window, text="File Names")
ent_video = scrolledtext.ScrolledText(window, width=65, height=10, wrap="none")
ent_name = scrolledtext.ScrolledText(window, width=65, height=10, wrap="none")

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
ent_folder = tk.Entry(master=window, width=85, textvariable=folder_path)

res_label = tk.Label(window,
                     text="""Choose a resolution:""")

res_highest_button = tk.Radiobutton(window,
                                    text="Highest",
                                    variable=resolution_choice,
                                    value=1)

res_lowest_button = tk.Radiobutton(window,
                                   text="Lowest",
                                   variable=resolution_choice,
                                   value=2)

lbl_folder.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="w")
ent_folder.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="w")
btn_folder.grid(row=1, column=0, padx=(810, 0), pady=(20, 0), sticky="w")

lbl_videos.grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="w")
lbl_names.grid(row=2, column=0, padx=(500, 0), pady=(20, 0), sticky="w")
ent_video.grid(row=3, column=0, padx=(20, 0), pady=(20, 0), sticky="w")
ent_name.grid(row=3, column=0, padx=(500, 0), pady=(20, 0), sticky="w")
btn_convert_mp4.grid(row=8, column=0, padx=(20, 0), pady=(20, 20), sticky="w")
btn_convert_mp3.grid(row=8, column=0, padx=(150, 0), pady=(20, 20), sticky="w")

res_label.grid(row=5, column=0, padx=20, pady=(20, 10), sticky="w")
res_highest_button.grid(row=6, column=0, padx=30, pady=(10, 20), sticky="w")
res_lowest_button.grid(row=7, column=0, padx=30, pady=(5, 5), sticky="w")

# window.iconbitmap("dratini.ico")
window.iconbitmap(os.path.join("./", "dratini.ico"))
window.mainloop()
