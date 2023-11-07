import os
from send2trash import send2trash
import sys
import subprocess


def getFileNamesInZip(zipFilePath):
    processReturn = subprocess.check_output("7z l " + zipFilePath, creationflags=subprocess.CREATE_NO_WINDOW)
    decoded_string = processReturn.decode("utf-8").replace("\\\\", "\\").replace("\\", "/")
    ZipList = decoded_string.strip().split("\n")
    listStarted = False
    fileList = []
    for entry in ZipList:
        if listStarted:
            if "----" in entry:
                return fileList
            fileList.append(entry.split(" ")[-1])
        else:
            if "-----" in entry:
                listStarted = True


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


def unpackZip(zipFilePath, destinationDir):
    subprocess.call("7z x " + zipFilePath + " -o" + destinationDir, creationflags=subprocess.CREATE_NO_WINDOW)


def smartUnpack(zipPath):
    print("name: " + os.path.dirname(zipPath))
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
    if len(sys.argv) > 1:
        smartUnpack(sys.argv[1])
    else:
        print("Please provide an archive file as argument")
