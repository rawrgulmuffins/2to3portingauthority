import unittest
from unittest.mock import MagicMock
import logging

from testfixtures import LogCapture


class TestPortingAuthorityMiscFunctions(unittest.TestCase):

    def test_xmlrpc_client_bad_url(self):
        with LogCapture() as l:
            bad_pypi_url = "I'm a very bad url"
            python_pa.get_xmlrpc_client(pypi_url=bad_pypi_url)
            expected_logs = (
                (
                    "python_pa",
                    "CRITICAL",
                    "Wasn't able to connect to '{}'. Giving up.".format(
                        bad_pypi_url)))
            l.check(expected_logs)
