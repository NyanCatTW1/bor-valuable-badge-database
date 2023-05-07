from threading import Lock, Thread

from borValBadgeDbServer import util
from borValBadgeDbServer.models.universe_info import UniverseInfo
from borValBadgeDbServer.db.db import dbLock, badgeDB

checkLock = Lock()
checksInProgress = set()


def checkInProgress(universeId):
    checkLock.acquire()
    ret = universeId in checksInProgress
    checkLock.release()
    return ret


def checkWorker(universeId):
    dbLock.acquire()
    universe = badgeDB.universes.get(universeId, UniverseInfo(int(universeId)))
    dbLock.release()

    universe.last_checked = util.getTimestamp()

    dbLock.acquire()
    badgeDB.universes[universeId] = universe
    dbLock.release()

    checkLock.acquire()
    checksInProgress.remove(universeId)
    checkLock.release()


def startCheck(universeId):
    if checkInProgress(universeId):
        return

    checkLock.acquire()
    checksInProgress.add(universeId)
    Thread(target=checkWorker, args=[universeId]).start()
    checkLock.release()
