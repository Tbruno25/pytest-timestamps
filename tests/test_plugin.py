from unittest.mock import patch

import pytest

from pytest_timestamps.timestamp import timestamp as ts

pytest_plugins = "pytester"


@pytest.fixture
def timestamp():
    # Prevent times from being cleared once printed to terminal
    with patch.object(ts, "clear"):
        yield ts

    ts.clear()


def test_timestamps_normal(pytester, timestamp):
    pytester.makepyfile(
        """
    import pytest

    def test_plugin():
        assert True
    """
    )
    result = pytester.runpytest()
    assert timestamp.is_valid()
    result.assert_outcomes(passed=1)
    assert timestamp.get() in result.stdout.str()


def test_timestamps_verbose(pytester, timestamp):
    pytester.makepyfile(
        """
    import pytest

    def test_plugin():
        assert True
    """
    )
    result = pytester.runpytest("-v")
    assert timestamp.is_valid()
    result.assert_outcomes(passed=1)
    assert timestamp.get() in result.stdout.str()


def test_timestamp_is_cleared(pytester, timestamp):
    pytester.makepyfile(
        """
    import pytest

    def test_plugin():
        assert True
    """
    )
    pytester.runpytest()
    timestamp.clear.assert_called_once()


def test_timestamps_with_skip_decorator(pytester):
    pytester.makepyfile(
        """
    import pytest

    @pytest.mark.skip
    def test_plugin():
        assert True
    """
    )
    result = pytester.runpytest()
    result.assert_outcomes(skipped=1)


def test_timestamp_is_accurate(pytester, timestamp):
    time_delta = 60

    pytester.makepyfile(
        f"""
        from freezegun import freeze_time
        import pytest

        @pytest.fixture
        def time():
            with freeze_time() as frozen_time:
                yield frozen_time

        def test_plugin(time):
            time.tick({time_delta})
            assert True
        """
    )
    pytester.runpytest()
    test_duration = timestamp.stop - timestamp.start
    assert test_duration - time_delta < 1
