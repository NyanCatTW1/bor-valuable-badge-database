# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.database import Database  # noqa: E501
from openapi_server.models.user_request_check_get200_response import UserRequestCheckGet200Response  # noqa: E501
from openapi_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_user_dump_dbget(self):
        """Test case for user_dump_dbget

        Get a dump of the entire database. Updates every five minutes
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v3/user/dumpDB',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_user_request_check_get(self):
        """Test case for user_request_check_get

        Request a check/recheck of an universe. Gets ignored if the universe was last checked <5 mins ago
        """
        query_string = [('universeId', 56)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v3/user/requestCheck',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
