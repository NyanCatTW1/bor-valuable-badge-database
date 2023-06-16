# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from borValBadgeDbServer.models.database import Database  # noqa: E501
from borValBadgeDbServer.models.user_request_check_get200_response import UserRequestCheckGet200Response  # noqa: E501
from borValBadgeDbServer.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_user_request_check_get(self):
        """Test case for user_request_check_get

        Request a check/recheck of an universe. Gets ignored if the universe was last checked <5 mins ago
        """
        query_string = [('universeId', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v3/user/requestcheck',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
