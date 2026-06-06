from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .runner import evaluate_release


def main() -> int:
    parser = argparse.ArgumentParser(description="Run StudyOS release evaluations.")
    parser.add_argument("--fixtures", required=True)
    parser.add_argument("--outputs", required=True)
    parser.add_argument("--threshold", type=float, default=0.8)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    fixtures = json.loads(Path(args.fixtures).read_text(encoding="utf-8"))
    outputs = json.loads(Path(args.outputs).read_text(encoding="utf-8"))
    report = evaluate_release(fixtures, outputs, args.threshold)

    if args.json:
        print(json.dumps(asdict(report), indent=2))
    else:
        print(f"Release gate: {'PASS' if report.passed else 'FAIL'} ({report.pass_rate:.1%})")
        for result in report.results:
            status = "PASS" if result.passed else "FAIL"
            print(f"{status} {result.fixture_id} / {result.dimension}: {result.detail}")
    return 0 if report.passed else 1

