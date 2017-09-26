#import rpdb2 
#rpdb2.start_embedded_debugger('pw')

import sys
import urllib, urlparse
import xbmc, xbmcgui, xbmcplugin
import html2text, dateutil.parser
import content

YT_VIDEO = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid={0}"
YT_PLAYLIST = "plugin://plugin.video.youtube/?path=/root/video&action=play_all&playlist={0}"
YT_IMG = "https://i.ytimg.com/vi/{0}/hqdefault.jpg"

xbmc.log("ADDON CALLED ---> argv="+str(sys.argv),xbmc.LOGNOTICE)

_url = sys.argv[0]
_handle = int(sys.argv[1])

def get_params(arg):
    qs = arg[1:] if arg.startswith("?") else arg
    d = urlparse.parse_qs(qs)
    if not all([len(x)==1 for x in d.itervalues()]):
        raise ValueError("Duplicate key in query string: "+qs)
    return {k:v[0] for k,v in d.iteritems()}

_params = get_params(sys.argv[2])

xbmc.log("ADDON CALLED ---> url={0} : handle={1} : params={2}".format(
    _url, _handle, _params), xbmc.LOGNOTICE)

_data = None

def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urllib.urlencode(kwargs))


def _add_main_item(title, url, is_folder=True):
    "helper for main_menu"
    li = xbmcgui.ListItem(title)
    xbmcplugin.addDirectoryItem(handle=_handle, url=url, listitem=li, isFolder=is_folder)
    
def main_menu():
    _add_main_item('Speakers 2016', get_url(action="speakers_menu"))
    _add_main_item('More Videos', get_url(action="videos_menu"))
    xbmcplugin.endOfDirectory(_handle)


def _fullname(speaker):
    return ' '.join([speaker["firstName"].rstrip(), speaker["lastName"]])

def _speaker_fullname(sid):
    global _data
    return _fullname(_data.speakerdb[int(sid)])

def speakers_menu(params):
    global _data
    xbmcplugin.setContent(_handle, 'movies') #movies tvshows episodes musicvideos
    
    for sid, speaker in _data.speakerdb.iteritems():
        li = xbmcgui.ListItem(_fullname(speaker))
        li.setArt({
            "poster": speaker["avatarImageURL"],
            "icon": speaker["avatarImageURL"]
            })
        li.setInfo("video", {"plot": html2text.html2text(speaker["characteristic"])})
        
        url = get_url(action="speaker_talks", speakerId=sid)
        xbmcplugin.addDirectoryItem(handle=_handle, url=url, listitem=li, isFolder=True)
    
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL)
    xbmcplugin.endOfDirectory(_handle)

def speaker_talks(params):
    global _data
    sid = int(params["speakerId"])
    xbmcplugin.setContent(_handle, 'movies') #movies tvshows episodes musicvideos

    for eid in _data.speaker_events.get(sid,[]):
        event = _data.eventdb[eid]
        frdate = dateutil.parser.parse(event["from"])
        li = xbmcgui.ListItem(event["name"])
        li.setInfo("video", {
            "title": event["name"],
            "plot": html2text.html2text(event["text"]),
            "premiered": frdate.strftime("%Y-%m-%d %H:%M"),
            "date": frdate.strftime("%d.%m.%Y")
            })
        youtubeid = event.get("link")
        if not youtubeid:
            url = get_url(action="no_video", eventId=eid)
            xbmcplugin.addDirectoryItem(handle=_handle, url=url, listitem=li, isFolder=False)
        else:
            #TODO do we need IsPlayable?
            li.setArt({
                "icon": YT_IMG.format(youtubeid),
                "poster": YT_IMG.format(youtubeid)
                })
            li.setProperty('IsPlayable', 'true')
            url = YT_VIDEO.format(youtubeid)
            xbmc.log("ADDON ---> adding url: ".format(url), xbmc.LOGNOTICE)
            xbmcplugin.addDirectoryItem(
                handle=_handle, url=url, listitem=li, isFolder=False)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_DATE_TAKEN)
    xbmcplugin.endOfDirectory(_handle)

def no_video(params):
    xbmcgui.Dialog().ok(
        "No Video found",
        u'No video found for talk: "{0}"'.format(
            _data.eventdb[int(params["eventId"])]["name"])
    )

def videos_menu(params):
    #xbmcplugin.setContent(_handle, 'movies')
    
    li = xbmcgui.ListItem('2016 Keynote: Travis Oliphant')
    li.setProperty('IsPlayable', 'true')
    xbmcplugin.addDirectoryItem(handle=_handle, url='plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=bH7UAQ3YKCk', listitem=li) # isfolder=False
    li2 = xbmcgui.ListItem('Big Buck Bunny')
    xbmcplugin.addDirectoryItem(handle=_handle, url='rtsp://mpv.cdn3.bigCDN.com:554/bigCDN/_definst_/mp4:bigbuckbunnyiphone_400.mp4', listitem=li2)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

_action_table = {
    "videos_menu": videos_menu,
    "speakers_menu":  speakers_menu,
    "speaker_talks":  speaker_talks,
    "no_video":  no_video
    }

def route_action(params):
    """
    Router function that calls other functions
    depending on the provided paramstring
    """
    if not params:
        main_menu()
    else:
        try:
            xbmc.log("ADDON ---> Access actiontable: {0}, {1}".format(_action_table, params["action"]), xbmc.LOGNOTICE)
            action = _action_table[params["action"]]
            #xbmc.log("ADDON ---> calling", xbmc.LOGNOTICE)
            action(params)
            #xbmc.log("ADDON ---> after calling", xbmc.LOGNOTICE)
        except KeyError:
            raise ValueError('Invalid params: ' + str(params))
    
if __name__ == '__main__':
    if _data is None:
        import os.path, cPickle, tempfile
        cachepath = os.path.join(tempfile.gettempdir(),"confdata.pickle")
        if (os.path.isfile(cachepath)):
            xbmc.log("ADDON ---> Rereading from file...", xbmc.LOGNOTICE)
            _data = cPickle.load(open(cachepath))
        else:
            xbmc.log("ADDON ---> Rereading via API...", xbmc.LOGNOTICE)
            _data = content.EventData()
            cPickle.dump(_data, open(cachepath,"w"))
    else:
        xbmc.log("ADDON ---> EventData not empty", xbmc.LOGNOTICE)
        
    route_action(_params)
