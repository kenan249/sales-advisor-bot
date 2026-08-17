from types import SimpleNamespace

import pytest

from app.adapters.outbound.ai.openai_adapter import OpenAIAdapter
from app.domain.conversation.models import IncomingMessage, IntentType


class FakeCompletions:
    def __init__(self, contents):
        self._contents = iter(contents)

    async def create(self, **kwargs):
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=next(self._contents)))]
        )


@pytest.mark.asyncio
async def test_interpret_returns_a_user_intent():
    adapter = OpenAIAdapter(api_key="test-key")
    adapter._client = SimpleNamespace(
        chat=SimpleNamespace(completions=FakeCompletions(['{"type": "SEARCH_COFFEE", "parameters": {"method": "V60"}}']))
    )

    intent = await adapter.interpret(
        IncomingMessage(customer_id="customer", message_id="message", text="Busco café para V60"),
        {},
    )

    assert intent.type == IntentType.SEARCH_COFFEE
    assert intent.parameters == {"method": "V60"}


@pytest.mark.asyncio
async def test_generate_returns_the_model_response():
    adapter = OpenAIAdapter(api_key="test-key")
    adapter._client = SimpleNamespace(
        chat=SimpleNamespace(completions=FakeCompletions(["Te recomiendo un café de origen Huila."]))
    )

    response = await adapter.generate({"message": "¿Qué me recomiendas?"})

    assert response == "Te recomiendo un café de origen Huila."


def test_invalid_intent_response_defaults_to_unknown():
    intent = OpenAIAdapter._parse_intent("not-json")

    assert intent.type == IntentType.UNKNOWN
    assert intent.parameters == {}
