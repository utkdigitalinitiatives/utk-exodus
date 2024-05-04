import pytest
from utk_exodus.metadata import MachineDate
from pathlib import Path

fixtures_path = Path(__file__).parent / "fixtures"

NAMESPACES = {
    'mods': 'http://www.loc.gov/mods/v3', 
    'xlink': 'http://www.w3.org/1999/xlink'
}

@pytest.fixture(
    params=[
        {"filename": "volvoices_2993.xml", 
         "expected_results": {
            'date_created_d': ['1948-01'], 'date_issued_d': ['1948'], 'date_other_d': []
            }
        },
        {"filename": "webster_1127.xml",
         "expected_results": {
             'date_created_d': ['1926/1955'], 'date_issued_d': [], 'date_other_d': []
             }
        },
        {"filename": "volvoices_2495.xml",
         "expected_results": {
             'date_created_d': ['1941/1945'], 'date_issued_d': [], 'date_other_d': []
             }
        }
    ]
)
def fixture(request):
    request.param["fixtures_path"] = fixtures_path / request.param.get("filename")
    return request.param

def test_find_method_on_locations(fixture):
    machineDate = MachineDate(fixture.get("fixtures_path"), NAMESPACES)
    results = machineDate.find()
    assert results == fixture["expected_results"]
