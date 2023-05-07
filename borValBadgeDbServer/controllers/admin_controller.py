import connexion

import json

from borValBadgeDbServer.models.admin_purge_badge_infos_get200_response import AdminPurgeBadgeInfosGet200Response  # noqa: E501
from borValBadgeDbServer.models.user_request_check_get200_response import UserRequestCheckGet200Response  # noqa: E501
from borValBadgeDbServer.db.db import dbLock, getCachedBadgeDB, setCachedBadgeDB, badgeDB, saveDatabase, getBadgeIdCache, updateBadgeIdCache
from borValBadgeDbServer.db.checker import checkInProgress, startCheck, refreshValue


def admin_dump_dbget():  # noqa: E501
    """Get a dump of the entire database right now

     # noqa: E501


    :rtype: Union[Database, Tuple[Database, int], Tuple[Database, int, Dict[str, str]]
    """

    dbLock.acquire()
    setCachedBadgeDB(json.dumps(badgeDB.to_dict()) + "\n")

    ret = connexion.lifecycle.ConnexionResponse(
        status_code=200,
        content_type="application/json",
        mimetype="text/plain",
        body=getCachedBadgeDB()
    )
    dbLock.release()
    return ret


def admin_purge_badge_infos_get(badge_ids):  # noqa: E501
    """Purge cached info of badges

     # noqa: E501

    :param badge_ids: The CSV of badge ids
    :type badge_ids: List[int]

    :rtype: Union[AdminPurgeBadgeInfosGet200Response, Tuple[AdminPurgeBadgeInfosGet200Response, int], Tuple[AdminPurgeBadgeInfosGet200Response, int, Dict[str, str]]
    """

    badge_ids = {str(x) for x in badge_ids}

    dbLock.acquire()
    badgesAffected = 0
    for universeId in badgeDB.universes.keys():
        idsToRemove = badge_ids & getBadgeIdCache(universeId)
        badgesAffected += len(idsToRemove)
        for badgeId in idsToRemove:
            del badgeDB.universes[universeId].badges[badgeId]
        badgeDB.universes[universeId].badge_count = len(badgeDB.universes[universeId].badges)
        updateBadgeIdCache(universeId)
    dbLock.release()
    return AdminPurgeBadgeInfosGet200Response(badgesAffected)


def admin_purge_badge_infos_post(body):  # noqa: E501
    """Purge cached info of badges

     # noqa: E501

    :param body: The CSV of badge ids
    :type body: str

    :rtype: Union[AdminPurgeBadgeInfosGet200Response, Tuple[AdminPurgeBadgeInfosGet200Response, int], Tuple[AdminPurgeBadgeInfosGet200Response, int, Dict[str, str]]
    """

    return admin_purge_badge_infos_get(body.decode().split(","))


def admin_purge_universe_infos_get(universe_ids):  # noqa: E501
    """Purge cached info of universes and all associated badges

     # noqa: E501

    :param universe_ids: The CSV of universe ids
    :type universe_ids: List[int]

    :rtype: Union[AdminPurgeBadgeInfosGet200Response, Tuple[AdminPurgeBadgeInfosGet200Response, int], Tuple[AdminPurgeBadgeInfosGet200Response, int, Dict[str, str]]
    """

    universe_ids = {str(x) for x in universe_ids}

    dbLock.acquire()
    idsToRemove = universe_ids & set(badgeDB.universes.keys())
    badgesAffected = 0
    for universeId in idsToRemove:
        badgesAffected += badgeDB.universes[universeId].badge_count
        del badgeDB.universes[universeId]
    dbLock.release()
    return AdminPurgeBadgeInfosGet200Response(badgesAffected)


def admin_purge_universe_infos_post(body):  # noqa: E501
    """Purge cached info of universes and all associated badges

     # noqa: E501

    :param body: The CSV of universe ids
    :type body: str

    :rtype: Union[AdminPurgeBadgeInfosGet200Response, Tuple[AdminPurgeBadgeInfosGet200Response, int], Tuple[AdminPurgeBadgeInfosGet200Response, int, Dict[str, str]]
    """

    return admin_purge_universe_infos_get(body.decode().split(","))


def admin_refresh_value_get():  # noqa: E501
    """Redetermine values of all badges in the database

     # noqa: E501


    :rtype: Union[AdminPurgeBadgeInfosGet200Response, Tuple[AdminPurgeBadgeInfosGet200Response, int], Tuple[AdminPurgeBadgeInfosGet200Response, int, Dict[str, str]]
    """

    dbLock.acquire()
    badgesAffected = 0
    for universeId in badgeDB.universes.keys():
        badgesAffected += refreshValue(universeId)
        updateBadgeIdCache(universeId)
    dbLock.release()
    return AdminPurgeBadgeInfosGet200Response(badgesAffected)


def admin_save_dbget():  # noqa: E501
    """Save the database right now

     # noqa: E501


    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """

    saveDatabase()


def admin_start_check_get(universe_id):  # noqa: E501
    """Start a check/recheck of an universe

     # noqa: E501

    :param universe_id: The universe id to check
    :type universe_id: int

    :rtype: Union[UserRequestCheckGet200Response, Tuple[UserRequestCheckGet200Response, int], Tuple[UserRequestCheckGet200Response, int, Dict[str, str]]
    """

    universe_id = str(universe_id)
    dbLock.acquire()
    lastChecked = 0
    if universe_id in badgeDB.universes:
        lastChecked = badgeDB.universes[universe_id].last_checked
    dbLock.release()

    startCheck(universe_id)
    return UserRequestCheckGet200Response(lastChecked, checkInProgress(universe_id))
