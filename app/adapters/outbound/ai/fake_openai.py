from app.domain.conversation.models import IntentType, UserIntent

class FakeAIAdapter:
    async def interpret(self, message, context):
        text = message.text.lower()
        if "v60" in text or "café" in text or "cafe" in text:
            return UserIntent(
                type=IntentType.SEARCH_COFFEE,
                parameters={"method": "V60" if "v60" in text else None}
            )
        return UserIntent(type=IntentType.UNKNOWN, parameters={})

    async def generate(self, context):
        result = context.get("result")
        return f"Encontré estas opciones: {result}" if result else "Cuéntame qué café estás buscando y te ayudo."
