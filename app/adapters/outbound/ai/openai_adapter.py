import json
from typing import Any

from openai import AsyncOpenAI

from app.domain.conversation.models import IncomingMessage, IntentType, UserIntent


class OpenAIAdapter:
    """Adaptador de OpenAI para interpretar mensajes y generar respuestas."""

    def __init__(self, api_key: str, model: str = "gpt-4.1-mini") -> None:
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = model

    async def interpret(self, message: IncomingMessage, context: dict) -> UserIntent:
        completion = await self._client.chat.completions.create(
            model=self._model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Clasifica el mensaje de un cliente de una cafetería. "
                        "Responde exclusivamente JSON con las claves 'type' y 'parameters'. "
                        f"type debe ser uno de: {', '.join(intent.value for intent in IntentType)}. "
                        "parameters debe ser un objeto. Usa UNKNOWN si no puedes identificar la intención."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {"message": message.text, "conversation": context},
                        default=str,
                        ensure_ascii=False,
                    ),
                },
            ],
        )
        content = completion.choices[0].message.content or "{}"
        return self._parse_intent(content)

    async def generate(self, context: dict) -> str:
        completion = await self._client.chat.completions.create(
            model=self._model,
            temperature=0.7,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres el asesor de ventas de una cafetería. Responde en español, "
                        "de forma cordial, breve y útil, usando el resultado disponible."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(context, default=str, ensure_ascii=False),
                },
            ],
        )
        return completion.choices[0].message.content or "No pude generar una respuesta en este momento."

    @staticmethod
    def _parse_intent(content: str) -> UserIntent:
        try:
            payload: dict[str, Any] = json.loads(content)
            intent_type = IntentType(payload.get("type", IntentType.UNKNOWN.value))
            parameters = payload.get("parameters", {})
            if not isinstance(parameters, dict):
                parameters = {}
            return UserIntent(type=intent_type, parameters=parameters)
        except (json.JSONDecodeError, TypeError, ValueError):
            return UserIntent(type=IntentType.UNKNOWN, parameters={})
