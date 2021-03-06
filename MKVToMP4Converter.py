## MKVToMP4Converter: Programm that uses a set of existing tools to convert
## .mkv files into .mp4 files.

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
MKVToMP4Converter

@author: Basil Philipp
@license: GPLv3
@contact: basil.philipp@gmail.com
"""



import subprocess,shlex, string, sys

def convert(path):    
    information = info(path)

    try:
        t_audio = find_audio_track(information)
    
        t_video = (t_audio == 1) and 2 or 1

        a_codec = audio_codec(information)

        fps = get_fps(information, t_video)

        ext_tracks(path, t_audio, t_video, a_codec)

        convert_audio(a_codec)

        box(path, fps)

        print 'Done'

    except ConversionError as e:
        print   e.value 
    print '-------------------------------\n'
def info(name):
    '''Returns the ouput of mkvinfo as a string'''
    
    command = 'mkvinfo '+name.lstrip()
    args = shlex.split(command)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = p.communicate()

    return stdout
    



def find_audio_track(info):
    '''Determines wether the audio track is track 1 or track 2. Returns the appropriate number.'''
    
    pos_audio = string.find(info, 'Track type: audio')
    pos_video = string.find(info, 'Track type: video')

    if pos_audio == -1 or pos_video == -1:
        raise ConversionError('Tracks could not be found. Possibly the wrong format (not a .mkv file) or a corrupt .mkv file.')
  

    return (pos_audio < pos_video) and 1 or 2


def audio_codec(info):
    '''Determins wether the audio type is aac or dts. Returns a string with the correct format.'''

    aac = string.find(info, 'Codec ID: A_AC3')

    if aac != -1:
        return 'aac'
    

    dts = string.find(info, 'Codec ID: A_DTS')

    if dts != -1:
        return 'dts'
    
#TODO: Error output
    else:
        raise ConversionError('The audio codec could not be determined')
        
    
 
def get_fps (info, t_video):
    '''Gets the fps from the mkvinfo string'''

    fps = ' fps for a video track)'
    if t_video == 1:
        pos = string.find(info, fps)

    else:
        pos = string.rfind(info, fps)

    return info[pos -6:pos]


def ext_tracks(name, t_audio, t_video, type_audio):
    '''Starts the command to extract the audio and the video track into separate files'''

    print '\nExtracting tracks'

    command = 'mkvextract tracks %s %s:movie.264 %s:sound.%s' % (name , t_video, t_audio, type_audio)
    args = shlex.split(command)
    print command

    #TODO: Loading sign or so.
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in iter(p.stdout.readline, ""):
        print line,
    

def convert_audio(type_audio):
    '''Converts dts to aac. Conversion is needed even if already extracted as aac, otherwise volume is too low'''
    
    #TODO Fix output, does not make a lot of sense when converting from aac to aac
    
    
    if cmp(type_audio, 'dts') == 0:
        print '\nConversion of sound.dts to sound_.aac'
        command = 'ffmpeg -i sound.%s -y -vn -acodec libfaac -ac 2 -ar 48000 -ab 160k sound_.aac' % type_audio

    else:
        print '\nAdjusting volume of sound.aac and saving to sound_.aac'
        command = 'ffmpeg -i sound.%s -y -vn -acodec libfaac -vol 900 -ac 2 -ar 48000 -ab 160k sound_.aac' % type_audio


    args = shlex.split(command)
    print command
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()


def box(name, fps):
    '''Boxes the sound and video file into an mp4'''
    filename = name[:-3]+'mp4'
    print "\nBoxing the extracted files into %s" % (filename)
    command = 'MP4Box -new %s -add movie.264 -add sound_.aac -fps %s' % (filename, fps)

    args = shlex.split(command)
    print command
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
  


if __name__ == '__main__':
    try:
        convert(sys.argv[1])

    except IndexError:
        print 'Usage: python MKVToMP4Converter.py [.mkv file to convert]'

class ConversionError(Exception):
    def __init__(self, value):
        self.value = 'ERROR: %s'%(value)

    def __str__(self):
        return self.value
