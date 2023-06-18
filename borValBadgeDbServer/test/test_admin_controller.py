# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from borValBadgeDbServer.models.admin_purge_universe_infos_get200_response import AdminPurgeUniverseInfosGet200Response  # noqa: E501
from borValBadgeDbServer.models.database import Database  # noqa: E501
from borValBadgeDbServer.models.user_request_check_get200_response import UserRequestCheckGet200Response  # noqa: E501
from borValBadgeDbServer.test import BaseTestCase


class TestAdminController(BaseTestCase):
    """AdminController integration test stubs"""

    def test_admin_dump_dbget(self):
        """Test case for admin_dump_dbget

        Get a dump of the entire database right now
        """
        headers = { 
            'Accept': 'application/json',
            'ApiKeyAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v3/admin/dumpdb',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_purge_universe_infos_get(self):
        """Test case for admin_purge_universe_infos_get

        Purge cached info of universes and all associated badges
        """
        query_string = [('universeIds', [56])]
        headers = { 
            'Accept': 'application/json',
            'ApiKeyAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v3/admin/purgeuniverseinfos',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("text/plain not supported by Connexion")
    def test_admin_purge_universe_infos_post(self):
        """Test case for admin_purge_universe_infos_post

        Purge cached info of universes and all associated badges
        """
        body = 'body_example'
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'text/plain',
            'ApiKeyAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v3/admin/purgeuniverseinfos',
            method='POST',
            headers=headers,
            data=json.dumps(body),
            content_type='text/plain')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_refresh_db_get(self):
        """Test case for admin_refresh_db_get

        Redetermine values of all badges in the database
        """
        headers = { 
            'Accept': 'application/json',
            'ApiKeyAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v3/admin/refreshdb',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_admin_start_check_get(self):
        """Test case for admin_start_check_get

        Start a check/recheck of an universe
        """
        query_string = [('universeId', 56)]
        headers = { 
            'Accept': 'application/json',
            'ApiKeyAuth': 'special-key',
        }
        response = self.client.open(
            '/api/v3/admin/startcheck',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
