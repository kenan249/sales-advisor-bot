from typing import Protocol
from app.domain.conversation.models import IncomingMessage, UserIntent

class AIIntentInterpreter(Protocol):
    async def interpret(self, message: IncomingMessage, context: dict) -> UserIntent: ...

class AIResponseGenerator(Protocol):
    async def generate(self, context: dict) -> str: ...
