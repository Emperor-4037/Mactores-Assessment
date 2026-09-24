import pytest
from app.model_client import complete_with_retry, MockModelClient, ThrottleError, FatalError
from app.config import SETTINGS

def test_retry_on_throttle():
    model = MockModelClient([
        ThrottleError("429"),
        ThrottleError("429"),
        '{"intent":"final","answer":"hi"}'
    ])

    result = complete_with_retry(model, [], SETTINGS)

    assert result == '{"final":"hi"}'
    assert model.calls == 3

def test_return_on_fatal():
    model = MockModelClient([
        FatalError("bad key"),
        '{"intent":"final", "answer":"hi"}'
    ])
    with pytest.raises(FatalError):
        complete_with_retry(model,[],SETTINGS)

    assert model.calls == 1