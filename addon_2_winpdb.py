import xbmc

import rpdb2 
rpdb2.start_embedded_debugger('pw')

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

xbmc.log("Hello", xbmc.LOGNOTICE)#xbmc.LOGDEBUG)
xbmc.log(str(sys.argv), xbmc.LOGNOTICE)
