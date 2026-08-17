from app.adapters.outbound.ai.fake_openai import FakeAIAdapter
from app.adapters.outbound.ai.openai_adapter import OpenAIAdapter
from app.adapters.outbound.messaging.fake_whatsapp import FakeWhatsAppAdapter
from app.adapters.outbound.repositories.fake_coffee import FakeCoffeeRepository
from app.adapters.outbound.repositories.fake_conversation import FakeConversationRepository
from app.application.services.intent_router import IntentRouter
from app.application.services.message_handler import MessageHandler
from app.application.use_cases.search_coffee import SearchCoffeeUseCase
from app.application.use_cases.get_recipe import GetRecipeUseCase
from app.application.use_cases.add_to_cart import AddToCartUseCase
from app.application.use_cases.get_cart import GetCartUseCase
from app.application.use_cases.create_order import CreateOrderUseCase
from app.application.use_cases.get_order_status import GetOrderStatusUseCase
from app.domain.conversation.models import IntentType
from app.shared.config import settings

def build_message_handler():
    ai = (
        OpenAIAdapter(api_key=settings.openai_api_key, model=settings.openai_model)
        if settings.openai_api_key
        else FakeAIAdapter()
    )
    handlers = {
        IntentType.SEARCH_COFFEE: SearchCoffeeUseCase(FakeCoffeeRepository()),
        IntentType.GET_RECIPE: GetRecipeUseCase(),
        IntentType.ADD_TO_CART: AddToCartUseCase(),
        IntentType.GET_CART: GetCartUseCase(),
        IntentType.CREATE_ORDER: CreateOrderUseCase(),
        IntentType.GET_ORDER_STATUS: GetOrderStatusUseCase(),
    }
    return MessageHandler(
        interpreter=ai,
        response_generator=ai,
        conversation_repository=FakeConversationRepository(),
        message_sender=FakeWhatsAppAdapter(),
        intent_router=IntentRouter(handlers),
    )

_message_handler = build_message_handler()

def get_message_handler():
    return _message_handler
