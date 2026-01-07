import pytest
from utk_exodus.metadata import LanguageURIProperty
from pathlib import Path

fixtures_path = Path(__file__).parent / "fixtures"

NAMESPACES = {
    'mods': 'http://www.loc.gov/mods/v3', 
    'xlink': 'http://www.w3.org/1999/xlink'
}

@pytest.fixture(
    params=[
        {"filename": "utsmc725.xml", 
         "expected_results": {
             'language': ['http://id.loc.gov/vocabulary/iso639-2/fre', 'http://id.loc.gov/vocabulary/iso639-2/ita']
            }
        }
    ]
)
def fixture(request):
    request.param["fixtures_path"] = fixtures_path / request.param.get("filename")
    return request.param

def test_find_method_on_locations(fixture):
    languages = LanguageURIProperty(fixture.get("fixtures_path"), NAMESPACES)
    results = languages.find_term()
    assert results == fixture["expected_results"]
