#import rpdb2 
#rpdb2.start_embedded_debugger('pw')

import sys
import urllib, urlparse
import xbmc, xbmcgui, xbmcplugin

import content

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


def speakers_menu(params):
    pass

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
    "speakers16":  speakers_menu
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
            action = _action_table[params["action"]]
            action(params)
        except KeyError:
            raise ValueError('Invalid params: ' + str(params))
    
if __name__ == '__main__':
    data = content.EventData()
    route_action(_params)
