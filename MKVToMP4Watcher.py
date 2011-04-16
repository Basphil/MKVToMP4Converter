import pyinotify 
import MKVtoMP4Converter as converter

wm = pyinotify.WatchManager()

mask = pyinotify.IN_MOVED_TO | pyinotify.IN_CREATE# watched events

class EventHandler(pyinotify.ProcessEvent):
    
    def process_IN_MOVED_TO(self, event):
        print "Moved:"+event.pathname
        if event.pathname[-3:]=='mkv':
            print 'Starting conversion of %s' % event.pathname
            converter.convert(event.pathname)
            print 'Done.'
            
            
    def process_IN_CREATE(self, event):
        print "Created:"+event.pathname
    
    
    
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

wdd = wm.add_watch('/media/mediadisk/files', mask, rec=True, auto_add=True)
notifier.loop()



