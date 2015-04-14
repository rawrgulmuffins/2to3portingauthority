import unittest
from unittest.mock import MagicMock
import logging
try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib

from testfixtures import LogCapture

import python_porting_authority as python_pa

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

    def test_xmlrpc_client_default_url(self):
        """
        This test requires the interwebs.  Could fail for many valid reasons.
        """
        xmlrpc_client = python_pa.get_xmlrpc_client()
        self.assertEqual(type(xmlrpc_client), xmlrpclib.ServerProxy)

    def test_xmlrpc_client_good_passed_url(self):
        """
        This test requires the interwebs.  Could fail for many valid reasons.
        """
        xmlrpc_client = python_pa.get_xmlrpc_client(
            pypi_url="https://pypi.python.org/pypi")
        self.assertEqual(type(xmlrpc_client), xmlrpclib.ServerProxy)

    def test_column_not_matrix(self):
        test_list = []
        actual_list = python_pa.column(test_list, 0)
        expected_list = []
        self.assertEqual(expected_list, actual_list)

    def test_column_index_out_of_range(self):
        test_list = [[1, 2], [3, 4]]
        with self.assertRaises(IndexError):
            python_pa.column(test_list, 2)

class TestGetPython2PackageNames(unittest.TestCase):

    def test_browse_returns_nothing(self):
        """
        XMLRPC's can have server errors that lead to no data. If we get no
        python packages that are three ready log a warning.
        """
        with LogCapture() as l:
            xmlrpc_client = xmlrpclib.ServerProxy
            xmlrpc_client.browse = MagicMock(return_value=[])
            xmlrpc_client.list_packages = MagicMock(return_value=["a_package"])
            python_pa.get_python2_package_names(xmlrpc_client)
            expected_logs = (
                (
                    "python_pa",
                    "WARNING",
                    python_pa.EMPTY_PYTHON3_RETURN))
            l.check(expected_logs)

    def test_list_packages_returns_nothing_after_getting_3_packages(self):
        """
        XMLRPC's can have server errors that lead to no data. If we got python3
        packages but nothing during the complete list request, log a critical
        warning and exit.
        """
        with LogCapture() as l:
            xmlrpc_client = xmlrpclib.ServerProxy
            xmlrpc_client.browse = MagicMock(return_value=["python3_ready"])
            xmlrpc_client.list_packages = MagicMock(return_value=[])
            python_pa.get_python2_package_names(xmlrpc_client)
            expected_logs = (
                (
                    "python_pa",
                    "CRITICAL",
                    python_pa.WAS_3_NOTHING_IN_COMPLETE_LIST))
            l.check(expected_logs)

    def test_list_packages_returns_nothing_after_getting_no_3_packages(self):
        """
        XMLRPC's can have server errors that lead to no data. If we recieved
        no python3 then log a warning about getting no python packages at
        all.
        """
        with LogCapture() as l:
            xmlrpc_client = xmlrpclib.ServerProxy
            xmlrpc_client.browse = MagicMock(return_value=[])
            xmlrpc_client.list_packages = MagicMock(return_value=[])
            python_pa.get_python2_package_names(xmlrpc_client)
            expected_logs = [
                ("python_pa", "WARNING", python_pa.EMPTY_PYTHON3_RETURN,),
                ("python_pa", "WARNING", python_pa.EMPTY_2_AND_3_RETURN,)]
            print(l)
            print(expected_logs)
            l.check(*expected_logs)

    def test_pypi_api_changes(self):
        """
        If there is an api change detect the change and report what's happened.
        """
        pass
