import unittest

from testfixtures import log_capture

import python_porting_authority as python_pa

class TestPortingAuthorityMiscFunctions(unittest.TestCase):

    @log_capture
    def test_xmlrpc_client_bad_url(self):
        python_pa.get_xml_rpc(pypi_url="i'm a bad url")
        l.check("2to3_pa", "CRITICAL", "Wasn't able to connect to '{}'. Giving up.")

    def test_xmlrpc_client_bad_url(self):
        """
        This test requires the interwebs.  Could fail for many valid reasons.
        """
        #2to3pa.get_xml_rpc(pypi_url="i'm a bad url")
        pass

    def test_column_not_matrix(self):
        pass

    def test_column_index_out_of_range(self):
        pass

class TestGetPython2PackageNames(unittest.TestCase):
    
    def test_browse_returns_nothing(self):
        """
        XMLRPC's can have server errors that lead to no data. Handle that case
        """
        pass

    def test_list_packages_returns_nothing(self):
        """
        XMLRPC's can have server errors that lead to no data. Handle that case
        """
        pass

    def test_pypi_api_changes(self):
        """
        If there is an api change detect the change and report what's happened.
        """
        pass
