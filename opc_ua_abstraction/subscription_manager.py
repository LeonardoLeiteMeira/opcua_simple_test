from asyncua.common.subscription import Subscription

from opcua_var import OpcuaVar

class SubscriptionManager:
    def __init__(self, name:str, subscription:Subscription) -> None:
        self.name:str = name
        self.subscription:Subscription = subscription
        self.handler_value:int|None = None

    async def create_subscription(self, node_var:OpcuaVar):
        self.handler_value = await self.subscription.subscribe_data_change(node_var.node)
        return self.handler_value
    
    def delete(self):
        self.subscription.delete()