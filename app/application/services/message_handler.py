class MessageHandler:
    def __init__(self, interpreter, response_generator, conversation_repository, message_sender, intent_router):
        self.interpreter = interpreter
        self.response_generator = response_generator
        self.conversation_repository = conversation_repository
        self.message_sender = message_sender
        self.intent_router = intent_router

    async def handle(self, message):
        context = await self.conversation_repository.get_context(message.customer_id)
        intent = await self.interpreter.interpret(message, context)
        result = await self.intent_router.route(intent)
        response = await self.response_generator.generate({
            "message": message.text,
            "intent": intent,
            "result": result,
            "conversation": context,
        })
        await self.message_sender.send_text(message.customer_id, response)
