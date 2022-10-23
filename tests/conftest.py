# import json
# from typing import Any, Dict, List

import pytest

from unilist import Unilist
# from unilist.readwrite import read_local_file, write_local_file

# Unilist.setup({ 'virtual': { 'roots': { 'tmp', './tmp' } } })

# def load_test_data() -> List[Dict[str, Any]]:
#     """Load test data from JSON file.
#     :return: Test data.
#     :rtype: Dict[str, Any]
#     """

#     uri = 'tests/test_data/colors.txt'
#     return list(read_local_file(uri))


@pytest.fixture
def unilist() -> Unilist:
    """Return a supply curve for use with tests.
    :return: Unilist instacnce.
    :rtype: Unilist
    """
    # supply_demand_data = load_test_data()
    uri = 'tmp://test_data/colors.txt'
    return Unilist(uri)
