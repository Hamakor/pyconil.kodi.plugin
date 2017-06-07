import json
from urllib2 import urlopen

API_2016 = "http://pycon-il.s3-website-us-east-1.amazonaws.com/api/v1/{command}.js"

def api_cmd(cmd):
    url = API_2016.format(command=cmd)
    return json.loads( urlopen(url).read() )

def prt_speaker(spk):
    print spk["firstName"], spk["lastName"], spk["avatarImageURL"]
    print spk["characteristic"]

class EventData(object):
    def __init__(self):
        sp = api_cmd("getSpeakers")
        self.speakerdb = {x["speakerId"]: x for x in sp["speakers"]}
        self.days = api_cmd("getSessions")

if (0):
    ed = EventData()
    
if (0):
    #gs = api_cmd("getSessions")
    sp = api_cmd("getSpeakers")
    speakerdb = {x["speakerId"]: x for x in sp["speakers"]}
    
    days = gs["days"]
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

tracks = [
    #track 1
    {"name":"track1",
     "data": {
        "room":1,
        "talks":[
            {"name":"talk11",
             "speaker":"speaker1",
             "abstract":
"""
Abstract of talk11
"""
            },
            {"name":"talk12",
             "speaker":"speaker2",
             "abstract":
"""
Abstract of talk12
"""
            },
        ] #end talks
     } #end data
    },

    #track 2 
    {"name":"track2",
     "data": {
        "room":2,
        "talks":[
            {"name":"talk2",
             "speaker":"speaker3",
             "abstract":
"""
Abstract of talk2
"""
             },
        ] #end talks
     } # end data
    }
]
