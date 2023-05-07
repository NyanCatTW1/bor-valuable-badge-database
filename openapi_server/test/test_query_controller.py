# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.query_by_badge_ids_get200_response import QueryByBadgeIdsGet200Response  # noqa: E501
from openapi_server.models.query_by_universe_ids_get200_response import QueryByUniverseIdsGet200Response  # noqa: E501
from openapi_server.test import BaseTestCase


class TestQueryController(BaseTestCase):
    """QueryController integration test stubs"""

    def test_query_by_badge_ids_get(self):
        """Test case for query_by_badge_ids_get

        Look up creation dates and values of badge ids
        """
        query_string = [('badgeIds', [56])]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v3/query/byBadgeIds',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("text/plain not supported by Connexion")
    def test_query_by_badge_ids_post(self):
        """Test case for query_by_badge_ids_post

        Look up creation dates and values of badge ids
        """
        body = 'body_example'
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'text/plain',
        }
        response = self.client.open(
            '/api/v3/query/byBadgeIds',
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='text/plain')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_query_by_universe_ids_get(self):
        """Test case for query_by_universe_ids_get

        Look up creation dates and values of all badges under universes
        """
        query_string = [('universeIds', [56])]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v3/query/byUniverseIds',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("text/plain not supported by Connexion")
    def test_query_by_universe_ids_post(self):
        """Test case for query_by_universe_ids_post

        Look up creation dates and values of all badges under universes
        """
        body = 'body_example'
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'text/plain',
        }
        response = self.client.open(
            '/api/v3/query/byUniverseIds',
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='text/plain')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
