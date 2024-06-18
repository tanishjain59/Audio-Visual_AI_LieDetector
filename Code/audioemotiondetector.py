import logging
import json

from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import pickle
from keras import backend as K

class ExtractEmotionFromAudioProcessor():
    def __init__(self):
        self.payload = self.ingest_payload()
        self.model=load_model('NN_Models/sentimentanalyzer.h5')
        self.tokenizer=self.load_tokenizer()

    def ingest_payload(self):
        with open('payload.json')as f:
            self.payload = json.load(f)
        self.text=self.payload['audioTranscribed']
        return self.payload


    def load_tokenizer(self):
        file = open('NN_Models/tokenizer.pkl', 'rb')
        return pickle.load(file)

    def decode_sentiment(self, score, include_neutral=True):
        if include_neutral:
            label = "NEUTRAL"
            if score <= 0.4:
                label = "NEGATIVE"
            elif score >= 0.7:
                label = "POSITIVE"

            return label
        else:
            return "NEGATIVE" if score < 0.5 else "POSITIVE"

    def predict(self, text,include_neutral=True):

        # Tokenize text
        x_test = pad_sequences(self.tokenizer.texts_to_sequences([text]), maxlen=300)
        # Predict
        score = self.model.predict([x_test])[0]
        # Decode sentiment
        label = self.decode_sentiment(score, include_neutral=include_neutral)

        return {"label": label, "score": float(score)}

    def analyzemessage(self,sentence):
        result = self.predict(sentence)
        return result["label"]


    def run(self):
        self.ingest_payload()
        sentences=self.text.split('.')
        emotion={}
        for i in range(len(sentences)):
            label=self.analyzemessage(sentences[i])
            emotion[i]=label
        self.payload['audioEmotion']=emotion

        """
        ****  Run the step ****
        """

        self.output_payload()
        return

    def output_payload(self):
        with open('payload.json','w')as f:
            json.dump(self.payload,f)