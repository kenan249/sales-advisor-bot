from typing import Protocol

class MessageSender(Protocol):
    async def send_text(self, customer_id: str, text: str) -> None: ...
