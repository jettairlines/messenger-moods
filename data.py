from HTMLParser import HTMLParser
import nltk
nltk.download()
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import operator
import datetime
import json

month_dict = {"January":1,"February":2,"March":3,"April":4, "May":5, "June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}

quotes = []
times = []

class AllLanguages(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.msgcount = 0
        self.jw = False
        self.lasttag = None
        self.lastclass = None

    def handle_starttag(self, tag, attrs):
    	##print ">seen " + tag
        self.lasttag = tag
        self.lastclass = None
        for name, value in attrs:
            if name == 'class':
            	self.lastclass = value
            	##print ">>of class " + value
            	

    def handle_data(self, data):
    	global datas
    	if self.lasttag == 'span' and self.lastclass == 'user':
        	if data == 'Jett Wang':
        		self.jw = True
        	else:
        		self.jw = False
        if self.lasttag == 'span' and self.lastclass == 'meta' and self.jw:
        	times.append(data)
        if self.lasttag == 'p' and self.jw:
        	self.jw = False
        	quotes.append(data);
        
myfile = open('messages.htm', 'r').read()
parser = AllLanguages()
parser.feed(myfile)

datas = dict(zip(times, quotes))
result = {}
# result_daily = {'neu':0,'pos':0,'neg':0,'compound':0}



sid = SentimentIntensityAnalyzer()
for time, quote in datas.iteritems():
	 ## handling time stamps
     time = time.replace(',','').split()
     # time = time[1] + time[2] + time[3]
     time = datetime.datetime(int(time[3]),month_dict[time[1]],int(time[2])).date().strftime('%Y-%m-%d')

     # print(quote)
     scores = sid.polarity_scores(quote)
     scoresum = sum(scores.itervalues())
     if scoresum == 0:
     	continue
     ## :'^)
     scores['neu'] = 0
     ## convert to proportions
     for cat in scores:
     	# print('{0}: {1}, '.format(cat, scores[cat]))
     	scores[cat] /= scoresum
    
     highest = max(scores.iteritems(), key=operator.itemgetter(1))[0]

     # if not result.get(time):
     # 	result[time] = result_daily
     # else:
     # 	result[time][highest]+=1

     if not result.has_key(time):
     	result[time] = scores
     else:
     	for cat,score in scores.iteritems():
     		result[time][cat]+=scores[cat]

for time,res in result.iteritems():
	result[time] = max(result[time].iteritems(), key=operator.itemgetter(1))[0]
# result = sorted(result)

values = [{"date": k, "mood": v} for k, v in result.items()]
with open('data.js', 'r+') as outfile:
	content = outfile.read()
	outfile.seek(0, 0)
	outfile.write("var data = ")
	json.dump(values, outfile, indent=4)
	
print "data parsing complete ¯\_(ツ)_/¯"