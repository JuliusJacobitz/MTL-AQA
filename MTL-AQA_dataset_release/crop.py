"""
Created by Julius Jacobitz

Crop Videos in frame range based on raw annotations
"""

import pandas as pd 
import os 
import pathlib
import cv2
from moviepy.editor import *


def frame_to_timestamp(frame:int,fps:float):
    """Convert frame number to seconds"""
    seconds = frame/fps
    return seconds

def normalize_columns(cols):
    """
    streamline different annotations
    """
    cols = cols.str.lower()
    cols = cols.str.replace("start_frame","start")
    cols = cols.str.replace("end_frame","end")
    cols = cols.str.replace("start frame","start")
    cols = cols.str.replace("end frame","end")
    cols = cols.str.replace("camera angle","view")
    cols = cols.str.replace("angle","view")
    
    
    cols = cols.str.replace(" ","") # do this at the end for safety reasons
    return cols

def create_subclips(annotation_path,video_path,result_folder):
    """
    Select all clips that are annotated with "s" (side view) and save them in
    an extra dir.
    """
    print(f"Creating subclips for {str(annotation_path)}")
    
    subfolder = pathlib.Path(result_folder) / str(os.path.split(video_path)[1]).split(".")[0]
    os.makedirs(subfolder,exist_ok=True)

    annotations = pd.read_excel(annotation_path,index_col=0)
    annotations.columns = normalize_columns(annotations.columns)

    annotations:pd.DataFrame = annotations[annotations.view.str.lower() == "s"] # only select side views


    # get fps
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()


    video = VideoFileClip(video_path)

    for sr_nr,row in annotations.iterrows():
        output_path = os.path.join(subfolder,f"{sr_nr}.mp4")

        if not os.path.isfile(output_path):
            cropped = video.subclip(frame_to_timestamp(row["start"],fps),frame_to_timestamp(row["end"],fps))
            cropped.write_videofile(output_path)



if __name__ == "__main__":

    video_dir = "C:/Users/Julius/OneDrive - bwedu/Studium/Bachelor/07_BA/Bachelorarbeit/Data/MTL-AQA/MTL-AQA_dataset_release/video_downloads"
    cropped_videos_dir = "C:/Users/Julius/OneDrive - bwedu/Studium/Bachelor/07_BA/Bachelorarbeit/Data/MTL-AQA/MTL-AQA_dataset_release/cropped_videos"

    raw_annotations_dir = "C:/Users/Julius/OneDrive - bwedu/Studium/Bachelor/07_BA/Bachelorarbeit/Data/MTL-AQA/MTL-AQA_dataset_release/JJ_used_Annotations"
    encode_raw_annotations = os.fsencode(raw_annotations_dir)
    
    for file in os.listdir(encode_raw_annotations):
        filename = os.fsdecode(file)
        if filename.endswith(".xlsx"): 
            annotation_path = os.path.join(raw_annotations_dir, filename)
            
            create_subclips(annotation_path,video_path=os.path.join(video_dir,filename.split(".")[0]+".mp4"),result_folder=cropped_videos_dir)
