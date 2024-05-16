import pytest
from utk_exodus.metadata import SubjectProperty
from pathlib import Path

# Set path to fixtures
fixtures_path = Path(__file__).parent / "fixtures"

# Set namespaces
NAMESPACES = {
    "mods": "http://www.loc.gov/mods/v3",
    "xlink": "http://www.w3.org/1999/xlink",
}


@pytest.fixture(
    params=[
        {
            "filename": "cdf_13238.xml",
            "expected_results": {
                "subject": [
                    "http://id.loc.gov/authorities/subjects/sh85023396",
                    "http://id.loc.gov/authorities/subjects/sh87000100",
                    "http://id.loc.gov/authorities/names/n79059917",
                ]
            },
        },
        {
            "filename": "egypt_224.xml",
            "expected_results": {
                "subject": ["http://id.loc.gov/authorities/subjects/sh85016233"]
            },
        },
        {
            "filename": "knoxgardens_125.xml",
            "expected_results": {
                "subject": [
                    "http://id.loc.gov/authorities/subjects/sh85101348",
                    "http://id.loc.gov/authorities/subjects/sh85053123",
                    "http://id.loc.gov/authorities/subjects/sh85103022",
                    "http://id.loc.gov/authorities/subjects/sh2008120720",
                ]
            },
        },
    ]
)
def fixture(request):
    param = request.param
    param["fixture_path"] = fixtures_path / param.get("filename")
    return param


def test_find_method_on_subject(fixture):
    subjects = SubjectProperty(fixture.get("fixture_path"), NAMESPACES)
    results = subjects.find_topic()
    assert results == fixture["expected_results"]
