from asyncua import Node

class OpcuaVar:
    def __init__(self, node:Node, handle_value:int) -> None:
        self.name = ""
        self.__node = node
        self.handle_value = handle_value

    @classmethod
    async def create(self, node:Node, handle_value:int):
        self.__node = node
        self.handle_value = handle_value
        self.name = (await self.__node.read_browse_name()).Name