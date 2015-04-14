"""
This is a stand alone command line program which will deliver a random python
package which has yet to be ported to python3.
"""
try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib
import pprint

def column(matrix, i):
    return [row[i] for row in matrix]

def main():
    client = xmlrpclib.ServerProxy("https://pypi.python.org/pypi")
    classifiers=["Programming Language :: Python :: 3"]
    python3_package_names_versions = client.browse(classifiers)
    python3_package_names = column(python3_package_names_versions, 0)
    pprint.pprint(python3_package_names)

if __name__ == "__main__":
    main()
