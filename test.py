import asyncio
from app.adapters.outbound.ai.openai_adapter import OpenAIAdapter
from app.domain.conversation.models import IncomingMessage
from app.shared.config import settings


async def main():
    adapter = OpenAIAdapter(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
      )

    message = IncomingMessage(
        customer_id="317895896",
        message_id="m1",
        text="quiero un café geisha de 250 gramos",
      )
    user_intent = await adapter.interpret(message, context={})

    response = await adapter.generate({
          "message": message.text,
          "intent": user_intent,
          "result": {
              "coffee": "Geisha",
              "weight": "250 g",
              "price": 45000,
          },
          "conversation": {},
      })

    print(f"Intención: {user_intent.type.value}")
    print(f"Parámetros: {user_intent.parameters}")
    print(f"Respuesta: {response}")


if __name__ == "__main__":
    asyncio.run(main())