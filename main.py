# -*- coding: utf-8 -*-

import sys, os, urllib, urllib.request, json, urllib.parse
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from yt_dlp import YoutubeDL
from flox import Flox

VIDEOS_FOLDER = "./videos"

class DownloadYT(Flox):

    def query(self, query):
        data = self.get_video_data(query)
        title = data["title"]
        author = data["author_name"]

        self.add_item(
            title=f"Download {title}",
            subtitle=author,
            icon="./images/download.png",
            method=self.download_video,
            parameters=query
        )

    def context_menu(self, data):
        self.add_item(
            title="Open video folder",
            subtitle="Press enter to open the folder containing your downloaded videos",
            icon="./images/folder.png",
            method=self.open_video_folder
        )

    def download_video(self, url):
        with YoutubeDL({"paths": {"home": self.settings["videos_folder"]}}) as ytdl:
            if not os.path.exists(self.settings["videos_folder"]):
                os.mkdir(f"{os.getcwd()}\\videos")
                self.settings["videos_folder"] = f"{os.getcwd()}\\videos"
            ytdl.download(url)
    
    def open_video_folder(self):
        if not os.path.exists(self.settings["videos_folder"]):
            os.mkdir(f"{os.getcwd()}\\videos")
            self.settings["videos_folder"] = f"{os.getcwd()}\\videos"
        os.startfile(self.settings["videos_folder"])

    def get_video_data(self, url: str):
        params = {"format": "json", "url": url}
        oembed = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        oembed = oembed + "?" + query_string

        with urllib.request.urlopen(oembed) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
            return data


if __name__ == "__main__":
    DownloadYT()