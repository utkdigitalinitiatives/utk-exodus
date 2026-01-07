import pytest
from utk_exodus.metadata import RightsOrLicenseProperties
from pathlib import Path

fixtures_path = Path(__file__).parent / "fixtures"

NAMESPACES = {
    'mods': 'http://www.loc.gov/mods/v3', 
    'xlink': 'http://www.w3.org/1999/xlink'
}

@pytest.fixture(
    params=[
        {"filename": "heilman1010.xml",
         "expected_results": {
            'license': ['http://creativecommons.org/licenses/by-nc-nd/3.0/'], 'rights_statement': ['http://rightsstatements.org/vocab/InC/1.0/']
            }
        },
        {"filename": "civilwar_1438.xml",
         "expected_results": {
            'rights_statement': ['http://rightsstatements.org/vocab/NoC-US/1.0/']
            }
        },
        {"filename": "covid_1.xml",
         "expected_results": {
            'rights_statement': ['http://rightsstatements.org/vocab/CNE/1.0/']
            }
        }
    ]
)
def fixture(request):
    request.param["fixtures_path"] = fixtures_path / request.param.get("filename")
    return request.param

def test_find_method_on_locations(fixture):
    rights = RightsOrLicenseProperties(fixture.get("fixtures_path"), NAMESPACES)
    results = rights.find()
    assert results == fixture["expected_results"]
