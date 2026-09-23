import pytest
from app.autonomy import evaluate_gate
from app.models import GateDecision

@pytest.mark.parametrize(
    "level, tool_kind, writes_so_far, max_auto_writes, expected",
    [(
       "shadow", #Autonomy Level
       "read",   #Tool Kind
        0,       #Writes so far
        10,      #Max Automaxtic Writes allowed
        GateDecision(allow=True, simulate=False, requires_approval=False, reason="Reads always allowed") #Expected Outcome
        ),
        
        ("shadow", "write", 2, 5, GateDecision(allow=True, simulate=True, requires_approval=False, reason="In Shadow autonomy level, agent should run as in production but, results are to be simulated and recorded")),
        ("supervised", "write", 2, 3, GateDecision(allow=False, simulate=False, requires_approval=True, reason="In Supervised autonomy level, agent is allowed to run as in production but, needs human approval at every step")),
        ("autonomous", "write", 2, 10, GateDecision(allow=True, simulate=False, requires_approval=False, reason="In Autonomous autonomy level,while the writes so far are less than max auto writes allowed, agent is allowed to run as in production")),
        ("autonomous", "write", 10, 10, GateDecision(allow=False, simulate=False, requires_approval=True, reason="In Autonomous autonomy level,while the writes so far are greater than or equal to max auto writes allowed, agent is allowed to run as in production but, requires human approval at every step"))]
)

def test_evaluate_gate(level, tool_kind, writes_so_far, max_auto_writes, expected):
    
    decision = evaluate_gate(
               level=level,
               tool_kind=tool_kind,
               writes_so_far=writes_so_far,
               max_auto_writes=max_auto_writes,
            )
    
    assert decision.allow == expected.allow
    assert decision.simulate == expected.simulate
    assert decision.requires_approval == expected.requires_approval