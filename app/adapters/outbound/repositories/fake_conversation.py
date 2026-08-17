class FakeConversationRepository:
    async def get_context(self, customer_id):
        return {}
    async def save_context(self, customer_id, context):
        pass
