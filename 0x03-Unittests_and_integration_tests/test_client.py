#!/usr/bin/env python3
"""Module for testing GithubOrgClient and its methods."""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Class for testing GithubOrgClient methods."""

    @parameterized.expand([
        ('google',),
        ('abc',),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.

        Args:
            org_name (str): The organization name to test.
            mock_get_json (Mock): Mocked get_json method.
        """
        test_instance = GithubOrgClient(org_name)
        test_instance.org()
        mock_get_json.assert_called_once_with(f'https://api.github.com/orgs/{org_name}')

    def test_public_repos_url(self):
        """
        Test that GithubOrgClient._public_repos_url returns the expected value
        based on the mocked payload.
        """
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
            mock_org.return_value = payload
            test_instance = GithubOrgClient('test_org')
            result = test_instance._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns the correct list of repos
        based on the mocked payload.

        Args:
            mock_get_json (Mock): Mocked get_json method.
        """
        json_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = json_payload

        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/test_org/repos"
            test_instance = GithubOrgClient('test_org')
            result = test_instance.public_repos()

            expected_repos = [repo["name"] for repo in json_payload]
            self.assertEqual(result, expected_repos)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test_org/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test GithubOrgClient.has_license method.

        Args:
            repo (dict): Repository data.
            license_key (str): License key to check.
            expected (bool): Expected result.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test case for GithubOrgClient class using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Set up the class by mocking requests.get to return example payloads."""
        config = {'return_value.json.side_effect': [
            cls.org_payload, cls.repos_payload,
            cls.org_payload, cls.repos_payload
        ]}
        cls.get_patcher = patch('requests.get', **config)
        cls.mock = cls.get_patcher.start()

    def test_public_repos(self):
        """Integration test for GithubOrgClient.public_repos method."""
        test_instance = GithubOrgClient("google")
        self.assertEqual(test_instance.org, self.org_payload)
        self.assertEqual(test_instance.repos_payload, self.repos_payload)
        self.assertEqual(test_instance.public_repos(), self.expected_repos)
        self.assertEqual(test_instance.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self):
        """Integration test for GithubOrgClient.public_repos method with license filtering."""
        test_instance = GithubOrgClient("google")
        self.assertEqual(test_instance.public_repos(), self.expected_repos)
        self.assertEqual(test_instance.public_repos("XLICENSE"), [])
        self.assertEqual(test_instance.public_repos("apache-2.0"), self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls):
        """Tear down the class by stopping the patcher."""
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()
