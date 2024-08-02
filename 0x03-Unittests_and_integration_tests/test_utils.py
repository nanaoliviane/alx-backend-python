#!/usr/bin/env python3
"""Module for testing utility functions."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
import requests


class TestAccessNestedMap(unittest.TestCase):
    """Class for testing access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the correct value.

        Args:
            nested_map (dict): The nested dictionary to access.
            path (tuple): The path of keys to access in the nested dictionary.
            expected (any): The expected value to be returned by access_nested_map.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """
        Test that a KeyError is raised for the respective inputs.

        Args:
            nested_map (dict): The nested dictionary to access.
            path (tuple): The path of keys to access in the nested dictionary.
            expected (str): The expected key causing the KeyError.
        """
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual(f"KeyError('{expected}')", repr(e.exception))


class TestGetJson(unittest.TestCase):
    """Class for testing get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test that get_json returns the expected result.

        Args:
            test_url (str): The URL to fetch JSON from.
            test_payload (dict): The expected JSON payload to be returned.
        """
        config = {'return_value.json.return_value': test_payload}
        patcher = patch('requests.get', **config)
        mock = patcher.start()
        self.assertEqual(get_json(test_url), test_payload)
        mock.assert_called_once()
        patcher.stop()


class TestMemoize(unittest.TestCase):
    """Class for testing memoize decorator."""

    def test_memoize(self):
        """
        Test that when calling a_property twice, the correct result is returned
        but a_method is only called once using assert_called_once.
        """

        class TestClass:
            """Test class for testing memoize decorator."""

            def a_method(self):
                """Method that returns a fixed value."""
                return 42

            @memoize
            def a_property(self):
                """Property method that uses memoize decorator."""
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock:
            test_class = TestClass()
            self.assertEqual(test_class.a_property, 42)
            self.assertEqual(test_class.a_property, 42)
            mock.assert_called_once()


if __name__ == "__main__":
    unittest.main()
