from threading import Lock, Thread
import requests
import json
from dateutil.parser import isoparse
import time
import calendar
import sys
import traceback

from borValBadgeDbServer import util
from borValBadgeDbServer.models.badge_info import BadgeInfo
from borValBadgeDbServer.models.universe_info import UniverseInfo
from borValBadgeDbServer.db.db import dbLock, getBadgeDB, updateBadgeIdCache, getBadgeIdCache

checkLock = Lock()
checksInProgress = set()
missingReports = set()
missingReportsProcessed = 0


def check_in_progress(universeId):
    checkLock.acquire()
    ret = universeId in checksInProgress
    checkLock.release()
    return ret


def checkWorker(universeId):
    print(f"checkWorker@{universeId}: Check started", file=sys.stderr)
    universe: UniverseInfo = getBadgeDB().universes.get(universeId, UniverseInfo(int(universeId)))

    cursor = None
    name = None
    while True:
        try:
            oldCount = universe.badge_count
            url = f"https://badges.roblox.com/v1/universes/{universeId}/badges?limit=100&sortOrder=Desc"
            if cursor is not None:
                url += f"&cursor={cursor}"

            resp = json.loads(requests.get(url, timeout=30).text)
            if "data" in resp:
                for badge in resp["data"]:
                    name = badge["awardingUniverse"]["name"]
                    created = calendar.timegm(isoparse(badge["created"]).utctimetuple())
                    if badge["id"] not in universe.free_badges:
                        universe.badges[str(badge["id"])] = BadgeInfo(badge["id"], True, created, int(universeId))

            cursor = resp["nextPageCursor"]
            universe.badge_count = len(universe.badges) + len(universe.free_badges)
            print(f"checkWorker@{universeId}: {oldCount} -> {universe.badge_count}. Next cursor: {cursor}", file=sys.stderr)
            if cursor is None or oldCount == universe.badge_count:
                break
        except Exception:
            traceback.print_exc()
            time.sleep(0.1)

    if name is not None:
        universe.name = name
    universe.last_checked = util.getTimestamp()

    if universe.badge_count != 0:
        dbLock.acquire()
        getBadgeDB().universes[universeId] = universe
        refreshUniverse(universeId, True)
        updateBadgeIdCache(universeId)
        dbLock.release()

    checkLock.acquire()
    checksInProgress.remove(universeId)
    checkLock.release()
    print(f"checkWorker@{universeId}: Finished check", file=sys.stderr)


def refreshUniverse(universeId, doCompact=False):
    valuableBadges = set()

    badges = []
    days = {}
    for badgeId in getBadgeDB().universes[universeId].badges.keys():
        createdAt = getBadgeDB().universes[universeId].badges[badgeId].created
        badge = (createdAt, badgeId)
        badges.append(badge)

        day = createdAt // (24 * 60 * 60)
        if day not in days:
            days[day] = []
        days[day].append(badge)

    for day in days.values():
        valuableBadges.update(sorted(day)[5:])

    badges.sort()
    badges_affected = set()
    badgesToCompact = set(badges)
    curTime = util.getTimestamp()
    for i in range(len(badges)):
        badge = badges[i]
        oldValue = getBadgeDB().universes[universeId].badges[badge[1]].value

        if int(badge[1]) <= 2124945818:
            newValue = 2  # Legacy
            badgesToCompact.discard(badge)
        elif badge in valuableBadges:
            newValue = 1  # Valuable
            badgesToCompact.discard(badge)
            for k in range(max(0, i - 5), i):
                badgesToCompact.discard(badges[k])
        else:
            newValue = 0  # Free
            # Don't compact badges created within the last 72 hours
            if curTime - badge[0] <= 3 * 24 * 60 * 60:
                badgesToCompact.discard(badge)

        if oldValue != newValue:
            print(badge, oldValue, "->", newValue)
            badges_affected.add(badge)
        getBadgeDB().universes[universeId].badges[badge[1]].value = newValue

    if doCompact:
        for badge in badgesToCompact:
            print("Compact", badge)
            badges_affected.add(badge)
            assert getBadgeDB().universes[universeId].badges[badge[1]].value == 0
            del getBadgeDB().universes[universeId].badges[badge[1]]
            getBadgeDB().universes[universeId].free_badges.append(int(badge[1]))
    getBadgeDB().universes[universeId].free_badges.sort()
    return len(badges_affected)


def startCheck(universeId):
    checkLock.acquire()
    if universeId not in checksInProgress:
        checksInProgress.add(universeId)
        Thread(target=checkWorker, args=[universeId], daemon=True).start()
    checkLock.release()


def missingReportWorker():
    while True:
        try:
            checkLock.acquire()
            if len(missingReports) == 0:
                checkLock.release()
                time.sleep(0.01)
                continue

            toCheck = missingReports.pop()

            global missingReportsProcessed
            missingReportsProcessed += 1
            if missingReportsProcessed % 50 == 0 or len(missingReports) == 0:
                print(f"missingReportWorker: {len(missingReports)} left to process", file=sys.stderr)
            checkLock.release()

            if toCheck in getBadgeIdCache():
                continue

            url = f"https://badges.roblox.com/v1/badges/{toCheck}"
            resp = json.loads(requests.get(url).text)
            if "awardingUniverse" not in resp:
                continue

            startCheck(str(resp["awardingUniverse"]["id"]))
        except Exception:
            traceback.print_exc()


def reportMissing(badgeIds):
    checkLock.acquire()
    global missingReports
    oldLength = len(missingReports)
    missingReports |= badgeIds
    ret = len(missingReports) - oldLength
    checkLock.release()
    return ret
