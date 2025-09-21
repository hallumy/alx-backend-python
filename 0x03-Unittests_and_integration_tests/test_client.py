#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized


with patch("client.memoize", lambda x: x):
    from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json') 
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct data and calls get_json once"""
        expected_data = {"login": org_name}
        mock_get_json.return_value = expected_data

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_data)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
