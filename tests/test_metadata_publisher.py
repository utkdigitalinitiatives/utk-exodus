import pytest
from utk_exodus.metadata import PublisherProperty
from pathlib import Path

fixtures_path = Path(__file__).parent / "fixtures"

NAMESPACES = {
    'mods': 'http://www.loc.gov/mods/v3', 
    'xlink': 'http://www.w3.org/1999/xlink'
}

@pytest.fixture(
    params=[
        {"filename": "playbills1052.xml", 
         "expected_results": {
             'publisher': []
            }
        }
    ]
)
def fixture(request):
    request.param["fixtures_path"] = fixtures_path / request.param.get("filename")
    return request.param

def test_find_method_on_locations(fixture):
    publishers = PublisherProperty(fixture.get("fixtures_path"), NAMESPACES)
    results = publishers.find()
    assert results == fixture["expected_results"]
