import pytest
from utk_exodus.metadata import PhysicalLocationsProperties
from pathlib import Path

fixtures_path = Path(__file__).parent / "fixtures"

NAMESPACES = {
    'mods': 'http://www.loc.gov/mods/v3', 
    'xlink': 'http://www.w3.org/1999/xlink'
}

@pytest.fixture(
    params=[
        {"filename": "volvoices_2495.xml", 
         "expected_results": {
            'repository': ['Union University (Jackson, Tenn.)'], 'archival_collection': ['Bemis Collection']
            }
        },
        {"filename": "civilwar_1438.xml",
         "expected_results": {
             'repository': ['University of Tennessee, Knoxville. Special Collections'], 'archival_collection': ['O. P. Temple Papers,1862']
             }
        },
        {"filename": "egypt_224.xml",
         "expected_results": {
             'repository': ['Frank H. McClung Museum of Natural History and Culture'], 'archival_collection': []
             }
        },
        {"filename": "volvoices_2136.xml",
         "expected_results": {
             'repository': ['Cleveland State Community College'], 'archival_collection': ['Cleveland Public Library History Branch Collection']
             }
        }
    ]
)
def fixture(request):
    request.param["fixtures_path"] = fixtures_path / request.param.get("filename")
    return request.param

def test_find_method_on_locations(fixture):
    locations = PhysicalLocationsProperties(fixture.get("fixtures_path"), NAMESPACES)
    results = locations.find()
    assert results == fixture["expected_results"]
