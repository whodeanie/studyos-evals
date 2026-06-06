# StudyOS Evals

Independent release gates for citation-first tutoring, quiz contracts, safety,
and adaptive-learning behavior.

The harness evaluates saved StudyOS artifacts. It does not call a live model,
which makes failures reproducible and keeps the release decision independent
from provider availability.

## Run the sample release gate

```bash
PYTHONPATH=src python3 -m studyos_evals \
  --fixtures examples/fixtures.json \
  --outputs examples/outputs.json \
  --threshold 0.8
```

## Tests

```bash
python3 -m pytest
```

See [docs/PRD.md](docs/PRD.md) for evaluation strategy and architecture.

