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


def printMsg(msg,paramDict={}, tagName=None):
    if paramDict and 'outputFunc' in paramDict:
        outParam = list(paramDict['printParams'])
        if tagName: outParam.append(tagName)
        paramDict['outputFunc'](msg,*outParam)
    else: print msg

def convertTags(file,paramDict):
    try:
        tag = ID3v2(file)
        framesDict = {x.fid : x for x in tag.frames}
        for fid, s in [
                ('TALB',paramDict['album']),
                ('TPE1',paramDict['artist'])
                ]:
            if fid in framesDict: frame = framesDict[fid]
            else:
                frame = tag.new_frame(fid)
                tag.frames.append(frame)
            frame.set_text(s,encoding='latin_1')
        tag.commit()
        if inDictAndTrue('print',paramDict): printMsg('commited successfully',paramDict)
    except Exception as e:
        printMsg('Failed to write %s, with exception %s' %(file,e),paramDict,tagName='err')



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
    if inDictAndTrue('print',paramDict):
      printMsg('%s: Artist: %s, album: %s' %(f,artist,album),paramDict,tagName='convert')
    if inDictAndTrue('convertTags',paramDict):
        convertTags(os.path.join(root,f),paramDict)

def setArtistTag(root,d,paramDict=None):
    pDict=paramDict.copy()
    pDict['artist']=d
    crunch(os.path.join(root,d),pDict,setAlbumTag)

def setAlbumTag(root,d,paramDict,):
    if inDictAndTrue('print',paramDict):
        printMsg( '='*50,paramDict,tagName='dir')
        printMsg( d,paramDict,tagName='dir')
        printMsg( '='*50,paramDict,tagName='dir')
    pDict = paramDict.copy()
    pDict['album']=d
    crunch(os.path.join(root,d),pDict,fDirs=None,fFiles=applyFileTags)


def crunchRoot(rootDir,paramDict=None):
    print paramDict
    try:
      crunch(rootDir,paramDict,fDirs=setArtistTag)

    except StopIteration as e:
        printMsg('Invalid directory: %s' %rootDir, paramDict,tagName='err')

    except Exception as e:
        printMsg( 'an error has occured: %r' %e, paramDict,tagName='err')






import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Edit mp3 tags recursively.')
    parser.add_argument('rootDir',metavar='root-directory')
    parser.add_argument('--dry-run','-d', action='store_true',
                   help='Don\'t execute, just show which files are going to be changed and how.')
    parser.add_argument('--verbose', '-v' ,action='store_true',
                   help='Print changes')
    args = parser.parse_args()
    paramDict ={'print' : args.verbose or args.dry_run, 'convertTags' : args.dry_run==False}

    crunchRoot(args.rootDir,paramDict)
