# StudyOS Evals

A small deterministic release gate for saved StudyOS artifacts. It checks
lexical grounding fixtures, citation allowlists, refusal markers, quiz
contracts, and expected mastery or study-plan direction.

The harness does not call a live model. That keeps runs reproducible and makes
the release decision independent from provider availability.

## What this is not

This is not a general-purpose model evaluator, a semantic factuality judge, a
safety certification, or evidence that a tutoring workflow improves learning.
Its checks are explicit fixture contracts over saved JSON artifacts. Human and
educator review remain outside this repository.

## Run the sample release gate

```bash
python3 -m pip install -e ".[dev]"
python3 -m studyos_evals \
  --fixtures examples/fixtures.json \
  --outputs examples/outputs.json \
  --threshold 0.8
```

## Tests

```bash
python3 -m pytest
python3 -m compileall -q src
```

The suite covers threshold validation, duplicate fixture IDs, malformed
artifacts, token-boundary matching, citations, refusal markers, quiz contracts,
mastery direction, and study-plan priority.

See [docs/PRD.md](docs/PRD.md) for the deliberately narrow evaluation strategy.
