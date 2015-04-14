"""
This is a stand alone command line program which will deliver a random python
package which has yet to be ported to python3.

USAGE: python_porting_authority
    Currently no arguments.
"""
try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib
from random import randint
import logging

SERVER_PROXY_ERROR_MSG = "Wasn't able to connect to '{}'. Giving up."
EMPTY_PYTHON3_RETURN = ("Retrieved no package names from pypi which are"
    "python3 ready.")
EMPTY_2_AND_3_RETURN = ("Recieved no python packages or python3 ready packages. "
    "Most likely passed an empty pypi server.")
WAS_3_NOTHING_IN_COMPLETE_LIST = ("Recieved no python packages after getting"
    "python3 ready packages. Most likely race condition error. See if error "
    "happens again.")

def column(matrix, i):
    """
    Found at http://stackoverflow.com/questions/903853/how-to-extract-column-from-a-multi-dimentional-array
    """
    return [row[i] for row in matrix]

def get_xmlrpc_client(pypi_url="https://pypi.python.org/pypi"):
    """
    Retrieve a pypi xmlrpc client connection by which you can query package
    information from pypi.
    """
    logger = logging.getLogger("python_pa")
    try:
        return xmlrpclib.ServerProxy(pypi_url)
    except (xmlrpclib.ProtocolError, OSError):
        logger.critical(SERVER_PROXY_ERROR_MSG.format(pypi_url))

def get_python2_package_names(xmlrpc_client):
    """
    Use the pypi xmlrpc to retrieve the names of python3 ready packages and
    all the package names. Return a list of all package names - python3 ready
    packages.
    """
    logger = logging.getLogger("python_pa")
    classifiers=["Programming Language :: Python :: 3"]
    python3_package_names_versions = xmlrpc_client.browse(classifiers)
    python3_package_names = set(column(python3_package_names_versions, 0))
    if python3_package_names == set([]):
        logger.warning(EMPTY_PYTHON3_RETURN)
    all_package_names = set(xmlrpc_client.list_packages())
    if all_package_names == set([]):
        if python3_package_names == set([]):
            # Probably a broken pypi server.
            logger.warning(EMPTY_2_AND_3_RETURN)
        else:
            # Something died in the matrix.
            logger.critical(WAS_3_NOTHING_IN_COMPLETE_LIST)
    return list(all_package_names.difference(python3_package_names))

def main():
    logger = logging.getLogger("python_pa")
    xmlrpc_client = get_xmlrpc_client()
    python2_package_names = get_python2_package_names(xmlrpc_client)
    package_index = randint(0, len(python2_package_names))
    selected_package_name = python2_package_names[package_index]
    print(selected_package_name)

if __name__ == "__main__":
    main()
