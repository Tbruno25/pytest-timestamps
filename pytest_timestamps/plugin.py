from datetime import datetime

import pytest
from _pytest.terminal import TerminalReporter


def format_timestamp(ts):
    return datetime.fromtimestamp(ts).strftime("%H:%M:%S")


class Timestamped(TerminalReporter):
    color = "blue"

    def __init__(self, reporter):
        TerminalReporter.__init__(self, reporter.config)

    @staticmethod
    def _get_timestamps(report):
        return [format_timestamp(ts) for ts in report.timestamps]

    @property
    def timestamps_test(self):
        "Return test start -> test stop"
        return tuple(self.timestamps[1:3])

    @property
    def timestamps_total(self):
        "Return setup start -> teardown stop"
        return tuple(self.timestamps[0:4:3])

    def _write_ts_to_terminal(self):
        start, stop = self.timestamps_test
        ts_line = f"[{start} - {stop}]"
        w = self._width_of_current_line
        fill = self._tw.fullwidth - w - 10
        self.write(ts_line.rjust(fill), **{self.color: True})

    def _write_progress_information_filling_space(self):
        if self.verbosity > 0:
            self._write_ts_to_terminal()
        super()._write_progress_information_filling_space()

    def pytest_runtest_logreport(self, report):
        self.timestamps = self._get_timestamps(report)
        super().pytest_runtest_logreport(report)


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    if config.pluginmanager.has_plugin("terminalreporter"):
        reporter = config.pluginmanager.get_plugin("terminalreporter")
        config.pluginmanager.unregister(reporter, "terminalreporter")
        config.pluginmanager.register(Timestamped(reporter), "terminalreporter")
    if config.pluginmanager.has_plugin("html"):
        global html
        from py.xml import html


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Record timestamps to the test report."""
    output = yield

    if call.when == "setup":
        item._timestamps = [call.start]

    elif call.when == "call":
        item._timestamps.append(call.start)
        item._timestamps.append(call.stop)

    else:
        item._timestamps.append(call.stop)

    report = output.get_result()
    report.timestamps = tuple(item._timestamps)


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th("Setup Start"))
    cells.insert(3, html.th("Test Start"))
    cells.insert(4, html.th("Test Stop"))
    cells.insert(5, html.th("Teardown Stop"))


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    if len(report.timestamps) == 4:
        for idx, ts in enumerate(report.timestamps):
            cells.insert(idx + 2, html.td(format_timestamp(ts)))
