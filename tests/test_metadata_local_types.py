import pytest
from utk_exodus.metadata import LocalTypesProperties
from pathlib import Path

fixtures_path = Path(__file__).parent / "fixtures"

NAMESPACES = {
    'mods': 'http://www.loc.gov/mods/v3', 
    'xlink': 'http://www.w3.org/1999/xlink'
}

@pytest.fixture(
    params=[
        {"filename": "swim_162.xml", 
         "expected_results": {
             'resource_type_local': ['text'], 'form_local': ['brochures']
            }
        },
        {"filename": "egypt_224.xml",
         "expected_results": {
             'resource_type_local': ['still image'], 'form_local': ['platinum prints']
             }
        }
    ]
)
def fixture(request):
    request.param["fixtures_path"] = fixtures_path / request.param.get("filename")
    return request.param

def test_find_method_on_locations(fixture):
    localTypes = LocalTypesProperties(fixture.get("fixtures_path"), NAMESPACES)
    results = localTypes.find()
    assert results == fixture["expected_results"]
