#import rpdb2 
#rpdb2.start_embedded_debugger('pw')

import sys
import urllib, urlparse
import xbmc, xbmcgui, xbmcplugin

import content

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
    _add_main_item('Speakers 2016', get_url(action="speakers16"))
    _add_main_item('Test Videos', get_url(action="videos"))
    xbmcplugin.endOfDirectory(_handle)


def _fullname(speaker):
    return ' '.join([speaker["firstName"].rstrip(), speaker["lastName"]])

def _speaker_fullname(sid):
    global _data
    return _fullname(_data.speakerdb[int(sid)])

def speakers_menu(params):
    global _data
    xbmcplugin.setContent(_handle, 'movies')
    for sid, speaker in _data.speakerdb.iteritems():
        li = xbmcgui.ListItem(_fullname(speaker))
        url = get_url(action="speaker_talks", speakerId=sid)
        xbmcplugin.addDirectoryItem(handle=_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(_handle)

def speaker_talks(params):
    global _data
    xbmcgui.Dialog().ok(
        "Speaker talks popup",
        u"Speakers talks for {0} - not supported yet".format(_speaker_fullname(params["speakerId"]))
    )

def vid_menu(params):
    #xbmcplugin.setContent(_handle, 'movies')
    
    li = xbmcgui.ListItem('My First Video!')
    xbmcplugin.addDirectoryItem(handle=_handle, url='/media/elements/media/pipi.mp4', listitem=li) # isfolder=False
    li2 = xbmcgui.ListItem('My second Video!')
    xbmcplugin.addDirectoryItem(handle=_handle, url='rtsp://mpv.cdn3.bigCDN.com:554/bigCDN/_definst_/mp4:bigbuckbunnyiphone_400.mp4', listitem=li2)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

_action_table = {
    "videos": vid_menu,
    "speakers16":  speakers_menu,
    "speaker_talks":  speaker_talks
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
            xbmc.log("ADDON ---> calling", xbmc.LOGNOTICE)
            action(params)
            xbmc.log("ADDON ---> after calling", xbmc.LOGNOTICE)
        except KeyError:
            raise ValueError('Invalid params: ' + str(params))
    
if __name__ == '__main__':
    if _data is None:
        import os.path, cPickle
        if (os.path.isfile("/tmp/confdata.pickle")):
            xbmc.log("ADDON ---> Rereading from file...", xbmc.LOGNOTICE)
            _data = cPickle.load(open("/tmp/confdata.pickle"))
        else:
            xbmc.log("ADDON ---> Rereading via API...", xbmc.LOGNOTICE)
            _data = content.EventData()
            cPickle.dump(_data, open("/tmp/confdata.pickle","w"))
    else:
        xbmc.log("ADDON ---> EventData not empty", xbmc.LOGNOTICE)
        
    route_action(_params)
