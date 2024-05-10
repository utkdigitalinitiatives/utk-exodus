import pytest
from utk_exodus.restrict import Restrictions
from pathlib import Path

# Set path to fixtures
fixtures_path = Path(__file__).parent / "fixtures"

@pytest.fixture(
    params=[
        {
            "filename": "bass_10900_POLICY.xml",
            "expected_results": {
                "work_restricted": True,
                "restricted_datastreams": [],
            }
        },
        {
            "filename": "voloh_10_POLICY.xml",
            "expected_results": {
                "work_restricted": False,
                "restricted_datastreams": ['DEED_OF_GIFT', 'CONSENT_FORM'],
            }
        },
        {
            "filename": "rfta_8_POLICY.xml",
            "expected_results": {
                "work_restricted": False,
                "restricted_datastreams": [],
            }
        }
    ]
)
def fixture(request):
    request.param["fixtures_path"] = fixtures_path / request.param.get("filename")
    return request.param

def test_find_restricted_datastreams(fixture):
    restrictions = Restrictions(fixture.get("fixtures_path"))
    results = restrictions.get()
    assert results == fixture["expected_results"]