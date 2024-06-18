import os
import logging

from datetime import datetime
import json
from moviepy.editor import VideoFileClip

class SplitMediaProcessor():
    def __init__(self):
        # self.config = config
        self.payload=self.ingest_payload()
        return

    def de_multiplexer(self, input_file_name):
        self.audio_file_name = input_file_name[:-3]+'wav'
        self.video_file_name = input_file_name

        video = VideoFileClip(input_file_name)
        video.audio.write_audiofile(self.audio_file_name)


        return

    def ingest_payload(self):
        with open('payload.json')as f:
            self.payload=json.load(f)
        self.input_file_name=str(self.payload['sessionId'])+'.mp4'
        return self.payload

    def output_payload(self):
        with open('payload.json')as f:
            self.payload=json.load(f)
        self.payload['audioFileName']=self.audio_file_name
        self.payload['videoFileName']=self.video_file_name
        f.close()
        with open('payload.json','w')as outfile:
            json.dump(self.payload,outfile)


    def run(self):
        self.ingest_payload()

        """
        ****  Run the step ****
        """

        session_id = self.payload["sessionId"]
        live_video_file_name = f"{session_id}.mp4"
        logging.info(f"Invoking ffmpeg video/audio splitter... Input Live video file = live_video_file_name; ")

        start_time = datetime.now()

        self.de_multiplexer(live_video_file_name)
        logging.info(f"Split parts: video = {self.video_file_name}; audio = {self.audio_file_name}")

        end_time = datetime.now()

        logging.info(f"Start Time   : {start_time}")
        logging.info(f"End Time     : {end_time}")
        logging.info(f"Elapsed Time : {(end_time - start_time)}")

        # **** Output the payload data for the next step ****
        self.payload["videoFileName"] = self.video_file_name
        self.payload["audioFileName"] = self.audio_file_name
        self.output_payload()
        return
