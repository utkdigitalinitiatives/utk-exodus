import pytest
from utk_exodus.metadata import TitleProperty
from pathlib import Path

# Set path to fixtures
fixtures_path = Path(__file__).parent / "fixtures"

# Set namespaces
NAMESPACES = {'mods': 'http://www.loc.gov/mods/v3', 'xlink': 'http://www.w3.org/1999/xlink'}

# List fixtures to test with expected results
@pytest.fixture(
    params=[
        {
            "filename": "egypt_224.xml",
            "expected_results": {
                'title': ['Bracelets from Abydos, Tomb of Djer'],
                'alternative_title': []
            }
        },
        {
            "filename": "swim_162.xml",
            "expected_results": {
                'title': ['University of Tennessee Volunteers Swimming-Diving media guide, 1969'],
                'alternative_title': ['Swimming 1969: The University of Tennessee ']
            }
        }
    ]
)
def title_fixture(request):
    param = request.param
    param["fixture_path"] = fixtures_path / param.get('filename')
    return param

def test_find_method_on_title_fixture(title_fixture):
    titles = TitleProperty(title_fixture.get('fixture_path'), NAMESPACES)
    results = titles.find()
    assert results == title_fixture['expected_results']
