from borValBadgeDbServer.models.user_request_check_get200_response import UserRequestCheckGet200Response  # noqa: E501
from borValBadgeDbServer.models.user_report_missing_get200_response import UserReportMissingGet200Response  # noqa: E501
from borValBadgeDbServer import util
from borValBadgeDbServer.db.db import getBadgeDB, getBadgeIdCache
from borValBadgeDbServer.db.checker import check_in_progress, startCheck, reportMissing

import traceback
import time


def user_report_missing_get(badge_ids):  # noqa: E501
    """Run checks based on missing/unknown badge ids

     # noqa: E501

    :param badge_ids: The CSV of badge ids
    :type badge_ids: List[int]

    :rtype: Union[UserReportMissingGet200Response, Tuple[UserReportMissingGet200Response, int], Tuple[UserReportMissingGet200Response, int, Dict[str, str]]
    """

    for _attempt in range(5):
        try:
            badge_ids_todo = {int(x) for x in badge_ids} - getBadgeIdCache().keys()
            return UserReportMissingGet200Response(reportMissing({str(x) for x in badge_ids_todo}), len(badge_ids_todo))
        except Exception:
            traceback.print_exc()
            time.sleep(0.1)
    raise RuntimeError


def user_report_missing_post(body):  # noqa: E501
    """Run checks based on missing/unknown badge ids

     # noqa: E501

    :param body: The CSV of badge ids
    :type body: str

    :rtype: Union[UserReportMissingGet200Response, Tuple[UserReportMissingGet200Response, int], Tuple[UserReportMissingGet200Response, int, Dict[str, str]]
    """

    return user_report_missing_get(body.decode().split(","))


def user_request_check_get(universe_id):  # noqa: E501
    """Request a check/recheck of an universe. Gets ignored if the universe was last checked &lt;5 mins ago

     # noqa: E501

    :param universe_id: The universe id to check
    :type universe_id: int

    :rtype: Union[UserRequestCheckGet200Response, Tuple[UserRequestCheckGet200Response, int], Tuple[UserRequestCheckGet200Response, int, Dict[str, str]]
    """

    universe_id = str(universe_id)

    for _attempt in range(5):
        try:
            last_checked = 0
            if universe_id in getBadgeDB().universes:
                last_checked = getBadgeDB().universes[universe_id].last_checked

            if util.getTimestamp() - last_checked >= 5 * 60:
                startCheck(universe_id)

            return UserRequestCheckGet200Response(last_checked, check_in_progress(universe_id))
        except Exception:
            traceback.print_exc()
            time.sleep(0.1)
    raise RuntimeError
