from dataclasses import dataclass
from enum import Enum

class IntentType(str, Enum):
    GREETING = "GREETING"
    SEARCH_COFFEE = "SEARCH_COFFEE"
    GET_RECIPE = "GET_RECIPE"
    ADD_TO_CART = "ADD_TO_CART"
    GET_CART = "GET_CART"
    CREATE_ORDER = "CREATE_ORDER"
    GET_ORDER_STATUS = "GET_ORDER_STATUS"
    UNKNOWN = "UNKNOWN"

@dataclass(frozen=True)
class IncomingMessage:
    customer_id: str
    message_id: str
    text: str
    channel: str = "WHATSAPP"

@dataclass(frozen=True)
class UserIntent:
    type: IntentType
    parameters: dict
