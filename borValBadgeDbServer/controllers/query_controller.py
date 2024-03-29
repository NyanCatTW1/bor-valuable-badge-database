from borValBadgeDbServer.models.query_by_badge_ids_get200_response import QueryByBadgeIdsGet200Response  # noqa: E501
from borValBadgeDbServer.models.query_by_universe_ids_get200_response import QueryByUniverseIdsGet200Response  # noqa: E501

from borValBadgeDbServer.models.badge_info import BadgeInfo
from borValBadgeDbServer.models.universe_info import UniverseInfo

from borValBadgeDbServer.db.db import getBadgeDB, getBadgeIdCache, isNVL

import traceback
import time


def query_by_badge_ids_get(badge_ids):  # noqa: E501
    """Look up creation dates and values of badge ids

     # noqa: E501

    :param badge_ids: The CSV of badge ids
    :type badge_ids: List[int]

    :rtype: Union[QueryByBadgeIdsGet200Response, Tuple[QueryByBadgeIdsGet200Response, int], Tuple[QueryByBadgeIdsGet200Response, int, Dict[str, str]]
    """

    for _attempt in range(5):
        try:
            badge_ids_todo = {int(x) for x in badge_ids}
            ret = []

            idsToGet = badge_ids_todo & getBadgeIdCache().keys()
            for badgeId in idsToGet:
                universeId = getBadgeIdCache()[badgeId]
                if str(badgeId) in getBadgeDB().universes[universeId].badges:
                    ret.append(getBadgeDB().universes[universeId].badges[str(badgeId)])
                else:
                    ret.append(BadgeInfo(badgeId, True, 0, int(universeId), 0, isNVL(badgeId)))
            badge_ids_todo -= idsToGet

            for missingId in badge_ids_todo - idsToGet:
                ret.append(BadgeInfo(missingId, False))
            return QueryByBadgeIdsGet200Response(ret)
        except Exception:
            traceback.print_exc()
            time.sleep(0.1)
    raise RuntimeError


def query_by_badge_ids_post(body):  # noqa: E501
    """Look up creation dates and values of badge ids

     # noqa: E501

    :param body: The CSV of badge ids
    :type body: str

    :rtype: Union[QueryByBadgeIdsGet200Response, Tuple[QueryByBadgeIdsGet200Response, int], Tuple[QueryByBadgeIdsGet200Response, int, Dict[str, str]]
    """

    return query_by_badge_ids_get(body.decode().split(","))


def query_by_universe_ids_get(universe_ids):  # noqa: E501
    """Look up creation dates and values of all badges under universes

     # noqa: E501

    :param universe_ids: The CSV of universe ids
    :type universe_ids: List[int]

    :rtype: Union[QueryByUniverseIdsGet200Response, Tuple[QueryByUniverseIdsGet200Response, int], Tuple[QueryByUniverseIdsGet200Response, int, Dict[str, str]]
    """

    universe_ids = {str(x) for x in universe_ids}

    for _attempt in range(5):
        try:
            ret = []
            idsToGet = universe_ids & set(getBadgeDB().universes.keys())
            for universeId in idsToGet:
                ret.append(getBadgeDB().universes[universeId])

            for missingId in universe_ids - idsToGet:
                ret.append(UniverseInfo(missingId, False))

            return QueryByUniverseIdsGet200Response(ret)
        except Exception:
            traceback.print_exc()
            time.sleep(0.1)
    raise RuntimeError


def query_by_universe_ids_post(body):  # noqa: E501
    """Look up creation dates and values of all badges under universes

     # noqa: E501

    :param body: The CSV of universe ids
    :type body: str

    :rtype: Union[QueryByUniverseIdsGet200Response, Tuple[QueryByUniverseIdsGet200Response, int], Tuple[QueryByUniverseIdsGet200Response, int, Dict[str, str]]
    """

    return query_by_universe_ids_get(body.decode().split(","))
