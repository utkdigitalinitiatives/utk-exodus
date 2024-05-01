import pytest
from utk_exodus.metadata import GeoNamesProperty
from pathlib import Path

fixtures_path = Path(__file__).parent / "fixtures"

NAMESPACES = {
    'mods': 'http://www.loc.gov/mods/v3', 
    'xlink': 'http://www.w3.org/1999/xlink'
}

@pytest.fixture(
    params=[
        {"filename": "webster_1127.xml", 
         "expected_results": {
             'spatial': ['http://sws.geonames.org/4050810', 'http://sws.geonames.org/4609260', 'http://id.loc.gov/authorities/subjects/sh85057008']
            } 
        }
    ]
)
def fixture(request):
    request.param["fixtures_path"] = fixtures_path / request.param.get("filename")
    return request.param

def test_find_method_on_geonames(fixture):
    geoname = GeoNamesProperty(fixture.get("fixtures_path"), NAMESPACES)
    results = geoname.find("spatial")
    assert results == fixture["expected_results"]
