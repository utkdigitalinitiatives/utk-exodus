import pytest
from utk_exodus.restrict import Restrictions
from pathlib import Path

# Set path to fixtures
fixtures_path = Path(__file__).parent / "fixtures"

@pytest.fixture(
    params=[
        {
            "filename": "bass_10900_POLICY.xml",
            "expected_results": True
        },
        {
            "filename": "voloh_10_POLICY.xml",
            "expected_results": False
        },
        {
            "filename": "rfta_8_POLICY.xml",
            "expected_results": False
        }
    ]
)
def fixture(request):
    request.param["fixtures_path"] = fixtures_path / request.param.get("filename")
    return request.param

def test_find_restricted_datastreams(fixture):
    restrictions = Restrictions(fixture.get("fixtures_path"))
    results = restrictions.determine_if_work_restricted()
    assert results == fixture["expected_results"]