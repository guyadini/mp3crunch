#!/usr/bin/python
#-------------------------------------------------------------------------------
# Name:        crunch
# Purpose:
#
# Author:      guy
#
# Created:     06/01/2012
# Copyright:   (c) guy 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import sys

def nonAscii(s):
    if max([ord(c) for c in s])>0x7E: return True
    else: return False

def mapIfAscii(items,rootDir,f,paramDict):
    if not f: return
    for i in items:
        if nonAscii(i): continue
        f(rootDir,i,paramDict)


def crunch(rootDir,paramDict=None,fDirs=None,fFiles=None):
    '''Apply fDir(**kwargs) to all the subdirectories of rootDir,
    and fFile(**kwargs) to all the files in the directory'''
    w = os.walk(rootDir)
    rootDir,dirs,files = w.next()
    mapIfAscii(dirs,rootDir,fDirs,paramDict)
    mapIfAscii(files,rootDir,fFiles,paramDict)


def applyFileTags(root,f,paramDict):
    artist = paramDict['artist']
    album = paramDict['album']
    print '%s: Artist: %s, album: %s' %(f,artist,album)

def setArtistTag(root,d,paramDict=None):
    pDict={'artist':d}
    crunch(os.path.join(root,d),pDict,setAlbumTag)

def setAlbumTag(root,d,paramDict,):
    print '='*20
    pDict = paramDict.copy()
    pDict['album']=d
    crunch(os.path.join(root,d),pDict,fDirs=None,fFiles=applyFileTags)


def crunchRoot(rootDir):
    crunch(rootDir,fDirs=setArtistTag)



if __name__ == '__main__':
    if len(sys.argv)<2:
        #rootDir='.'
        rootDir=r'C:\Users\guy\Music\Collection'
    else: rootDir=sys.argv[1]
    crunchRoot(rootDir)
