from _pytest.config import Config
from _pytest.reports import TestReport
from _pytest.terminal import TerminalReporter

from pytest_timestamps.timestamp import timestamp

TEXT_COLOR = "blue"
LINE_DEDENT = 10


class TimestampReporter(TerminalReporter):  # type: ignore
    def __init__(self, config: Config) -> None:
        TerminalReporter.__init__(self, config)

    def _write_timestamp(self) -> None:
        line_width = self._width_of_current_line
        total_width = self._tw.fullwidth
        fill = total_width - line_width - LINE_DEDENT
        data = timestamp.get().rjust(fill)
        self.write(data, **{TEXT_COLOR: True})

    def _write_progress_information_filling_space(self) -> None:
        if timestamp.is_valid():
            self._write_timestamp()
        super()._write_progress_information_filling_space()
        timestamp.clear()

    def pytest_runtest_logreport(self, report: TestReport) -> None:
        timestamp.update(report)
        super().pytest_runtest_logreport(report)
