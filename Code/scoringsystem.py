import json



class ScoringSystem():


    def __init__(self):
        self.payload=self.ingest_payload()


    def ingest_payload(self):
        with open('payload.json')as f:
            self.payload = json.load(f)

        return self.payload

    def run(self):
        self.aggregateemotions()
        self.videoemotionanalyzer()
        self.scoreanalyzer()
        self.output_payload()

    def aggregateemotions(self):

        self.audioemotions=self.payload['audioEmotion']
        self.videoemotions=self.payload['videoEmotions']
        audioemotioncats={}
        videoemotioncats={}
        print(self.audioemotions)
        print(self.videoemotions)
        for i in range(len([*self.audioemotions.keys()])):
            if self.audioemotions[str(i)]in audioemotioncats.keys():
                audioemotioncats[self.audioemotions[str(i)]]+=1
            else:
                audioemotioncats[self.audioemotions[str(i)]]=1

        for i in range(len([*self.videoemotions.keys()])):
            if self.videoemotions[str(i)]in videoemotioncats.keys():
                videoemotioncats[self.videoemotions[str(i)]]+=1
            else:
                videoemotioncats[self.videoemotions[str(i)]]=1

        self.payload['audioEmotionAggregates']=audioemotioncats
        self.payload['videoEmotionAggregates']=videoemotioncats

    def videoemotionanalyzer(self):
        self.videoemotions=self.payload['videoEmotions']
        initialscore=0
        self.report={}
        microexpressions=[]
        for i in range(len([*self.videoemotions.keys()])):
            if self.videoemotions[str(i)]==self.videoemotions[str(max((i-1),0))]:

                self.report[i]="No MicroExpression"
            elif self.videoemotions[str(i)]!=self.videoemotions[str(max((i-1),0))]:
                if self.videoemotions[str(i)] in microexpressions:
                    initialscore += (i / len([*self.videoemotions.keys()])) * 100
                    self.report[i]="MicroExpression Detected"
                else:
                    microexpressions.append(self.videoemotions[str(i)])
                    initialscore +=(i/len([*self.videoemotions.keys()]))*200
                    self.report[i]="No MicroExpression Detected"
        self.payload['result']=self.report
        self.payload['score']=initialscore

    def scoreanalyzer(self):
        if self.payload['score']>=500:
            self.payload['finalVerdict']="Strong Lie Detected"
        elif self.payload['score']>100 and self.payload['score']<500:
            self.payload['finalVerdict']="Moderate Lie Detected"
        else:
            self.payload['finalVerdict']="No Lie Detected"



    def output_payload(self):
        with open('payload.json','w')as f:
            json.dump(self.payload,f)
