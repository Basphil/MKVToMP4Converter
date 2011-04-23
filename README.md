# MKVToMP4Converter
* License          : GPLv3
* Project URL      : [https://github.com/Basphil/MKVToMP4Converter](https://github.com/Basphil/MKVToMP4Converter)

This program allows you to convert an .mkv file into an .mp4 file. 
The program consists of two parts: MKVToMP4Watcher lets you watch a directory for new .mkv files and then
authomatically calls MKVToMP4Converter on those files. MKVToMP4Converter turns an .mkv file in a new .mp4 file.

All credit for the process of monitoring directories and making an .mp4 out of the .mkv file goes to the 
developpers behind the programms listed under 'Dependencies'. MKVToMP4Watcher and MKVToMP4Converter are just 
wrappers around these tools.

## Dependencies

* Linux ≥ 2.6.13
* Python ≥ 2.4
* [pyinotify](https://github.com/seb-m/pyinotify)
* [mkvtoolnix](http://www.bunkus.org/videotools/mkvtoolnix/)
* [FFmpeg](http://www.ffmpeg.org/)
* [MP4Box](http://gpac.wp.institut-telecom.fr/mp4box/) 


## Install

### Install the dependencies
Visit this page to learn how to [install the dependencies](https://github.com/Basphil/MKVToMP4Converter/wiki/Installation-of-the-dependencies).

### Install from git repository

    $ git clone git@github.com:Basphil/MKVToMP4Converter.git

## Usage

To watch a directory, download the code, install the dependencies and run this command from a shell:

    $ python MKVToMP4Watcher.py [Path of directory to watch]

Or to directly convert an .mkv file:

    $ python MKVToMP4Converter.py [.mkv file to convert]


If something does not work, have a look at the issues section of the project page. If the issue has
already been reported weigh in. If the issues is new please report it. If you haven't got a github account,
you can also drop me an e-mail.  
