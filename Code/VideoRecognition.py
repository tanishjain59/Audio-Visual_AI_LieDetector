import logging
import json
import cv2
import time
from keras.models import load_model
import numpy as np


class ExtractEmotionFromVideoProcessor():
    def __init__(self):
        self.payload = self.ingest_payload()
        self.model=load_model('NN_Models/Fer2013.hdf5')

    def ingest_payload(self):
        with open('payload.json')as f:
            self.payload = json.load(f)

        return self.payload

    def extractframes(self):
        capture=cv2.VideoCapture(self.payload['videoFileName'])
        prev=0
        i=0
        '''
        Change the sample size here to alter the sampling rate
        '''
        frame_sample_size=10
        filenames=[]
        while capture.isOpened():
            time_elapsed=time.time()-prev
            ret,frame=capture.read()
            if not ret:
                break
            if time_elapsed>1./frame_sample_size:
                prev=time.time()
                filename=self.payload['videoFileName']+"_"+str(i)+".jpg"
                filenames.append(filename)
                cv2.imwrite(filename,frame)
                i+=1
                continue
        self.payload['videoFrames']=filenames
        print(self.payload)
        capture.release()

    def output_payload(self):
        with open('payload.json','w')as outfile:
            json.dump(self.payload,outfile)
        return

    def extract_emotion(self):
        emotions={}
        classes = np.array(("Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"))
        for i in range(len(self.payload['videoFrames'])):
            print(self.payload['videoFrames'][i])
            image=cv2.imread(self.payload['videoFrames'][i])
            image=cv2.resize(image,(48,48))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            print("Predicting Emotion....")
            predictions=self.model.predict(image.reshape(-1,48,48,1))
            print(predictions)
            print("Emotion calculated....")
            finalprediction=classes[np.argmax(predictions)]
            emotions[i]=finalprediction
        self.payload['videoEmotions']=emotions





    def run(self):
        self.ingest_payload()
        self.extractframes()

        self.extract_emotion()
        self.output_payload()
        return
