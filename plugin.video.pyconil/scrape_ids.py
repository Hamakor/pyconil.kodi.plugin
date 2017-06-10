import urllib2
import json

pyconil_channel = "UC8ApA9ibgkf0XK7lgTVZgEQ"
YT_API = 'https://www.googleapis.com/youtube/v3'

if (0):
    my_key = raw_input("Type API Key: ")
    cmd = "{base}/playlists?part=snippet&channelId={chan}&key={key}".format(
        base=YT_API, chan=pyconil_channel, key=my_key)
    
    data = json.loads(urllib2.urlopen(cmd).read())
    playlists = [x["id"] for x in data["items"]]

if (0):
    videos = []
    for playlist in playlists:
        cmd = "{base}/playlistItems?part=contentDetails&playlistId={pl}&maxResults=50&key={key}".format(
            base=YT_API, pl=playlist, key=my_key)
        data = json.loads(urllib2.urlopen(cmd).read())
        print len(data["items"]), data["pageInfo"]["totalResults"]
        videos.extend([item["contentDetails"]["videoId"] for item in data["items"]])

if (0):
    titles = []
    descs = []
    for vid in videos:
        cmd = "{base}/videos?part=snippet&id={vid}&key={key}".format(
            base=YT_API, vid=vid, key=my_key)
        data = json.loads(urllib2.urlopen(cmd).read())
        titles.append(data["items"][0]["snippet"]["title"])
        print titles[-1]
        descs.append(data["items"][0]["snippet"]["description"])

if (0):
    manual = dict([
        (3, u"bH7UAQ3YKCk"),
        (4, u"99vpXHasxuI"),
        (14, u"LakHpMkEXKk"),
        (24, u"QGHz5TwvpDY"),
        (29, u"lIDVIQht_xs"),
        (41, u"tEu624QSYYo"),
        (42, u"BcdNe6b1lyM"),
        (45, u"1vwv5TeItm8")
        ])

if (0):
    #ed = EventData()
    event_video = {}
    for event in ed.eventdb.values():
        if not event["speakers"]: continue
        
        eid = event["eventId"]
        name = event["name"]
        res = [i for i,x in enumerate(titles) if x.lower().startswith(name.lower())]
        if len(res)==1:
            print "--"
            event_video[eid] = videos[res[0]]
        else:
            assert len(res)==0
            if eid in manual:
                event_video[eid] = manual[eid]
                print "--<"
            else:
                print eid, name
