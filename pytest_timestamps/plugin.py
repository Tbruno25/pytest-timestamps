from datetime import datetime
from typing import Final, Optional

import pytest
from _pytest.config import Config
from _pytest.reports import TestReport
from _pytest.terminal import TerminalReporter


def format(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")


class Timestamp:
    start: Optional[float] = None
    stop: Optional[float] = None

    def clear(self) -> None:
        self.start = None
        self.stop = None

    def get(self) -> str:
        return f"[{format(self.start)} - {format(self.stop)}]"  # type: ignore

    def is_valid(self) -> bool:
        return bool(self.start and self.stop)

    def update(self, report: TestReport) -> None:
        if report.when == "call":
            if not self.start:
                self.start = report.start
            self.stop = report.stop


class TimestampReporter(TerminalReporter):  # type: ignore
    color: str = "blue"
    dedent: int = 10
    timestamp: Final = Timestamp()

    def __init__(self, config: Config) -> None:
        TerminalReporter.__init__(self, config)

    def _write_timestamp(self) -> None:
        line_width = self._width_of_current_line
        total_width = self._tw.fullwidth
        fill = total_width - line_width - self.dedent
        timestamp = self.timestamp.get().rjust(fill)
        self.write(timestamp, **{self.color: True})

    def _write_progress_information_filling_space(self) -> None:
        if self.timestamp.is_valid():
            self._write_timestamp()
        super()._write_progress_information_filling_space()
        self.timestamp.clear()

    def pytest_runtest_logreport(self, report: TestReport) -> None:
        self.timestamp.update(report)
        super().pytest_runtest_logreport(report)


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    if config.pluginmanager.has_plugin("terminalreporter"):
        reporter = config.pluginmanager.get_plugin("terminalreporter")
        config.pluginmanager.unregister(reporter, "terminalreporter")
        config.pluginmanager.register(TimestampReporter(config), "terminalreporter")
