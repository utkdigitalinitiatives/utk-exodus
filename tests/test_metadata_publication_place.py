import pytest
from utk_exodus.metadata import PublicationPlaceProperty
from pathlib import Path

fixtures_path = Path(__file__).parent / "fixtures"

NAMESPACES = {
    'mods': 'http://www.loc.gov/mods/v3', 
    'xlink': 'http://www.w3.org/1999/xlink'
}

@pytest.fixture(
    params=[
        {"filename": "volvoices_2136.xml", 
         "expected_results": {
             'publication_place': ['http://id.loc.gov/authorities/names/n81024913']
            }
        },
        {"filename": "volvoices_2495.xml",
         "expected_results": {
             'publication_place': ['http://id.loc.gov/authorities/names/n82063401']
            }
        }
    ]
)
def fixture(request):
    request.param["fixtures_path"] = fixtures_path / request.param.get("filename")
    return request.param

def test_find_method_on_locations(fixture):
    publications = PublicationPlaceProperty(fixture.get("fixtures_path"), NAMESPACES)
    results = publications.find()
    assert results == fixture["expected_results"]
