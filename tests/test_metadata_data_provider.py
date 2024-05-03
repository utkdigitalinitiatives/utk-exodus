import pytest
from utk_exodus.metadata import DataProvider
from pathlib import Path

fixtures_path = Path(__file__).parent / "fixtures"

NAMESPACES = {
    'mods': 'http://www.loc.gov/mods/v3', 
    'xlink': 'http://www.w3.org/1999/xlink'
}

@pytest.fixture(
    params=[
        {"filename": "egypt_224.xml",
         "expected_results": {
             'provider': ['University of Tennessee, Knoxville. Libraries'], 'intermediate_provider': ['Frank H. McClung Museum of Natural History and Culture']
            } 
        }
    ]
)
def fixture(request):
    request.param["fixtures_path"] = fixtures_path / request.param.get("filename")
    return request.param

def test_find_method_on_data_provider(fixture):
    dataProvider = DataProvider(fixture.get("fixtures_path"), NAMESPACES)
    results = dataProvider.find()
    assert results == fixture["expected_results"]
