from pydub import AudioSegment
import math
import json

class AudioSplitter():
    def __init__(self):
        self.payload=self.ingestpayload()

    def ingestpayload(self):
        with open('payload.json')as f:
            self.payload=json.load(f)
        self.audiofilename = str(self.payload['audioFileName'])
        self.audio = AudioSegment.from_wav(self.audiofilename)
        return self.payload

    def getduration(self):
        return self.audio.duration_seconds


    def singlesplit(self,from_min,to_min,split_filename):
        t1=from_min*60*1000
        t2=to_min*60*1000
        split_audio=self.audio[t1:t2]
        split_audio.export(split_filename,format="wav")

    def multiple_split(self,min_per_split):
        total_minutes=math.ceil(self.getduration()/60)
        filenames=[]
        for i in range(0,total_minutes,min_per_split):
            split_fn=str(i)+"_"+self.audiofilename
            filenames.append(split_fn)
            self.singlesplit(i,i+min_per_split,split_fn)
            print(str(i)+'Done')

            if i==total_minutes-min_per_split:
                print("All splitted successfully")
        self.audiofilenames = filenames


    def outputpayload(self):
        with open ('payload.json','w')as f:
            payload=self.payload
            payload['audioFileNames']=self.audiofilenames
            json.dump(self.payload,f)

    def run(self):
        splitwav=self.multiple_split(min_per_split=1)
        self.outputpayload()


