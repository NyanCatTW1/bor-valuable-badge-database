import os
import sys
import json
import traceback
from threading import Lock
import shutil
import gzip
import time

from borValBadgeDbServer.models.database import Database
from borValBadgeDbServer.util import getTimestamp

dbPath = None
dbLock = Lock()
badgeDB: Database = None
cachedBadgeDB = None
cachedBadgeIdsPerUniverse = {}


def getBadgeDB():
    return badgeDB


def getCachedBadgeDB():
    return cachedBadgeDB


def setCachedBadgeDB(newDB):
    global cachedBadgeDB
    cachedBadgeDB = newDB


def getBadgeIdCache(universeId):
    return cachedBadgeIdsPerUniverse[universeId]


def updateBadgeIdCache(universeId):
    if universeId not in badgeDB.universes and universeId in cachedBadgeIdsPerUniverse:
        del cachedBadgeIdsPerUniverse[universeId]
    else:
        cachedBadgeIdsPerUniverse[universeId] = set(map(int, badgeDB.universes[universeId].badges.keys())) | set(badgeDB.universes[universeId].free_badges)


def loadDatabase():
    dbLock.acquire()
    global dbPath
    if len(sys.argv) < 2:
        dbPath = "borValBadgeDB.json.gz"
    else:
        dbPath = sys.argv[1]

    global badgeDB
    try:
        badgeDB = Database.from_dict(json.load(gzip.open(dbPath, "r")))
        totalBadgeCount = 0
        for universe in badgeDB.universes.values():
            totalBadgeCount += universe.badge_count
        print(f"Loaded {dbPath} with {len(badgeDB.universes)} universes and {totalBadgeCount} badges", file=sys.stderr)
    except Exception:
        traceback.print_exc()
        print(f"Failed to load {dbPath}! Using default", file=sys.stderr)
        badgeDB = Database.from_dict({"universes": {}})

        if os.path.isfile(dbPath):
            bakPath = dbPath + f"-{getTimestamp()}.bak"
            shutil.copy2(dbPath, bakPath)
            print(f"Copied {dbPath} to {bakPath}", file=sys.stderr)

    for universeId in badgeDB.universes.keys():
        updateBadgeIdCache(universeId)
    dbLock.release()

    """
    try:
        from guppy import hpy
        h = hpy()
        heap = h.heap()
        print(heap, file=sys.stderr)
        print(heap.byrcs, file=sys.stderr)
    except ModuleNotFoundError:
        pass
    """


def saveDatabase():
    print("Saving database...", file=sys.stderr)
    startTime = time.time()
    try:
        dbLock.acquire()
        setCachedBadgeDB(json.dumps(badgeDB.to_dict()) + "\n")
        toSave = getCachedBadgeDB().encode("ascii")
        dbLock.release()
        toSave = gzip.compress(toSave)

        bakPath = dbPath + f"-{getTimestamp()}.bak"
        if os.path.isfile(dbPath):
            shutil.copy2(dbPath, bakPath)
        with open(dbPath, "wb") as f:
            f.write(toSave)
        if os.path.isfile(bakPath):
            os.remove(bakPath)

        endTime = time.time()
        print(f"Databased saved in {round(endTime - startTime, 2)} seconds", file=sys.stderr)
    except Exception:
        traceback.print_exc()
        print("Failed to save database!", file=sys.stderr)
