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

