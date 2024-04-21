from asyncua import Node

class OpcuaVar:
    def __init__(self, node:Node, handle_value:int) -> None:
        self.name = ""
        self.__node = node
        self.handle_value = handle_value

    async def create(self):
        try:
            self.name = (await self.__node.read_browse_name()).Name
        except Exception as e:
            print("Error has occurred in opcua var!")
            print(e)
    
    
    async def get_value(self):
        return await self.__node.get_value()
    
    def set_handle_subscription_value(self, handle_value:int):
        self.handle_value = handle_value
    
