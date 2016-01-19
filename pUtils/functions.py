import os
import shutil
import re

seriesMatches = []
moviesMatches = []

# noinspection PyPep8Naming
class Utils:
    def __init__(self, seriesmatches, moviesmatches):
        self.seriesMatches = seriesmatches
        self.moviesMatches = moviesmatches

    def createEnv(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def majFirstLetter(self, inputString):
        string = inputString[:1].upper() + inputString[1:]
        return string

    def cleanName(self, nameAsList):
        string = ""
        for i in nameAsList:
            string += self.majFirstLetter(i) + '.'
        return string[:-1]

    def isShow(self, fileName):
        # returns -1 if not a show, otherwise the name of the show
        fileName = fileName.lower()

        for match in self.seriesMatches:
            p = re.compile(match)
            m = p.search(fileName)
            if m:
                return fileName[:m.start()]
        return -1

    def isMovie(self, fileName):
        # Will be used only if isShow returns -1
        for match in self.moviesMatches:
            p = re.compile(match)
            m = p.search(fileName)
            if m:
                return 1
        return -1

    def showNameToList(self, showName):
        tempList = re.findall(r"[\w']+", showName)
        return [x for x in tempList]

    def listFolders(self, path):
        return [x[1] for x in os.walk(path)][0]

    def listFiles(self, path):
        return [x[2] for x in os.walk(path)][0]

    def getExt(self, item):
        return os.path.splitext(item)[1]

    def move(self, oldPath, newPath):
        self.createEnv(newPath)
        shutil.move(oldPath, newPath)