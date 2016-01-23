import pUtils
import os
import sys
import shutil

# Options
videoExt = ['.avi', '.mp4', '.mkv', '.srt']
seriesFolder = 'SERIES'
seriesMatches = ['[0-9]{4}.s[0-9]{2}e[0-9]{2}', 's[0-9]{2}e[0-9]{2}']

moviesFolder = 'MOVIES'
moviesMatches = ['dvdrip', 'brrip', 'dvdscr', 'hdrip', 'webrip', 'bdrip']

avoid = ['sample.avi']

logs = True
moveFiles = True
deleteOldPath = True

# End Options

utils = pUtils.Utils(seriesMatches, moviesMatches)

STRING_UNKNOWN = 'unknown'
STRING_MOVIE = 'movie'
STRING_SERIES = 'series'


# noinspection PyPep8Naming
def magicToFolders(currentPath, globalPath):
    for folder in utils.listFolders(currentPath):
        result = checkFileName(folder)
        if result.getVideoKind() == STRING_MOVIE:
            oldPath = os.path.join(currentPath, folder)
            newPath = os.path.join(globalPath, moviesFolder)

            if logs:
                print 'Moving ' + folder + ' to ' + newPath
            if moveFiles:
                utils.move(oldPath, newPath)
            continue
        if result.getVideoKind() != STRING_UNKNOWN:
            magicToFiles(os.path.join(currentPath, folder), globalPath, result)


# noinspection PyPep8Naming
def magicToFiles(currentPath, globalPath, fileObject):
    global newPath

    for file in utils.listFiles(currentPath):

        if fileObject is None:
            fileObject = checkFileName(file)

        if fileObject.getVideoKind() == STRING_UNKNOWN:
            fileObject = None
            continue

        if file in avoid:
            continue

        if utils.getExt(file) in videoExt:
            oldPath = os.path.join(currentPath, file)

            if fileObject.getVideoKind() == STRING_MOVIE:
                newPath = os.path.join(globalPath, moviesFolder)
            elif fileObject.getVideoKind() == STRING_SERIES:
                tempList = utils.showNameToList(fileObject.getShowName())
                newPath = os.path.join(globalPath, seriesFolder, utils.cleanName(tempList))

            if newPath:

                if logs:
                    print 'Moving ' + fileObject.getName() + ' to ' + newPath
                if moveFiles:
                    # Check if the move command returns smth
                    utils.move(oldPath, newPath)

        fileObject = None

    # remove old path if everything went allright
    if deleteOldPath and currentPath != globalPath:
        shutil.rmtree(currentPath)


# noinspection PyPep8Naming
def checkFileName(fileName):
    fileName = fileName.lower()
    resultShow = utils.isShow(fileName)
    if resultShow == -1:
        resultMovie = utils.isMovie(fileName)
        if resultMovie == 1:
            return FileObject(STRING_MOVIE, fileName, '')
        else:
            return FileObject(STRING_UNKNOWN, fileName, '')
    else:
        return FileObject(STRING_SERIES, fileName, resultShow)


# noinspection PyPep8Naming
class FileObject:
    videoKind = ''
    name = ''
    showName = ''

    def __init__(self, videoKind, name, showName):
        self.videoKind = videoKind
        self.name = name

        if showName:
            self.showName = showName

    def getVideoKind(self):
        return self.videoKind

    def getName(self):
        return self.name

    def setShowName(self, showName):
        self.showName = showName

    def getShowName(self):
        return self.showName

inputPath = sys.argv[1]
magicToFolders(inputPath, inputPath)
magicToFiles(inputPath, inputPath, None)
