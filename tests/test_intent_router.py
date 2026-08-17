import pytest
from app.application.services.intent_router import IntentRouter
from app.domain.conversation.models import IntentType, UserIntent

class Handler:
    async def execute(self, parameters):
        return parameters

@pytest.mark.asyncio
async def test_route():
    router = IntentRouter({IntentType.SEARCH_COFFEE: Handler()})
    result = await router.route(UserIntent(IntentType.SEARCH_COFFEE, {"method": "V60"}))
    assert result == {"method": "V60"}
