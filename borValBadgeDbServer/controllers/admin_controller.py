import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

import json

from borValBadgeDbServer.models.admin_purge_badge_infos_get200_response import AdminPurgeBadgeInfosGet200Response  # noqa: E501
from borValBadgeDbServer.models.database import Database  # noqa: E501
from borValBadgeDbServer.models.user_request_check_get200_response import UserRequestCheckGet200Response  # noqa: E501
from borValBadgeDbServer import util
from borValBadgeDbServer.db.db import dbLock, cachedBadgeDB, badgeDB
from borValBadgeDbServer.db.checker import checkInProgress, startCheck


def admin_dump_dbget():  # noqa: E501
    """Get a dump of the entire database right now

     # noqa: E501


    :rtype: Union[Database, Tuple[Database, int], Tuple[Database, int, Dict[str, str]]
    """

    dbLock.acquire()
    global cachedBadgeDB
    cachedBadgeDB = json.dumps(badgeDB.to_dict(), sort_keys=True, indent=2) + "\n"

    ret = connexion.lifecycle.ConnexionResponse(
        status_code=200,
        content_type="application/json",
        mimetype="text/plain",
        body=cachedBadgeDB
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
    return 'do some magic!'


def admin_purge_badge_infos_post(body):  # noqa: E501
    """Purge cached info of badges

     # noqa: E501

    :param body: The CSV of badge ids
    :type body: str

    :rtype: Union[AdminPurgeBadgeInfosGet200Response, Tuple[AdminPurgeBadgeInfosGet200Response, int], Tuple[AdminPurgeBadgeInfosGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def admin_purge_universe_infos_get(universe_ids):  # noqa: E501
    """Purge cached info of universes and all associated badges

     # noqa: E501

    :param universe_ids: The CSV of universe ids
    :type universe_ids: List[int]

    :rtype: Union[AdminPurgeBadgeInfosGet200Response, Tuple[AdminPurgeBadgeInfosGet200Response, int], Tuple[AdminPurgeBadgeInfosGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def admin_purge_universe_infos_post(body):  # noqa: E501
    """Purge cached info of universes and all associated badges

     # noqa: E501

    :param body: The CSV of universe ids
    :type body: str

    :rtype: Union[AdminPurgeBadgeInfosGet200Response, Tuple[AdminPurgeBadgeInfosGet200Response, int], Tuple[AdminPurgeBadgeInfosGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def admin_refresh_value_get():  # noqa: E501
    """Redetermine values of all badges in the database

     # noqa: E501


    :rtype: Union[AdminPurgeBadgeInfosGet200Response, Tuple[AdminPurgeBadgeInfosGet200Response, int], Tuple[AdminPurgeBadgeInfosGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


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
