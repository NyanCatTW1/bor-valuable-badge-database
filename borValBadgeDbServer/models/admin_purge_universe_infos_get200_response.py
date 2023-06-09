# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from borValBadgeDbServer.models.base_model_ import Model
from borValBadgeDbServer import util


class AdminPurgeUniverseInfosGet200Response(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, badges_affected=None):  # noqa: E501
        """AdminPurgeUniverseInfosGet200Response - a model defined in OpenAPI

        :param badges_affected: The badges_affected of this AdminPurgeUniverseInfosGet200Response.  # noqa: E501
        :type badges_affected: int
        """
        self.openapi_types = {
            'badges_affected': int
        }

        self._badges_affected = badges_affected

    @classmethod
    def from_dict(cls, dikt) -> 'AdminPurgeUniverseInfosGet200Response':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The _admin_purgeuniverseinfos_get_200_response of this AdminPurgeUniverseInfosGet200Response.  # noqa: E501
        :rtype: AdminPurgeUniverseInfosGet200Response
        """
        return util.deserialize_model(dikt, cls)

    @property
    def badges_affected(self):
        """Gets the badges_affected of this AdminPurgeUniverseInfosGet200Response.


        :return: The badges_affected of this AdminPurgeUniverseInfosGet200Response.
        :rtype: int
        """
        return self._badges_affected

    @badges_affected.setter
    def badges_affected(self, badges_affected):
        """Sets the badges_affected of this AdminPurgeUniverseInfosGet200Response.


        :param badges_affected: The badges_affected of this AdminPurgeUniverseInfosGet200Response.
        :type badges_affected: int
        """

        self._badges_affected = badges_affected
