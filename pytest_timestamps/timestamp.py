from datetime import datetime
from typing import Optional

from _pytest.reports import TestReport


def format(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")


class _Timestamp:
    start: Optional[float] = None
    stop: Optional[float] = None

    def clear(self) -> None:
        self.start = None
        self.stop = None

    @staticmethod
    def _format(timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")

    def get(self) -> str:
        return f"[{format(self.start)} - {format(self.stop)}]"  # type: ignore

    def is_valid(self) -> bool:
        return bool(self.start and self.stop)

    def update(self, report: TestReport) -> None:
        if report.when == "call":
            if not self.start:
                self.start = report.start
            self.stop = report.stop


timestamp = _Timestamp()
