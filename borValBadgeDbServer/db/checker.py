from threading import Lock, Thread
import requests
import json
from dateutil.parser import isoparse
import time

from borValBadgeDbServer import util
from borValBadgeDbServer.models.badge_info import BadgeInfo
from borValBadgeDbServer.models.universe_info import UniverseInfo
from borValBadgeDbServer.db.db import dbLock, badgeDB, updateBadgeIdCache

checkLock = Lock()
checksInProgress = set()


def checkInProgress(universeId):
    checkLock.acquire()
    ret = universeId in checksInProgress
    checkLock.release()
    return ret


def checkWorker(universeId):
    dbLock.acquire()
    universe: UniverseInfo = badgeDB.universes.get(universeId, UniverseInfo(int(universeId)))
    dbLock.release()

    cursor = None
    while True:
        oldCount = len(universe.badges)
        url = f"https://badges.roblox.com/v1/universes/{universeId}/badges?limit=100&sortOrder=Desc"
        if cursor is not None:
            url += f"&cursor={cursor}"

        resp = json.loads(requests.get(url).text)
        if "data" in resp:
            for badge in resp["data"]:
                created = int(time.mktime(isoparse(badge["created"]).timetuple()) * 1000)
                universe.badges[str(badge["id"])] = BadgeInfo(badge["id"], True, created, int(universeId))

        cursor = resp["nextPageCursor"]
        universe.badge_count = len(universe.badges)
        print(f"{universeId}: {oldCount} -> {universe.badge_count}")
        if cursor is None or oldCount == universe.badge_count:
            break

    universe.last_checked = util.getTimestamp()

    if len(universe.badges) != 0:
        dbLock.acquire()
        badgeDB.universes[universeId] = universe
        updateBadgeIdCache(universeId)
        dbLock.release()

    checkLock.acquire()
    checksInProgress.remove(universeId)
    checkLock.release()


def refreshValue(universeId):
    badgesAffected = 0
    for badgeId in badgeDB.universes[universeId].badges.keys():
        oldValue = badgeDB.universes[universeId].badges[badgeId].value

        if int(badgeId) <= 2124949326:
            newValue = "Legacy"
        else:
            newValue = "Free"

        if oldValue != newValue:
            badgesAffected += 1
        badgeDB.universes[universeId].badges[badgeId].value = newValue
    return badgesAffected


def startCheck(universeId):
    if checkInProgress(universeId):
        return

    checkLock.acquire()
    checksInProgress.add(universeId)
    Thread(target=checkWorker, args=[universeId]).start()
    checkLock.release()
