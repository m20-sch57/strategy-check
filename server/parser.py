from server.structures import Problem, Rules
from zipfile import ZipFile, BadZipFile
from enum import IntEnum
from server.storage import storage
from server.commonFunctions import readFile, problemFolder, splitPath, createFile
import os, shutil, glob, json
import shutil

SaveFolder = 'tmp'

class FolderType(IntEnum):
    Correct = 0
    OnTheWay = 1
    Bad = 2

FoldersList = ['downloads', 'sources', 'static', 'templates']
FilesList = ['config.json', 'statement']

def getFolderType(path):
    lst = os.listdir(path)
    if (len(lst) == 1 and os.path.isdir(os.path.join(path, lst[0]))):
        return {'type' : FolderType.OnTheWay, 'go' : lst[0]}
    for folder in FoldersList:
        if (not os.path.isdir(os.path.join(path, folder))):
            return {'type' : FolderType.Bad}
    for file in FilesList:
        if (not os.path.isfile(os.path.join(path, file))):
            return {'type' : FolderType.Bad}
    return {'type' : FolderType.Correct}

MaxSourceSize = 256000

class SourceSizeException(Exception):
    pass

def getFilePathes(prefixPath):
    return [filename
            for filename in 
            glob.iglob(os.path.join(prefixPath, '**', '*'), recursive = True)
            if (os.path.isfile(filename))
    ]

def readFiles(readPath, outPath):
    res = []
    for filename in getFilePathes(readPath):
        if (os.path.getsize(filename) > MaxSourceSize):
            raise SourceSizeException
        rel = os.path.relpath(filename, readPath)
        res.append([os.path.join(outPath, rel), readFile(filename)])
    return res

def copyFiles(readPath, outPath):
    for filename in getFilePathes(readPath):
        aimPath = os.path.join(outPath, *splitPath(filename)[2:])
        createFile(aimPath)
        shutil.copy(filename, aimPath)

def parseArchive(archivePath, probId = -1):
    if (not os.path.isfile(archivePath)):
        return {'ok' : 0, 'error' : 'No such archive (internal error)'}
    if (os.path.isdir(SaveFolder)):
        shutil.rmtree(SaveFolder)
    try:
        zip = ZipFile(archivePath)
    except BadZipFile:
        return {'ok' : 0, 'error' : 'Bad zip file'}
    zip.extractall(path = SaveFolder)
    problemPath = SaveFolder

    while (True):
        typeDict = getFolderType(problemPath)
        if (typeDict['type'] == FolderType.Correct):
            break
        elif (typeDict['type'] == FolderType.Bad):
            return {'ok' : 0, 'error' : "Archive isn't correct"}
        else:
            problemPath = os.path.join(problemPath, typeDict['go'])

    statement = readFile(os.path.join(problemPath, 'statement'))
    rawConfig = readFile(os.path.join(problemPath, 'config.json'))
    config = json.loads(rawConfig)

    if ('name' not in config):
        return {'ok' : 0, 'error' : 'No name parameter in config'}

    if (probId == -1):
        probId = storage.getProblemsCount()
        problem = Problem(probId, Rules("", [], [], ""), {}, [], [], -1, 0)
    else:
        problem = storage.getProblem(probId)
        problem.revisionId += 1

    name = config['name']

    try:
        downloads = readFiles(os.path.join(problemPath, 'downloads'),
            os.path.join('app', 'downloads', problemFolder(probId)))
        sources1 = readFiles(os.path.join(problemPath, 'sources'),
            os.path.join('problems', problemFolder(probId)))
        sources2 = readFiles(os.path.join(problemPath, 'templates'),
            os.path.join('app', 'templates', 'problems', problemFolder(probId)))
    except SourceSizeException:
        return {'ok' : 0, 'error' : 'Source file is too large'}
    except UnicodeDecodeError:
        return {'ok' : 0, 'error' : "Can't decode files"}

    copyFiles(os.path.join(problemPath, 'static'),
        os.path.join('app', 'static', 'problems', problemFolder(probId)))

    sources = sources1 + sources2

    if (name == "" or (name != problem.rules.name and storage.getProblemByName(name) != None)):
        return {"ok": 0, "error": "You can't add problem with same name"}

    newRules = Rules(name, sources, downloads, statement)
    problem.rules = newRules

    storage.saveProblem(problem)
    return {'ok' : 1}

