from borValBadgeDbServer.models.query_by_badge_ids_get200_response import QueryByBadgeIdsGet200Response  # noqa: E501
from borValBadgeDbServer.models.query_by_universe_ids_get200_response import QueryByUniverseIdsGet200Response  # noqa: E501

from borValBadgeDbServer.models.badge_info import BadgeInfo
from borValBadgeDbServer.models.universe_info import UniverseInfo

from borValBadgeDbServer.db.db import getBadgeDB, getBadgeIdCache


def query_by_badge_ids_get(badge_ids):  # noqa: E501
    """Look up creation dates and values of badge ids

     # noqa: E501

    :param badge_ids: The CSV of badge ids
    :type badge_ids: List[int]

    :rtype: Union[QueryByBadgeIdsGet200Response, Tuple[QueryByBadgeIdsGet200Response, int], Tuple[QueryByBadgeIdsGet200Response, int, Dict[str, str]]
    """

    badge_ids = {int(x) for x in badge_ids}
    ret = []

    for universeId in getBadgeDB().universes.keys():
        idsToGet = badge_ids & getBadgeIdCache(universeId)
        for badgeId in idsToGet:
            if str(badgeId) in getBadgeDB().universes[universeId].badges:
                ret.append(getBadgeDB().universes[universeId].badges[str(badgeId)])
            else:
                ret.append(BadgeInfo(badgeId, True, 0, int(universeId), 0))
        badge_ids -= idsToGet

    for missingId in badge_ids:
        ret.append(BadgeInfo(missingId, False))
    return QueryByBadgeIdsGet200Response(ret)


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
    ret = []
    idsToGet = universe_ids & set(getBadgeDB().universes.keys())
    for universeId in idsToGet:
        ret.append(getBadgeDB().universes[universeId])

    for missingId in universe_ids - idsToGet:
        ret.append(UniverseInfo(missingId, False))

    return QueryByUniverseIdsGet200Response(ret)


def query_by_universe_ids_post(body):  # noqa: E501
    """Look up creation dates and values of all badges under universes

     # noqa: E501

    :param body: The CSV of universe ids
    :type body: str

    :rtype: Union[QueryByUniverseIdsGet200Response, Tuple[QueryByUniverseIdsGet200Response, int], Tuple[QueryByUniverseIdsGet200Response, int, Dict[str, str]]
    """

    return query_by_universe_ids_get(body.decode().split(","))
