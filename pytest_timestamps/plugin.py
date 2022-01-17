from datetime import datetime

import pytest
from _pytest.terminal import TerminalReporter


def format_timestamp(ts):
    return datetime.fromtimestamp(ts).strftime("%H:%M:%S")


class Timestamped(TerminalReporter):
    color = "blue"

    def __init__(self, reporter):
        TerminalReporter.__init__(self, reporter.config)
        self._node = None
        self._fspath = None
        self._last_fspath = None

    def _get_timestamps(self):
        if self.verbosity > 0:
            times = self._node
        else:
            times = self._fspath
        return [format_timestamp(i) for i in times]

    def _write_ts_to_terminal(self):
        start, stop = self._get_timestamps()
        ts_line = f"[{start} - {stop}]"
        w = self._width_of_current_line
        fill = self._tw.fullwidth - w - 10
        self.write(ts_line.rjust(fill), **{self.color: True})

    def _write_progress_information_filling_space(self):
        self._write_ts_to_terminal()
        super()._write_progress_information_filling_space()

    def pytest_runtest_logreport(self, report):
        if len(report.timestamps) == 3:
            if report.fspath != self._last_fspath:
                self._last_fspath = report.fspath
                self._fspath = report.timestamps[1:3]
            else:
                self._fspath[1] = report.timestamps[2]
        self._node = report.timestamps[1:3]
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

    if call.when == "setup":
        item._timestamps = [call.start]

    elif call.when == "call":
        item._timestamps.append(call.start)
        item._timestamps.append(call.stop)

    else:
        item._timestamps.append(call.stop)

    output = yield
    report = output.get_result()
    report.timestamps = item._timestamps


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
