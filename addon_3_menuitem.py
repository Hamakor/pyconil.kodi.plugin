import rpdb2 
rpdb2.start_embedded_debugger('pw')

import xbmc

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

xbmc.log("Hello", xbmc.LOGNOTICE)#xbmc.LOGDEBUG)
xbmc.log(str(sys.argv), xbmc.LOGNOTICE)

#xbmcplugin.setContent(_handle, 'movies') # see # content: files, songs, artists, albums, movies, tvshows, episodes, musicvideos # http://mirrors.kodi.tv/docs/python-docs/13.0-gotham/xbmcplugin.html # look in 17.0 docs

li = xbmcgui.ListItem('My First Video!', iconImage='resources/icon.png')
xbmcplugin.addDirectoryItem(handle=_handle, url='/media/elements/media/pipi.mp4', listitem=li)
li2 = xbmcgui.ListItem('My second Video!', iconImage='resources/icon2.png')
xbmcplugin.addDirectoryItem(handle=_handle, url='rtsp://mpv.cdn3.bigCDN.com:554/bigCDN/_definst_/mp4:bigbuckbunnyiphone_400.mp4', listitem=li2)

xbmcplugin.endOfDirectory(_handle)
