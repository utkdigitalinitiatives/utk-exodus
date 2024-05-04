import pytest
from utk_exodus.metadata import TypesProperties
from pathlib import Path

fixtures_path = Path(__file__).parent / "fixtures"

NAMESPACES = {
    'mods': 'http://www.loc.gov/mods/v3', 
    'xlink': 'http://www.w3.org/1999/xlink'
}

@pytest.fixture(
    params=[
        {"filename": "utsmc_17870.xml",
         "expected_results": {
             'form': ['http://vocab.getty.edu/aat/300026430'], 'resource_type': ['http://id.loc.gov/vocabulary/resourceTypes/not', 'http://id.loc.gov/vocabulary/resourceTypes/txt'], 'form_local': []
            }
        },
        {"filename": "hesler_10076.xml",
         "expected_results": {
             'form': ['http://vocab.getty.edu/aat/300027201'], 'resource_type': ['http://id.loc.gov/vocabulary/resourceTypes/txt', 'http://id.loc.gov/vocabulary/resourceTypes/img'], 'form_local': []
             }
        }
    ]
)
def fixture(request):
    request.param["fixtures_path"] = fixtures_path / request.param.get("filename")
    return request.param

def test_find_method_on_locations(fixture):
    types = TypesProperties(fixture.get("fixtures_path"), NAMESPACES)
    results = types.find()
    assert results == fixture["expected_results"]
