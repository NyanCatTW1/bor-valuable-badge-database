import connexion

import json

from borValBadgeDbServer.models.admin_purge_badge_infos_get200_response import AdminPurgeBadgeInfosGet200Response  # noqa: E501
from borValBadgeDbServer.models.user_request_check_get200_response import UserRequestCheckGet200Response  # noqa: E501
from borValBadgeDbServer.db.db import dbLock, getCachedBadgeDB, setCachedBadgeDB, getBadgeDB, saveDatabase, getBadgeIdCache, updateBadgeIdCache
from borValBadgeDbServer.db.checker import check_in_progress, startCheck, refreshUniverse


def admin_dump_dbget():  # noqa: E501
    """Get a dump of the entire database right now

     # noqa: E501


    :rtype: Union[Database, Tuple[Database, int], Tuple[Database, int, Dict[str, str]]
    """

    dbLock.acquire()
    setCachedBadgeDB(json.dumps(getBadgeDB().to_dict()) + "\n")

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
    badges_affected = 0
    for universeId in getBadgeDB().universes.keys():
        idsToRemove = badge_ids & getBadgeIdCache(universeId)
        badges_affected += len(idsToRemove)
        for badgeId in idsToRemove:
            if badgeId in getBadgeDB().universes[universeId]:
                del getBadgeDB().universes[universeId].badges[badgeId]
            else:
                getBadgeDB().universes[universeId].free_badges.remove(badgeId)
        getBadgeDB().universes[universeId].badge_count = len(getBadgeDB().universes[universeId].badges)
        updateBadgeIdCache(universeId)
    dbLock.release()
    return AdminPurgeBadgeInfosGet200Response(badges_affected)


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
    idsToRemove = universe_ids & set(getBadgeDB().universes.keys())
    badges_affected = 0
    for universeId in idsToRemove:
        badges_affected += getBadgeDB().universes[universeId].badge_count
        del getBadgeDB().universes[universeId]
    dbLock.release()
    return AdminPurgeBadgeInfosGet200Response(badges_affected)


def admin_purge_universe_infos_post(body):  # noqa: E501
    """Purge cached info of universes and all associated badges

     # noqa: E501

    :param body: The CSV of universe ids
    :type body: str

    :rtype: Union[AdminPurgeBadgeInfosGet200Response, Tuple[AdminPurgeBadgeInfosGet200Response, int], Tuple[AdminPurgeBadgeInfosGet200Response, int, Dict[str, str]]
    """

    return admin_purge_universe_infos_get(body.decode().split(","))


def admin_refresh_db_get():  # noqa: E501
    """Redetermine values of all badges in the database and compact it

     # noqa: E501


    :rtype: Union[AdminPurgeBadgeInfosGet200Response, Tuple[AdminPurgeBadgeInfosGet200Response, int], Tuple[AdminPurgeBadgeInfosGet200Response, int, Dict[str, str]]
    """

    dbLock.acquire()
    badges_affected = 0
    for universeId in getBadgeDB().universes.keys():
        badges_affected += refreshUniverse(universeId)
        updateBadgeIdCache(universeId)
    dbLock.release()
    return AdminPurgeBadgeInfosGet200Response(badges_affected)


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
    last_checked = 0
    if universe_id in getBadgeDB().universes:
        last_checked = getBadgeDB().universes[universe_id].last_checked

    startCheck(universe_id)
    return UserRequestCheckGet200Response(last_checked, check_in_progress(universe_id))
