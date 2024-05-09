import pytest
from utk_exodus.restrict import Restrictions
from pathlib import Path

# Set path to fixtures
fixtures_path = Path(__file__).parent / "fixtures"

@pytest.fixture(
    params=[
        {
            "filename": "bass_10900_POLICY.xml",
            "expected_results": []
        },
        {
            "filename": "voloh_10_POLICY.xml",
            "expected_results": ['DEED_OF_GIFT', 'CONSENT_FORM']
        },
        {
            "filename": "rfta_8_POLICY.xml",
            "expected_results": []
        }
    ]
)
def fixture(request):
    request.param["fixtures_path"] = fixtures_path / request.param.get("filename")
    return request.param

def test_find_restricted_datastreams(fixture):
    restrictions = Restrictions(fixture.get("fixtures_path"))
    results = restrictions.find_restricted_datastreams()
    assert results == fixture["expected_results"]