import os
import sys
import json
import traceback
from threading import Lock
import shutil
import gzip

from borValBadgeDbServer.models.database import Database
from borValBadgeDbServer.util import getTimestamp

dbPath = None
dbLock = Lock()
badgeDB: Database = None
badgeIdCache = {}


def getBadgeDB():
    return badgeDB


def getBadgeIdCache():
    return badgeIdCache


def updateBadgeIdCache(universeId):
    for badgeId in map(int, badgeDB.universes[universeId].badges.keys()):
        badgeIdCache[badgeId] = universeId

    for badgeId in badgeDB.universes[universeId].free_badges:
        badgeIdCache[badgeId] = universeId


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
        print(f"loadDatabase: Loaded {dbPath} with {len(badgeDB.universes)} universes and {totalBadgeCount} badges", file=sys.stderr)
    except Exception:
        traceback.print_exc()
        print(f"loadDatabase: Failed to load {dbPath}! Using default", file=sys.stderr)
        badgeDB = Database.from_dict({"universes": {}})

        if os.path.isfile(dbPath):
            bakPath = dbPath + f"-{getTimestamp()}.bak"
            shutil.copy2(dbPath, bakPath)
            print(f"loadDatabase: Copied {dbPath} to {bakPath}", file=sys.stderr)

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
