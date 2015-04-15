"""
This is a stand alone command line program which will deliver a random python
package which has yet to be ported to python3.

USAGE: python_porting_authority
    Currently no arguments.
"""
from random import randint
import logging

import caniusepython3


def main():
    logger = logging.getLogger("python_pa")
    py2_projects = caniusepython3.pypi.all_projects()
    py3_projects = caniusepython3.pypi.all_py3_projects()
    py2_only_projects = set(py2_projects).difference(set(py3_projects))
    package_index = randint(0, len(py2_only_projects))
    selected_package_name = list(py2_only_projects)[package_index]
    print(selected_package_name)

if __name__ == "__main__":
    main()
