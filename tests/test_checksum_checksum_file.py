import pytest
from utk_exodus.checksum import HashSheet
from pathlib import Path

# Set path to fixtures
fixtures_path = Path(__file__).parent / "fixtures"

@pytest.fixture(
    params=[
        {
            "filename": "bad_imports",
            "expected_results": {
                'url': 'https://raw.githubusercontent.com/utkdigitalinitiatives/utk-exodus/main/tests/fixtures/colloquy_202.xml',
                'checksum': '081a51fae0200f266d2933756d48441c4ea77b1e'
            }
        },
    ]
)
def fixture(request):
    request.param["fixtures_path"] = fixtures_path / request.param.get("filename")
    return request.param

def test_checksum_file(fixture):
    hs = HashSheet(fixture.get("fixtures_path"), "example.csv")
    results = hs.checksum_file(
        "https://raw.githubusercontent.com/utkdigitalinitiatives/utk-exodus/main/tests/fixtures/colloquy_202.xml"
    )
    assert results == fixture["expected_results"]
