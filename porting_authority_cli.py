"""
This is a stand alone command line program which will deliver a random python
package which has yet to be ported to python3.
"""
try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib
from random import randint

def column(matrix, i):
    return [row[i] for row in matrix]

def main():
    client = xmlrpclib.ServerProxy("https://pypi.python.org/pypi")
    classifiers=["Programming Language :: Python :: 3"]
    python3_package_names_versions = client.browse(classifiers)
    python3_package_names = set(column(python3_package_names_versions, 0))
    all_package_names = set(client.list_packages())
    python2_only_package_name = all_package_names.difference(
        python3_package_names)
    package_index = randint(0, len(python2_only_package_name))
    selected_package_name = list(python2_only_package_name)[package_index]
    print(selected_package_name)

if __name__ == "__main__":
    main()
