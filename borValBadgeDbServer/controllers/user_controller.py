import connexion

from borValBadgeDbServer.models.user_request_check_get200_response import UserRequestCheckGet200Response  # noqa: E501
from borValBadgeDbServer import util
from borValBadgeDbServer.db.db import dbLock, getCachedBadgeDB, badgeDB
from borValBadgeDbServer.db.checker import checkInProgress, startCheck


def user_dump_dbget():  # noqa: E501
    """Get a dump of the entire database. Updates every five minutes

     # noqa: E501


    :rtype: Union[Database, Tuple[Database, int], Tuple[Database, int, Dict[str, str]]
    """

    dbLock.acquire()
    ret = connexion.lifecycle.ConnexionResponse(
        status_code=200,
        content_type="application/json",
        mimetype="text/plain",
        body=getCachedBadgeDB()
    )
    dbLock.release()
    return ret


def user_request_check_get(universe_id):  # noqa: E501
    """Request a check/recheck of an universe. Gets ignored if the universe was last checked &lt;5 mins ago

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

    if util.getTimestamp() - lastChecked >= 5 * 60 * 1000:
        startCheck(universe_id)

    return UserRequestCheckGet200Response(lastChecked, checkInProgress(universe_id))
