"""
Created by Julius Jacobitz

Download raw videos as .mp4 from Youtube
"""

from pytube import YouTube
import os
import pathlib
import matplotlib.pyplot as plt
import pandas as pd
from urllib.error import HTTPError


def download_video(url:str,destination_dir:str,filename=None):
    """
    Download video from youtube using the best resolution and save in directory
    """
    if not pathlib.Path.is_dir(destination_dir):
        os.makedirs(destination_dir)
    
    print(f"Downloading {filename}")    
    video = YouTube(url)
    video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(destination_dir,filename=filename)


if __name__ == "__main__":
    path = pathlib.Path(__file__).parent.resolve() / "video_downloads"

    video_list = pd.read_excel("C:\\Users\\Julius\\OneDrive - bwedu\\Studium\\Bachelor\\07_BA\\Bachelorarbeit\\Data\\MTL-AQA\\MTL-AQA_dataset_release\\Video_List.xlsx",index_col=0)
    
    for sr_nr,row in video_list.iterrows():
        try:
            sr_nr_str = str(sr_nr)
            if len(sr_nr_str)<2:
                sr_nr_str = "0"+sr_nr_str 
            download_video(row.Video,path,sr_nr_str+".mp4")
        except (FileExistsError,HTTPError) as e: 
            print(e) 