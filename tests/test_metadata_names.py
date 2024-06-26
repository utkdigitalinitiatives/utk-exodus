import pytest
from utk_exodus.metadata import NameProperty
from pathlib import Path

# Set path to fixtures
fixtures_path = Path(__file__).parent / "fixtures"


# Set Fixtures and Expected Results
@pytest.fixture(
    params=[
        {
            "filename": "harp_1.xml",
            "expected_results": {
                "composer": [
                    "http://id.loc.gov/authorities/names/no2002022963",
                    "http://id.loc.gov/authorities/names/n78013127",
                ],
                "compiler": [
                    "http://id.loc.gov/authorities/names/no2002022963",
                    "http://id.loc.gov/authorities/names/n78013127",
                ],
            },
        },
        {
            "filename": "volvoices_2495.xml",
            "expected_results": {
                "utk_associated_name": ["Bemis Bro. Bag Company"],
                "utk_photographer": ["unknown"],
            },
        },
        {
            "filename": "ekcd_50.xml",
            "expected_results": {
                'copyright_holder': ['http://id.loc.gov/authorities/names/n79144615'],
                'utk_creator': ['Kefauver, Estes 1903-1963']
            }
        },
        {
            "filename": "cdf_13238.xml",
            "expected_results": {
                'author': [
                    'http://id.loc.gov/authorities/names/n92112591',
                    'http://id.loc.gov/authorities/names/n86833543'
                ],
                'utk_author': [
                    'Poersch, Oxendine'
                ]
            }
        }
    ]
)
def names_fixture(request):
    param = request.param
    param["fixture_path"] = fixtures_path / param.get("filename")
    return param


def test_find_method_on_names(names_fixture):
    names = NameProperty(names_fixture.get("fixture_path"))
    results = names.find()
    assert results == names_fixture["expected_results"]
