# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from borValBadgeDbServer.models.base_model_ import Model
from borValBadgeDbServer import util


class UserReportMissingGet200Response(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, added_to_queue=None):  # noqa: E501
        """UserReportMissingGet200Response - a model defined in OpenAPI

        :param added_to_queue: The added_to_queue of this UserReportMissingGet200Response.  # noqa: E501
        :type added_to_queue: int
        """
        self.openapi_types = {
            'added_to_queue': int
        }

        self.attribute_map = {
            'added_to_queue': 'addedToQueue'
        }

        self._added_to_queue = added_to_queue

    @classmethod
    def from_dict(cls, dikt) -> 'UserReportMissingGet200Response':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The _user_reportMissing_get_200_response of this UserReportMissingGet200Response.  # noqa: E501
        :rtype: UserReportMissingGet200Response
        """
        return util.deserialize_model(dikt, cls)

    @property
    def added_to_queue(self):
        """Gets the added_to_queue of this UserReportMissingGet200Response.


        :return: The added_to_queue of this UserReportMissingGet200Response.
        :rtype: int
        """
        return self._added_to_queue

    @added_to_queue.setter
    def added_to_queue(self, added_to_queue):
        """Sets the added_to_queue of this UserReportMissingGet200Response.


        :param added_to_queue: The added_to_queue of this UserReportMissingGet200Response.
        :type added_to_queue: int
        """

        self._added_to_queue = added_to_queue