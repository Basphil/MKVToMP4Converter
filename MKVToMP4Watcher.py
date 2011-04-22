import pyinotify 
import MKVToMP4Converter as converter
import sys

directory = sys.argv[1]
wm = pyinotify.WatchManager()
flags = pyinotify.IN_CLOSE_WRITE

class EventHandler(pyinotify.ProcessEvent):
    
    def process_IN_CLOSE_WRITE(self, event):
        print "Finished writing:"+event.pathname
        if event.pathname[-3:]=='mkv':
            print 'Starting conversion of %s' % event.pathname
            converter.convert(event.pathname)
            print 'Done.' 
    
    
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

wdd = wm.add_watch(directory, flags, rec=True, auto_add=True)
notifier.loop()

