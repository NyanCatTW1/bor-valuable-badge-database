import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.query_by_badge_ids_get200_response import QueryByBadgeIdsGet200Response  # noqa: E501
from openapi_server.models.query_by_universe_ids_get200_response import QueryByUniverseIdsGet200Response  # noqa: E501
from openapi_server import util


def query_by_badge_ids_get(badge_ids):  # noqa: E501
    """Look up creation dates and values of badge ids

     # noqa: E501

    :param badge_ids: The CSV of badge ids
    :type badge_ids: List[int]

    :rtype: Union[QueryByBadgeIdsGet200Response, Tuple[QueryByBadgeIdsGet200Response, int], Tuple[QueryByBadgeIdsGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def query_by_badge_ids_post(body):  # noqa: E501
    """Look up creation dates and values of badge ids

     # noqa: E501

    :param body: The CSV of badge ids
    :type body: str

    :rtype: Union[QueryByBadgeIdsGet200Response, Tuple[QueryByBadgeIdsGet200Response, int], Tuple[QueryByBadgeIdsGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def query_by_universe_ids_get(universe_ids):  # noqa: E501
    """Look up creation dates and values of all badges under universes

     # noqa: E501

    :param universe_ids: The CSV of universe ids
    :type universe_ids: List[int]

    :rtype: Union[QueryByUniverseIdsGet200Response, Tuple[QueryByUniverseIdsGet200Response, int], Tuple[QueryByUniverseIdsGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def query_by_universe_ids_post(body):  # noqa: E501
    """Look up creation dates and values of all badges under universes

     # noqa: E501

    :param body: The CSV of universe ids
    :type body: str

    :rtype: Union[QueryByUniverseIdsGet200Response, Tuple[QueryByUniverseIdsGet200Response, int], Tuple[QueryByUniverseIdsGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'
