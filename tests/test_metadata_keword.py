import pytest
from utk_exodus.metadata import KeywordProperty
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
            "filename": "civilwar_1438.xml",
            "expected_results": {
                'keyword': [
                    'Jurisdiction -- Tennessee, East -- History -- Civil War, 1861-1865',
                    'Actions and defenses -- Tennessee, East -- History -- Civil War, 1861-1865',
                    'Tennessee, East -- Politics and government -- 19th century',
                    'Wallace, Jesse G. -- Correspondence',
                    'Temple, Oliver Perry, 1820-1907 -- Correspondence'
                ]
            }
        },
    ]
)
def fixture(request):
    param = request.param
    param["fixture_path"] = fixtures_path / param.get("filename")
    return param


def test_find_method_on_keyword(fixture):
    subjects = KeywordProperty(fixture.get("fixture_path"), NAMESPACES)
    results = subjects.find_topic()
    assert results == fixture["expected_results"]
