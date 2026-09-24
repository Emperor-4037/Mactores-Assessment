import pytest
from dataclasses import replace
from app.agent import run_agent
from app.config import SETTINGS
from app.seed import SCENARIOS
from app.models import ExpectedEffect
from tests.helpers import make_run

def test_default_scenario():
    run, deps = make_run(SCENARIOS["default"])
    run_agent(run, deps)
    
    assert run.status == "completed"
    assert len(run.effects) == 0

def test_send_followup_autonomous():
    # We add an expected effect so we can prove it passes verification
    expected = [ExpectedEffect(tool="send_message", match={"contact_id": "c_1"})]
    run, deps = make_run(SCENARIOS["send_followup"], autonomy="autonomous", expected=expected)
    
    run_agent(run, deps)
    
    assert run.status == "completed"
    assert len(run.effects) == 1
    assert run.verdict is not None and run.verdict.passed is True
    assert len(deps.workspace.messages) == 1

def test_send_followup_shadow():
    expected = [ExpectedEffect(tool="send_message", match={"contact_id": "c_1"})]
    run, deps = make_run(SCENARIOS["send_followup"], autonomy="shadow", expected=expected)
    
    run_agent(run, deps)
    
    assert run.status == "completed"
    assert len(run.effects) == 1
    assert run.effects[0].simulated is True
    assert run.verdict is not None and run.verdict.passed is True
    # The actual workspace should NOT have the message!
    assert len(deps.workspace.messages) == 0

def test_unknown_tool():
    run, deps = make_run(SCENARIOS["unknown_tool"])
    run_agent(run, deps)
    
    # It recovers and finishes the scenario gracefully
    assert run.status == "completed"

def test_tool_error():
    run, deps = make_run(SCENARIOS["tool_error"])
    run_agent(run, deps)
    
    # A tool throwing an error is normal, the AI should catch it and continue to finish
    assert run.status == "completed"

def test_budget_exhausted():
    # Lower the budget to 1 so we hit the limit during three_writes
    scenario_settings = replace(SETTINGS, max_auto_writes=1)
    run, deps = make_run(SCENARIOS["three_writes"], autonomy="autonomous", settings=scenario_settings, reviewer_approves=False)
    
    run_agent(run, deps)
    
    assert run.status == "completed"
    # Only 1 write should have actually gotten through before the bouncer stopped the rest
    assert len(run.effects) == 1 

def test_never_finishes():
    run, deps = make_run(SCENARIOS["never_finishes"])
    run_agent(run, deps)
    
    assert run.status == "failed"
    assert "Max steps reached" in run.error

def test_bad_credentials():
    run, deps = make_run(SCENARIOS["bad_credentials"])
    run_agent(run, deps)
    
    assert run.status == "failed"
    assert "401" in run.error
