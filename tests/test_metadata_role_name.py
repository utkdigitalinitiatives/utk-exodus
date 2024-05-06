import pytest
from utk_exodus.metadata import RoleAndNameProperty
from pathlib import Path

# Set path to fixtures
fixtures_path = Path(__file__).parent / "fixtures"

# Set namespaces
NAMESPACES = {'mods': 'http://www.loc.gov/mods/v3', 'xlink': 'http://www.w3.org/1999/xlink'}

# List fixtures to test with expected results -- Cover supplied, not supplied, and supplied plus not supplied
@pytest.fixture(
    params=[
        {
            "filename": "harp_1.xml",
            "expected_results": {
                'utk_composer': ['Swan, W. H. (William H.)', 'Swan, Marcus Lafayette'], 
                'utk_compiler': ['Swan, W. H. (William H.)', 'Swan, Marcus Lafayette']
            }
        },
        {
            "filename": "volvoices_2495.xml",
            "expected_results": {
                'utk_photographer': ['unknown'],
                'utk_associated_name': ['Bemis Bro. Bag Company']
            }
        },
        {
            "filename": "egypt_224.xml",
            "expected_results": {
                'utk_photographer': ['Brugsch-Bey, Emil, 1842-']
            }
        }
    ]
)
def title_fixture(request):
    param = request.param
    param["fixture_path"] = fixtures_path / param.get('filename')
    return param

def test_find_method_on_title_fixture(title_fixture):
    roleNames = RoleAndNameProperty(title_fixture.get('fixture_path'))
    results = roleNames.find()
    assert results == title_fixture['expected_results']
