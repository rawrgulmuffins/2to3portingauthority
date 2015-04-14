"""
This is a stand alone command line program which will deliver a random python
package which has yet to be ported to python3.
"""
try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib
from random import randint
import logging

def column(matrix, i):
    return [row[i] for row in matrix]

def get_xmlrpc_client(logger, pypi_url="https://pypi.python.org/pypi"):
    """
    Retrieve a pypi xmlrpc client connection by which you can query package
    information from pypi.
    """
    try:
        return xmlrpclib.ServerProxy(pypi_url)
    except xmlrpc.client.ProtocolError:
        logger.critical("Wasn't able to connect to {}. Giving up.".format(
            pypi_url))

def get_python2_package_names(xmlrpc_client):
    """
    Use the pypi xmlrpc to retrieve the names of python3 ready packages and
    all the package names. Return a list of all package names - python3 ready
    packages.
    """
    classifiers=["Programming Language :: Python :: 3"]
    python3_package_names_versions = xmlrpc_client.browse(classifiers)
    python3_package_names = set(column(python3_package_names_versions, 0))
    all_package_names = set(xmlrpc_client.list_packages())
    return list(all_package_names.difference(python3_package_names))

def main():
    logger = logging.getLogger("porting_authority")
    xmlrpc_client = get_xmlrpc_client(logger)
    python2_package_names = get_python2_package_names(xmlrpc_client)
    package_index = randint(0, len(python2_package_names))
    selected_package_name = python2_package_names[package_index]
    print(selected_package_name)

if __name__ == "__main__":
    main()
