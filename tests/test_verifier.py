import pytest
from app.verifier import verify
from app.models import Task, Run, ExpectedEffect, Effect

def test_verify_passed():
    # 1. Arrange: We expect an email to c_1. The agent sent an email to c_1.
    task = Task(
        id="t_1", goal="say hi", 
        expected_effects=[ExpectedEffect(tool="send_message", match={"contact_id": "c_1"})]
    )
    run = Run(
        id="r_1", task_id="t_1", autonomy="autonomous", 
        effects=[Effect(tool="send_message", args={"contact_id": "c_1", "body": "hi!"})]
    )

    # 2. Act
    verdict = verify(task, run)

    assert verdict.passed == True
    assert len(verdict.missing) == 0
    assert len(verdict.unexpected) == 0

def test_verify_missing():
    # 1. Arrange: We expect an email to c_1. The agent did NOTHING (empty list).
    task = Task(
        id="t_1", goal="say hi", 
        expected_effects=[ExpectedEffect(tool="send_message", match={"contact_id": "c_1"})]
    )
    run = Run(
        id="r_1", task_id="t_1", autonomy="autonomous", 
        effects=[] 
    )

    # 2. Act
    verdict = verify(task, run)

    assert verdict.passed == False
    assert len(verdict.missing) == 1
    assert len(verdict.unexpected) == 0


def test_verify_unexpected():
    # 1. Arrange: We expect NOTHING (empty list). The agent sent an email to c_2.
    task = Task(
        id="t_1", goal="do nothing", 
        expected_effects=[] 
    )
    run = Run(
        id="r_1", task_id="t_1", autonomy="autonomous", 
        effects=[Effect(tool="send_message", args={"contact_id": "c_2", "body": "whoops"})]
    )

    # 2. Act
    verdict = verify(task, run)

    assert verdict.passed == False
    assert len(verdict.missing) == 0
    assert len(verdict.unexpected) == 1