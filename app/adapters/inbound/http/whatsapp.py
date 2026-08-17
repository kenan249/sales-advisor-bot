from fastapi import APIRouter, Request
from app.domain.conversation.models import IncomingMessage
from app.shared.container import get_message_handler

router = APIRouter(prefix="/webhooks", tags=["whatsapp"])

@router.get("/whatsapp")
async def verify_webhook():
    # TODO: implementar la verificación real de Meta.
    return {"status": "verification_endpoint_ready"}

@router.post("/whatsapp")
async def receive_webhook(request: Request):
    payload = await request.json()
    # TODO: mapear el payload real de Meta.
    message = IncomingMessage(
        customer_id=payload.get("customer_id", "unknown"),
        message_id=payload.get("message_id", "unknown"),
        text=payload.get("text", ""),
    )
    await get_message_handler().handle(message)
    return {"status": "ok"}
