#import rpdb2 
#rpdb2.start_embedded_debugger('pw')

import sys
import urllib, urlparse
import xbmc, xbmcgui, xbmcaddon, xbmcplugin

xbmc.log("ADDON CALLED ---> argv="+str(sys.argv), xbmc.LOGNOTICE)

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

def get_params(arg):
    qs = arg[1:] if arg.startswith("?") else arg
    d = urlparse.parse_qs(qs)
    # TODO: find out why the values are all inside lists of length 1
    # for now: just extract the strings
    return {k:v[0] for k,v in d.iteritems()}

# Get the "query" part of the URL (action and arguments)
_params = get_params(sys.argv[2])

xbmc.log("ADDON CALLED ---> url={0} : handle={1} : params={2}".format(
    _url, _handle, _params), xbmc.LOGNOTICE)

_addonname   = xbmcaddon.Addon().getAddonInfo('name')

def get_url(**kwargs):
    """
    TODO: add credits
    Create a URL for calling the plugin recursively from the given set of keyword arguments.
    """
    return '{0}?{1}'.format(_url, urllib.urlencode(kwargs))

def _add_main_item(title, url, is_folder):
    "helper for main_menu"
    li = xbmcgui.ListItem(title)
    xbmcplugin.addDirectoryItem(handle=_handle, url=url, listitem=li, isFolder=is_folder)
    
def main_menu():
    _add_main_item('Speakers 2016', get_url(action="speakers16"), True)
    _add_main_item('Test Videos', get_url(action="videos"), True)
    xbmcplugin.endOfDirectory(_handle)


def vid_menu(params):
    """
    Videos menu (from stage 3)
    """
    # Following affect the display. Available types: movies, tvshows, episodes, musicvideos
    #xbmcplugin.setContent(_handle, 'movies')
    
    li = xbmcgui.ListItem('My First Video!', iconImage='DefaultVideo.png') # from the theme
    # Change the following address to some path on your disk
    xbmcplugin.addDirectoryItem(handle=_handle, url='C:/Users/aaronovitch/Downloads/cbi-208-video.m4v', listitem=li)
    li2 = xbmcgui.ListItem('My second Video!', iconImage='DefaultVideo.png')
    xbmcplugin.addDirectoryItem(handle=_handle, url='rtsp://mpv.cdn3.bigCDN.com:554/bigCDN/_definst_/mp4:bigbuckbunnyiphone_400.mp4', listitem=li2)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

def speakers_menu(params):
    xbmcgui.Dialog().ok(
        _addonname,
        "Speakers menu clicked - not supported yet"
    )

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
