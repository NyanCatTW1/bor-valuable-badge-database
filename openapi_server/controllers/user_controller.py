import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.database import Database  # noqa: E501
from openapi_server.models.user_request_check_get200_response import UserRequestCheckGet200Response  # noqa: E501
from openapi_server import util


def user_dump_dbget():  # noqa: E501
    """Get a dump of the entire database. Updates every five minutes

     # noqa: E501


    :rtype: Union[Database, Tuple[Database, int], Tuple[Database, int, Dict[str, str]]
    """
    return 'do some magic!'


def user_request_check_get(universe_id):  # noqa: E501
    """Request a check/recheck of an universe. Gets ignored if the universe was last checked &lt;5 mins ago

     # noqa: E501

    :param universe_id: The universe id to check
    :type universe_id: int

    :rtype: Union[UserRequestCheckGet200Response, Tuple[UserRequestCheckGet200Response, int], Tuple[UserRequestCheckGet200Response, int, Dict[str, str]]
    """
    return 'do some magic!'
