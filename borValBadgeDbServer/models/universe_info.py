# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from borValBadgeDbServer.models.base_model_ import Model
from borValBadgeDbServer.models.badge_info import BadgeInfo
from borValBadgeDbServer import util


class UniverseInfo(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, universe_id=0, found=True, last_checked=0, name="Unknown", badge_count=0, free_badges=None, badges=None):  # noqa: E501
        """UniverseInfo - a model defined in OpenAPI

        :param universe_id: The universe_id of this UniverseInfo.  # noqa: E501
        :type universe_id: int
        :param found: The found of this UniverseInfo.  # noqa: E501
        :type found: bool
        :param last_checked: The last_checked of this UniverseInfo.  # noqa: E501
        :type last_checked: int
        :param name: The name of this UniverseInfo.  # noqa: E501
        :type name: str
        :param badge_count: The badge_count of this UniverseInfo.  # noqa: E501
        :type badge_count: int
        :param free_badges: The free_badges of this UniverseInfo.  # noqa: E501
        :type free_badges: List[str]
        :param badges: The badges of this UniverseInfo.  # noqa: E501
        :type badges: Dict[str, BadgeInfo]
        """

        if free_badges is None:
            free_badges = []

        if badges is None:
            badges = {}

        self.openapi_types = {
            'universe_id': int,
            'found': bool,
            'last_checked': int,
            'name': str,
            'badge_count': int,
            'free_badges': List[str],
            'badges': Dict[str, BadgeInfo]
        }

        self.attribute_map = {
            'universe_id': 'universe_id',
            'found': 'found',
            'last_checked': 'last_checked',
            'name': 'name',
            'badge_count': 'badge_count',
            'free_badges': 'free_badges',
            'badges': 'badges'
        }

        self._universe_id = universe_id
        self._found = found
        self._last_checked = last_checked
        self._name = name
        self._badge_count = badge_count
        self._free_badges = free_badges
        self._badges = badges

    @classmethod
    def from_dict(cls, dikt) -> 'UniverseInfo':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The UniverseInfo of this UniverseInfo.  # noqa: E501
        :rtype: UniverseInfo
        """
        return util.deserialize_model(dikt, cls)

    @property
    def universe_id(self):
        """Gets the universe_id of this UniverseInfo.


        :return: The universe_id of this UniverseInfo.
        :rtype: int
        """
        return self._universe_id

    @universe_id.setter
    def universe_id(self, universe_id):
        """Sets the universe_id of this UniverseInfo.


        :param universe_id: The universe_id of this UniverseInfo.
        :type universe_id: int
        """

        self._universe_id = universe_id

    @property
    def found(self):
        """Gets the found of this UniverseInfo.


        :return: The found of this UniverseInfo.
        :rtype: bool
        """
        return self._found

    @found.setter
    def found(self, found):
        """Sets the found of this UniverseInfo.


        :param found: The found of this UniverseInfo.
        :type found: bool
        """

        self._found = found

    @property
    def last_checked(self):
        """Gets the last_checked of this UniverseInfo.


        :return: The last_checked of this UniverseInfo.
        :rtype: int
        """
        return self._last_checked

    @last_checked.setter
    def last_checked(self, last_checked):
        """Sets the last_checked of this UniverseInfo.


        :param last_checked: The last_checked of this UniverseInfo.
        :type last_checked: int
        """

        self._last_checked = last_checked

    @property
    def name(self):
        """Gets the name of this UniverseInfo.


        :return: The name of this UniverseInfo.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UniverseInfo.


        :param name: The name of this UniverseInfo.
        :type name: str
        """

        self._name = name

    @property
    def badge_count(self):
        """Gets the badge_count of this UniverseInfo.


        :return: The badge_count of this UniverseInfo.
        :rtype: int
        """
        return self._badge_count

    @badge_count.setter
    def badge_count(self, badge_count):
        """Sets the badge_count of this UniverseInfo.


        :param badge_count: The badge_count of this UniverseInfo.
        :type badge_count: int
        """

        self._badge_count = badge_count

    @property
    def free_badges(self):
        """Gets the free_badges of this UniverseInfo.


        :return: The free_badges of this UniverseInfo.
        :rtype: List[str]
        """
        return self._free_badges

    @free_badges.setter
    def free_badges(self, free_badges):
        """Sets the free_badges of this UniverseInfo.


        :param free_badges: The free_badges of this UniverseInfo.
        :type free_badges: List[str]
        """

        self._free_badges = free_badges

    @property
    def badges(self):
        """Gets the badges of this UniverseInfo.


        :return: The badges of this UniverseInfo.
        :rtype: Dict[str, BadgeInfo]
        """
        return self._badges

    @badges.setter
    def badges(self, badges):
        """Sets the badges of this UniverseInfo.


        :param badges: The badges of this UniverseInfo.
        :type badges: Dict[str, BadgeInfo]
        """

        self._badges = badges
