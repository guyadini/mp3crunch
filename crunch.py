#!/usr/bin/python
#-------------------------------------------------------------------------------
# Name:        crunch
#
# Author:      guy
#
# Created:     06/01/2012

#-------------------------------------------------------------------------------

import os
import sys
#tagger is the project pytagger. Get it from http://www.liquidx.net/pytagger/
from tagger import *

#TALB - album
#TPE1 - artist
#TIT2 - title.
#TRCK - track number.


def convertTags(file,paramsDict):
    try:
        tag = ID3v2(file)
        framesDict = {x.fid : x for x in tag.frames}
        for fid, s in [
                ('TALB',paramsDict['album']),
                ('TPE1',paramsDict['artist'])
                ]:
            if fid in framesDict: frame = framesDict[fid]
            else:
                frame = tag.new_frame(fid)
                tag.frames.append(frame)
            frame.set_text(s,encoding='latin_1')
        tag.commit()
        if inDictAndTrue('print',paramDict): print 'commited successfully'
    except Exception as e:
        print 'Failed to write %s, with exception %s' %(file,e)



def inDictAndTrue(k,d):
    if k in d and d[k]==True:
        return True
    else: return False

def nonAscii(s):
    if max([ord(c) for c in s])>0x7E: return True
    else: return False

def mapIfAscii(items,rootDir,f,paramDict):
    if not f: return
    for i in items:
        if nonAscii(i): continue
        f(rootDir,i,paramDict)

def mapIfMp3(items,rootDir,f,paramDict):
    if not f: return
    for i in items:
        if len(i)<4 or i[-4:].lower()!='.mp3': continue
        f(rootDir,i,paramDict)


def crunch(rootDir,paramDict=None,fDirs=None,fFiles=None):
    '''Apply fDir(**kwargs) to all the subdirectories of rootDir,
    and fFile(**kwargs) to all the files in the directory'''
    w = os.walk(rootDir)
    rootDir,dirs,files = w.next()
    mapIfAscii(dirs,rootDir,fDirs,paramDict)
    mapIfMp3(files,rootDir,fFiles,paramDict)


def applyFileTags(root,f,paramDict):
    artist = paramDict['artist']
    album = paramDict['album']
    if inDictAndTrue('print',paramDict): print '%s: Artist: %s, album: %s' %(f,artist,album)
    if inDictAndTrue('convertTags',paramDict):
        convertTags(os.path.join(root,f),paramDict)

def setArtistTag(root,d,paramDict=None):
    pDict=paramDict.copy()
    pDict['artist']=d
    crunch(os.path.join(root,d),pDict,setAlbumTag)

def setAlbumTag(root,d,paramDict,):
    if inDictAndTrue('print',paramDict): print '='*50
    pDict = paramDict.copy()
    pDict['album']=d
    crunch(os.path.join(root,d),pDict,fDirs=None,fFiles=applyFileTags)


def crunchRoot(rootDir,paramDict=None):
    crunch(rootDir,paramDict,fDirs=setArtistTag)

if __name__ == '__main__':
    if len(sys.argv)<2:
        rootDir='.'
        #rootDir=r'C:\Users\guy\Music\Collection' #for testing
    else: rootDir=sys.argv[1]
    #TODO - read these parameters from the command line
    paramDict ={'print' : True, 'convertTags' : False}
    crunchRoot(rootDir,paramDict)
