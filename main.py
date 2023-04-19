import os
import zipfile
from send2trash import send2trash
import sys

def getFileNamesInZip(zipFilePath):
    zip = zipfile.ZipFile(zipFilePath)
    return zip.namelist()


def getNumberOfObjectsInZipRoot(zipFilePath):
    fileNames = getFileNamesInZip(zipFilePath)
    c = 0
    for fileName in fileNames:
        if fileName.count('/') == 1:
            if fileName.endswith('/'):
                c += 1
        elif fileName.count('/') == 0:
            c += 1
    return c


def unpackZip(zipFilePath, targetDir):
    zip = zipfile.ZipFile(zipFilePath)
    zip.extractall(targetDir)


def smartUnpack(zipPath):
    if getNumberOfObjectsInZipRoot(zipPath) <= 1:
        unpackZip(zipPath, os.path.dirname(zipPath))
        send2trash(zipPath)
        return True
    elif getNumberOfObjectsInZipRoot(zipPath) > 1:
        newDir = os.path.join(os.path.dirname(zipPath), os.path.splitext(os.path.basename(zipPath))[0])
        unpackZip(zipPath, newDir)
        send2trash(zipPath)
        return True

if __name__ == "__main__":
    if len(sys.argv)>1:
        smartUnpack(sys.argv[1])
    else:
        print("Please provide an archive file as argument")