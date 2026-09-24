import pytest
from app.tools import Workspace, ToolError

def test_send_message_idempotency():
    # 1. Arrange
    ws = Workspace(contacts=[{"id": "c_1", "name": "Bob"}])
    
    # 2. Act (Call it TWICE with the exact same key!)
    result1 = ws.send_message(contact_id="c_1", body="hello", idempotency_key="key123")
    result2 = ws.send_message(contact_id="c_1", body="hello", idempotency_key="key123")
    
    # 3. Assert
    # The first one should be a fresh send
    assert result1["deduped"] == False
    # The second one should be caught by our safety net
    assert result2["deduped"] == True
    
    # MOST IMPORTANTLY: The message should only exist ONCE in the workspace.
    assert len(ws.messages) == 1