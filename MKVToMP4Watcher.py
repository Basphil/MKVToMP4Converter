## MKVToMP4Watcher: Programm that uses pyinotify to run MKVToMP4Converter 
## on .mkv files moved to, or created in the watched directory.

## Source code and additional information at 
## https://github.com/Basphil/MKVToMP4Converter

## Copyright (C) 2011  Basil Philipp <basil.philipp@gmail.com>

## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
MKVToMP4Watcher

@author: Basil Philipp
@license: GPLv3
@contact: basil.philipp@gmail.com
"""



import pyinotify 
import MKVToMP4Converter as converter
import sys
from optparse import OptionParser
import sendmail

usage = 'usage: python %prog [options] [Path of directory to watch] \n If no directory to watch is provided, the current directory will be watched.'
parser = OptionParser(usage=usage)

parser.add_option('-e', '--email',
                    action='store_true', dest='email', default=False, help='send an e-mail when an event occurs. %default by default')

(options, args) = parser.parse_args()

if len(args) == 1:
    directory = args[0]

elif len(args)>1:
    print 'incorrect number of arguments'
    sys.exit(2)


if options.email:
    mail = sendmail.SendMail()
    print 'e-mail option set'


wm = pyinotify.WatchManager()
flags = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_TO

class EventHandler(pyinotify.ProcessEvent):
    
    def process_IN_CLOSE_WRITE(self, event):
        print "Finished writing:"+event.pathname
        if event.pathname[-3:]=='mkv':
            print 'Starting conversion of %s' % event.pathname
            converter.convert(event.pathname)
            print 'Done.\n' 

            if options.email: 
                mail.send(event.pathname)
        else:
            if options.email:
                mail.send(event.pathname)

    def process_IN_MOVED_TO(self, event):
        print "Moved: "+event.pathname
        if event.pathname[-3:]=='mkv':
            print 'Starting conversion of %s' % event.pathname
            converter.convert(event.pathname)
            print 'Done.\n' 

            if options.email:
                mail.send(event.pathname)

        else:
            if options.email:
                mail.send(event.pathname)
        
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)

wdd = wm.add_watch(directory, flags, rec=True, auto_add=True)
notifier.loop()

