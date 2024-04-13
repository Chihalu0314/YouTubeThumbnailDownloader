import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import os
from googleapiclient.discovery import build

# YouTube Data APIのキーを設定します。
api_key = " "

# YouTube Data APIのサービスを作成します。
youtube = build('youtube', 'v3', developerKey=api_key)

def download_thumbnail():
    video_url = entry.get()
    video_id = video_url.split('=')[-1]
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()

    if not response["items"]:
        messagebox.showerror("エラー", "動画が見つかりませんでした。")
        return

    thumbnail_url = response["items"][0]["snippet"]["thumbnails"].get("maxres", {}).get("url")
    if not thumbnail_url:
        messagebox.showinfo("情報", "最高解像度のサムネイルは利用できません。高解像度のサムネイルをダウンロードします。")
        thumbnail_url = response["items"][0]["snippet"]["thumbnails"]["high"]["url"]

    thumbnail_data = requests.get(thumbnail_url).content

    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", initialfile=f"{video_id}_thumbnail", filetypes=[("JPEG files", "*.jpg")])
    if not save_path:
        return

    with open(save_path, "wb") as f:
        f.write(thumbnail_data)

    messagebox.showinfo("成功", "サムネイルをダウンロードしました。")

root = tk.Tk()
root.title("YouTube Thumbnail Downloader")

label = tk.Label(root, text="YouTube動画のURLを入力してください：")
label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

button = tk.Button(root, text="ダウンロード", command=download_thumbnail)
button.pack()

# ウィンドウを画面の中央に配置
window_width = 500
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

root.mainloop()
