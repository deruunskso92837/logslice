#!/usr/bin/env python3
"""logslice - Parse and filter log files with pattern matching."""
import re
import sys
import json
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class LogEntry:
    line_number: int
    timestamp: Optional[str]
    level: Optional[str]
    message: str

    def to_dict(self):
        return asdict(self)

LOG_PATTERN = re.compile(
    r"(?P<ts>\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[.\d]*\S*)\s+"
    r"(?P<level>DEBUG|INFO|WARN(?:ING)?|ERROR|FATAL|CRITICAL)\s+"
    r"(?P<msg>.*)"
)

def parse_line(lineno: int, line: str) -> LogEntry:
    m = LOG_PATTERN.match(line.strip())
    if m:
        return LogEntry(lineno, m.group("ts"), m.group("level"), m.group("msg"))
    return LogEntry(lineno, None, None, line.strip())

def slice_logs(filepath: str, level: str = None, pattern: str = None, limit: int = 0):
    entries = []
    with open(filepath) as f:
        for lineno, line in enumerate(f, 1):
            entry = parse_line(lineno, line)
            if level and entry.level and entry.level.upper() != level.upper():
                continue
            if pattern and not re.search(pattern, entry.message, re.IGNORECASE):
                continue
            entries.append(entry)
            if limit and len(entries) >= limit:
                break
    return entries

def main():
    import argparse
    p = argparse.ArgumentParser(description="Parse and filter log files")
    p.add_argument("file")
    p.add_argument("-l", "--level", help="Filter by log level")
    p.add_argument("-p", "--pattern", help="Regex pattern to match")
    p.add_argument("-n", "--limit", type=int, default=0)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    entries = slice_logs(args.file, args.level, args.pattern, args.limit)
    if args.json:
        print(json.dumps([e.to_dict() for e in entries], indent=2))
    else:
        for e in entries:
            ts = e.timestamp or "          "
            lvl = (e.level or "").ljust(8)
            print(f"{ts}  {lvl}  {e.message}")

if __name__ == "__main__":
    main()
