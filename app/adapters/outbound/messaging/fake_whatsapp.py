class FakeWhatsAppAdapter:
    async def send_text(self, customer_id, text):
        print(f"[FAKE WHATSAPP] -> {customer_id}: {text}")
