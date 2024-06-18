import logging
import json

import speech_recognition as sr

class ExtractTextFromAudioProcessor():
    def __init__(self):
        self.payload=self.ingest_payload()
        return

    def ingest_payload(self):
        with open('payload.json')as f:
            self.payload = json.load(f)
        self.audioFileNames = (self.payload['audioFileNames'])
        return self.payload

    def run(self):


        """
        ****  Run the step ****
        """
        r=sr.Recognizer()
        audiotext=""
        for i in range(len(self.audioFileNames)):
            print(self.audioFileNames[i])

            audiofile=sr.AudioFile(self.audioFileNames[i])
            with audiofile as source:
                audio=r.record(source)

            try:
                temptext=r.recognize_google(audio)
                audiotext+=temptext
                print(audiotext)

            except sr.UnknownValueError:
                print("Cannot transcribe")
                pass

        self.payload['audioTranscribed'] = str(audiotext)
        self.output_payload()
        return

    def output_payload(self):
        with open('payload.json','w')as outputfile:
            json.dump(self.payload,outputfile)