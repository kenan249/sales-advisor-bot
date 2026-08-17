class IntentRouter:
    def __init__(self, handlers: dict):
        self._handlers = handlers

    async def route(self, intent):
        handler = self._handlers.get(intent.type)
        if handler is None:
            raise ValueError(f"Unsupported intent: {intent.type}")
        return await handler.execute(intent.parameters)
