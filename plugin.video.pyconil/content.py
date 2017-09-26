import sys, os.path
import json
from urllib2 import urlopen

#TODO: read _old and the API uri from config

#API_2016 = "http://pycon-il.s3-website-us-east-1.amazonaws.com/api/v1/{command}.js"; _old=True
#API_2016 = "http://localhost:8080/api/pyconil2016_old/{command}.js"; _old=True
#API_2016 = "http://localhost:8080/api/pyconil2016/{command}"; _old=False
#API_2016 = "http://wiki.python.org.il:9090/api/pyconil2016_old/{command}.js"; _old=True
API_2016 = "http://wiki.python.org.il:9090/api/pyconil2016/{command}"; _old=False

this_dir = os.path.dirname(os.path.abspath(__file__))


def api_cmd(cmd):
    url = API_2016.format(command=cmd)
    return json.load(urlopen(url))

def prt_speaker(spk):
    print spk["firstName"], spk["lastName"], spk["avatarImageURL"]
    print spk["characteristic"]

class EventData(object):
    def __init__(self):
        sp = api_cmd("getSpeakers")
        self.speakerdb = {x["speakerId"]: x for x in sp["speakers"]}
        self.days = api_cmd("getSessions")["days"]
        if _old:
            self.vid_data = json.load(open(os.path.join(this_dir, "event_video.json")))
        self._load_data()
    
    def _load_data(self):
        self.eventdb = {}
        for day in self.days:
            for event in day["events"]:
                self.eventdb[event["eventId"]] = event
        
        self.speaker_events = {}
        for eid,event in self.eventdb.iteritems():
            for speaker in event["speakers"]:
                self.speaker_events.setdefault(speaker, []).append(eid)

        if _old:
            self.event_video = {
                int(eid): vid
                for eid,vid in self.vid_data.iteritems()}
            #
            for eid,vid in self.vid_data.iteritems():
                self.eventdb[int(eid)]["link"] = vid

if (0):
    ed = EventData()
    
if (0):
    sessions = api_cmd("getSessions")
    sp = api_cmd("getSpeakers")
    speakerdb = {x["speakerId"]: x for x in sp["speakers"]}
    
    days = sessions["days"]
    for day in days:
        print "date:", day["date"]
        for event in day["events"][:3]:
            print event["eventId"], event["track"], event["name"], event["place"]
            print event["place"], ":", event["from"], "-", event["to"]
            print "speakers:", [id_ for id_ in event["speakers"]]
            for s in event["speakers"]:
                print "--"
                prt_speaker(speakerdb[s])
            print event["text"]#event["description"]
            print "========================="

