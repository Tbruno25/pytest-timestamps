import pytest
from freezegun import freeze_time

pytest_plugins = "pytester"


@pytest.fixture
def timestamp():
    ts = "01:01:01"
    with freeze_time(f"2000-01-01 {ts}"):
        yield f"[{ts} - {ts}]"


def test_timestamps_normal(pytester, timestamp):
    pytester.makepyfile(
        """
    import pytest
    
    def test_plugin():
        assert True
    """
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
    assert timestamp in result.stdout.str()


def test_timestamps_verbose(pytester, timestamp):
    pytester.makepyfile(
        """
    import pytest
    
    def test_plugin():
        assert True
    """
    )
    result = pytester.runpytest("-v")
    result.assert_outcomes(passed=1)
    assert timestamp in result.stdout.str()
