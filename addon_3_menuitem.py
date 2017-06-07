#import rpdb2 
#rpdb2.start_embedded_debugger('pw')

import xbmc, xbmcgui, xbmcplugin

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

xbmc.log(str(sys.argv), xbmc.LOGNOTICE)

# Following affect the display. Available types: movies, tvshows, episodes, musicvideos
#xbmcplugin.setContent(_handle, 'movies')

li = xbmcgui.ListItem('My First Video!', iconImage='DefaultVideo.png') # from the theme
# Change the following address to some path on your disk
xbmcplugin.addDirectoryItem(handle=_handle, url='/media/elements/media/pipi.mp4', listitem=li)
li2 = xbmcgui.ListItem('My second Video!', iconImage='DefaultVideo.png')
xbmcplugin.addDirectoryItem(handle=_handle, url='rtsp://mpv.cdn3.bigCDN.com:554/bigCDN/_definst_/mp4:bigbuckbunnyiphone_400.mp4', listitem=li2)

xbmcplugin.endOfDirectory(_handle)
