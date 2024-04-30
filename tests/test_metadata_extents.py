import pytest
from utk_exodus.metadata import ExtentProperty
from pathlib import Path

# Set path to fixtures
fixtures_path = Path(__file__).parent / "fixtures"

# Set namespaces
NAMESPACES = {
    "mods": "http://www.loc.gov/mods/v3",
    "xlink": "http://www.w3.org/1999/xlink",
}


# Set Fixtures and Expected Results
@pytest.fixture(
    params=[
        {"filename": "colloquy_202.xml", "expected_results": {"extent": ["4 pages"]}},
        {
            "filename": "knoxgardens_125.xml",
            "expected_results": {"extent": ["3 1/4 x 5 inches"]},
        },
    ]
)
def extent_fixture(request):
    param = request.param
    param["fixture_path"] = fixtures_path / param.get("filename")
    return param


def test_find_method_on_extent(extent_fixture):
    extents = ExtentProperty(extent_fixture.get("fixture_path"), NAMESPACES)
    results = extents.find()
    assert results == extent_fixture["expected_results"]
