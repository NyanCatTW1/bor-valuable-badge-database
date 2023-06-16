from threading import Lock, Thread
import requests
import json
from dateutil.parser import isoparse
import time
import sys

from borValBadgeDbServer import util
from borValBadgeDbServer.models.badge_info import BadgeInfo
from borValBadgeDbServer.models.universe_info import UniverseInfo
from borValBadgeDbServer.db.db import dbLock, getBadgeDB, updateBadgeIdCache

checkLock = Lock()
checksInProgress = set()
missingReports = set()


def check_in_progress(universeId):
    checkLock.acquire()
    ret = universeId in checksInProgress
    checkLock.release()
    return ret


def checkWorker(universeId):
    universe: UniverseInfo = getBadgeDB().universes.get(universeId, UniverseInfo(int(universeId)))

    cursor = None
    name = None
    while True:
        oldCount = len(universe.badges)
        url = f"https://badges.roblox.com/v1/universes/{universeId}/badges?limit=100&sortOrder=Desc"
        if cursor is not None:
            url += f"&cursor={cursor}"

        resp = json.loads(requests.get(url).text)
        if "data" in resp:
            for badge in resp["data"]:
                name = badge["awardingUniverse"]["name"]
                created = int(time.mktime(isoparse(badge["created"]).timetuple()) * 1000)
                universe.badges[str(badge["id"])] = BadgeInfo(badge["id"], True, created, int(universeId))

        cursor = resp["nextPageCursor"]
        universe.badge_count = len(universe.badges)
        print(f"{universeId}: {oldCount} -> {universe.badge_count}", file=sys.stderr)
        if cursor is None or oldCount == universe.badge_count:
            break

    if name is not None:
        universe.name = name
    universe.last_checked = util.getTimestamp()

    if len(universe.badges) != 0:
        dbLock.acquire()
        getBadgeDB().universes[universeId] = universe
        refreshUniverse(universeId)
        updateBadgeIdCache(universeId)
        dbLock.release()

    checkLock.acquire()
    checksInProgress.remove(universeId)
    checkLock.release()
    print(f"Finished check on {universeId}", file=sys.stderr)


def refreshUniverse(universeId):
    valuableBadges = set()

    days = {}
    for badgeId in getBadgeDB().universes[universeId].badges.keys():
        day = getBadgeDB().universes[universeId].badges[badgeId].created // (24 * 60 * 60 * 1000)
        if day not in days:
            days[day] = []
        days[day].append(int(badgeId))

    for day in days.values():
        valuableBadges.update(sorted(day)[5:])

    badges_affected = set()
    badgeIds = list(map(str, sorted(map(int, getBadgeDB().universes[universeId].badges.keys()))))
    badgesToCompact = set(badgeIds)
    curTime = util.getTimestamp()
    for i in range(len(badgeIds)):
        badgeId = badgeIds[i]
        oldValue = getBadgeDB().universes[universeId].badges[badgeId].value

        if int(badgeId) <= 2124945818:
            newValue = 2  # Legacy
            badgesToCompact.discard(badgeId)
        elif oldValue == 1 or int(badgeId) in valuableBadges:
            newValue = 1  # Valuable
            badgesToCompact.discard(badgeId)
            for k in range(max(0, i - 5), i):
                badgesToCompact.discard(badgeIds[k])
        else:
            newValue = 0  # Free
            # Don't compact badges created within the last 72 hours
            if curTime - getBadgeDB().universes[universeId].badges[badgeId].created <= 3 * 24 * 60 * 60 * 1000:
                badgesToCompact.discard(badgeId)

        if oldValue != newValue:
            badges_affected.add(badgeId)
        getBadgeDB().universes[universeId].badges[badgeId].value = newValue

    for badgeId in badgesToCompact:
        badges_affected.add(badgeId)
        assert getBadgeDB().universes[universeId].badges[badgeId].value == 0
        del getBadgeDB().universes[universeId].badges[badgeId]
        getBadgeDB().universes[universeId].free_badges.append(int(badgeId))
    return len(badges_affected)


def startCheck(universeId):
    if check_in_progress(universeId):
        return

    checkLock.acquire()
    print(f"Started check on {universeId}", file=sys.stderr)
    checksInProgress.add(universeId)
    Thread(target=checkWorker, args=[universeId], daemon=True).start()
    checkLock.release()


def missingReportWorker():
    while True:
        checkLock.acquire()
        if len(missingReports) == 0:
            checkLock.release()
            time.sleep(0.01)
            continue

        toCheck = missingReports.pop()
        checkLock.release()

        url = f"https://badges.roblox.com/v1/badges/{toCheck}"
        resp = json.loads(requests.get(url).text)
        if "awardingUniverse" not in resp:
            continue

        universeId = str(resp["awardingUniverse"]["id"])
        startCheck(universeId)


def reportMissing(badgeIds):
    checkLock.acquire()
    global missingReports
    oldLength = len(missingReports)
    missingReports |= badgeIds
    ret = len(missingReports) - oldLength
    checkLock.release()
    return ret
