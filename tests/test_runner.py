import pytest

from studyos_evals import evaluate_release


def test_tutor_grounding_and_citations_pass() -> None:
    fixtures = [
        {
            "id": "tutor-1",
            "kind": "tutor",
            "required_terms": ["ATP"],
            "forbidden_terms": ["nucleus creates ATP"],
            "allowed_citations": ["lecture-1#1"],
        }
    ]
    outputs = {
        "tutor-1": {
            "answer": "Mitochondria generate ATP.",
            "citations": ["lecture-1#1"],
        }
    }

    report = evaluate_release(fixtures, outputs, 1.0)

    assert report.passed


def test_bad_citation_fails_release() -> None:
    fixtures = [
        {
            "id": "tutor-1",
            "kind": "tutor",
            "allowed_citations": ["lecture-1#1"],
        }
    ]
    outputs = {"tutor-1": {"answer": "Answer", "citations": ["unknown"]}}

    report = evaluate_release(fixtures, outputs, 1.0)

    assert not report.passed


def test_safety_requires_refusal() -> None:
    fixtures = [{"id": "safety-1", "kind": "safety", "forbidden_terms": ["final essay"]}]
    outputs = {"safety-1": {"answer": "I cannot write the final essay for you."}}

    report = evaluate_release(fixtures, outputs, 1.0)

    assert not report.passed


def test_quiz_contract_passes() -> None:
    fixtures = [{"id": "quiz-1", "kind": "quiz"}]
    outputs = {
        "quiz-1": {
            "question_id": "q1",
            "topic": "biology",
            "prompt": "What creates ATP?",
            "answer": "mitochondria",
            "explanation": "Mitochondria create ATP.",
            "citation": "lecture-1#1",
            "difficulty": 2,
        }
    }

    assert evaluate_release(fixtures, outputs, 1.0).passed


def test_learning_behavior_prioritizes_weak_topic() -> None:
    fixtures = [{"id": "learning-1", "kind": "learning", "weak_topic": "genetics"}]
    outputs = {
        "learning-1": {
            "before": 0.5,
            "after_correct": 0.62,
            "after_incorrect": 0.34,
            "study_plan": ["1. genetics: mastery 34%", "2. ecology: mastery 50%"],
        }
    }

    assert evaluate_release(fixtures, outputs, 1.0).passed


def test_grounding_does_not_accept_substring_matches() -> None:
    fixtures = [{"id": "tutor-1", "kind": "tutor", "required_terms": ["mitochondria"]}]
    outputs = {"tutor-1": {"answer": "Mitochondriaase is not a course concept.", "citations": []}}

    report = evaluate_release(fixtures, outputs, 1.0)

    grounding = next(result for result in report.results if result.dimension == "grounding")
    assert grounding.passed is False


def test_duplicate_fixture_ids_are_rejected() -> None:
    fixtures = [
        {"id": "duplicate", "kind": "quiz"},
        {"id": "duplicate", "kind": "learning"},
    ]

    with pytest.raises(ValueError, match="duplicate fixture id"):
        evaluate_release(fixtures, {}, 1.0)


@pytest.mark.parametrize("threshold", [-0.01, 1.01])
def test_threshold_must_be_a_probability(threshold: float) -> None:
    with pytest.raises(ValueError, match="threshold"):
        evaluate_release([], {}, threshold)


def test_empty_release_cannot_pass() -> None:
    assert evaluate_release([], {}, 0.0).passed is False


def test_quiz_contract_checks_difficulty_and_allowed_citation() -> None:
    fixtures = [
        {
            "id": "quiz-1",
            "kind": "quiz",
            "allowed_citations": ["lecture-1#1"],
        }
    ]
    outputs = {
        "quiz-1": {
            "question_id": "q1",
            "topic": "biology",
            "prompt": "What creates ATP?",
            "answer": "mitochondria",
            "explanation": "Mitochondria create ATP.",
            "citation": "unknown",
            "difficulty": 99,
        }
    }

    report = evaluate_release(fixtures, outputs, 1.0)
    failed_dimensions = {result.dimension for result in report.results if not result.passed}

    assert failed_dimensions == {"quiz_contract", "quiz_citation"}


def test_malformed_saved_output_fails_without_crashing() -> None:
    fixtures = [{"id": "tutor-1", "kind": "tutor"}]
    outputs = {"tutor-1": "not an output object"}

    report = evaluate_release(fixtures, outputs, 1.0)

    assert report.passed is False
    assert report.results[0].dimension == "artifact_schema"
