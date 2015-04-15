"""
This module is used to find the projects which have the most projects waiting
for them to be ported.
"""
from collections import Counter
from pprint import pprint

import caniusepython3
from caniusepython3.dependencies import blocking_dependencies

all_py_projects = list(caniusepython3.pypi.all_projects())
py3_projects = caniusepython3.pypi.all_py3_projects()
all_blockers = blocking_dependencies(
    all_py_projects,
    py3_projects)
blocker_list = []
for blockers_subset in all_blockers:
    for blocker in blockers_subset:
        blocker_list.append(blocker)
blockers_counter = Counter(blocker_list)
pprint(blockers_counter.most_common())
