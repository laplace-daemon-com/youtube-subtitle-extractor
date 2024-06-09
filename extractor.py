import os
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL


# 手動設定箇所
URL = "https://www.youtube.com/watch?v=XjV4HYZTJB8"  # 対象動画のURL
LANG = "en" # "ja"に変更すると日本語で出力

# 変更不要設定
URLS = [URL]
FORMAT = "ttml"


# 動画タイトル取得
with YoutubeDL() as ydl:
    info = ydl.extract_info(URL, download=False)
    title = info["title"].replace(" ", "_")


# 字幕取得用オプション
ydl_opts = {
    "skip_download": True,  # 動画自体のダウンロードスキップ
    "writeautomaticsub": True,  # 自動設定字幕を取得
    "subtitleslangs": [LANG],  # 言語設定
    "subtitlesformat": FORMAT,  # 出力フォーマット（一次ファイルとして使ってます）
    "outtmpl": title  # 出力ファイル名
}

# 字幕ダウンロード（ファイル出力。この時点ではttml形式のごちゃごちゃした状態）
with YoutubeDL(ydl_opts) as ydl:
    ydl.download(URLS)


# 以下で一時的に出力したttml形式ファイルをtxt形式に整形
downloaded_file = f"{title}.{LANG}.{FORMAT}"
with open(downloaded_file, mode="r") as f:
    contents = f.read()

soup = BeautifulSoup(contents, "xml")
p_tags = soup.find_all("p")

subtitles = [tag.get_text() for tag in p_tags]  # pタグ内のテキスト情報だけ取得
subtitle = "\n".join(subtitles)
subtitle = "\n\n".join([info["title"], subtitle])
output_directory = "output"

os.makedirs(output_directory, exist_ok=True)
with open(f"{output_directory}/{title}.{LANG}.txt", mode="w") as f:
    f.write(subtitle)


# 不要になった一次ファイル削除
os.remove(downloaded_file)