import os
import sys
import json
import traceback
from datetime import datetime
from threading import Lock

from borValBadgeDbServer.models.database import Database

from apscheduler.schedulers.sync import Scheduler
from apscheduler.triggers.interval import IntervalTrigger

dbScheduler = Scheduler()
dbPath = None
dbLock = Lock()
badgeDB = None
cachedBadgeDB = None


def loadDatabase():
    dbLock.acquire()
    global dbPath
    if len(sys.argv) < 2:
        dbPath = "borValBadgeDB.json"
    else:
        dbPath = sys.argv[1]

    global badgeDB
    try:
        badgeDB = Database.from_dict(json.load(open(dbPath)))
        totalBadgeCount = 0
        for universe in badgeDB.universes:
            totalBadgeCount += universe.badge_count
        print(f"Loaded {dbPath} with {len(badgeDB.universes)} universes and {totalBadgeCount} badges")
    except Exception:
        traceback.print_exc()
        print(f"Failed to load {dbPath}! Using default")
        badgeDB = Database.from_dict({"universes": []})

        if os.path.isfile(dbPath):
            # https://stackoverflow.com/a/60380427
            bakPath = dbPath + f"-{int(datetime.utcnow().timestamp() * 1e3)}.bak"
            os.rename(dbPath, bakPath)
            print(f"Moved {dbPath} to {bakPath}")
    dbLock.release()

    dbScheduler.add_schedule(saveDatabase, IntervalTrigger(minutes=5))
    dbScheduler.start_in_background()


def saveDatabase():
    dbLock.acquire()
    try:
        global cachedBadgeDB
        cachedBadgeDB = json.dumps(badgeDB.to_dict(), sort_keys=True, indent=2) + "\n"

        with open(dbPath, "w") as f:
            f.write(cachedBadgeDB)
    except Exception:
        traceback.print_exc()
        print("Failed to save database!")
    dbLock.release()
