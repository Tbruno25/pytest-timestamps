import pytest

from pytest_timestamps.reporter import TimestampReporter


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    if config.pluginmanager.has_plugin("terminalreporter"):
        reporter = config.pluginmanager.get_plugin("terminalreporter")
        config.pluginmanager.unregister(reporter, "terminalreporter")
        config.pluginmanager.register(TimestampReporter(config), "terminalreporter")
