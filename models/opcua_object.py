from asyncua import Client, Node
from client import SubHandler
from models.opcua_method import OpcuaMethod
from models.opcua_var import OpcuaVar

class OpcuaObject:
    def __init__(self, node:Node, client: Client) -> None:
        self.name = ""
        self.__node = node
        self.__node_vars:list[OpcuaVar] = []
        self.__node_methods:list[OpcuaMethod] = []
        self.__client = client
        self.__subscription = None

    @classmethod
    async def create(self, node:Node, client: Client):
        self.__client = client
        self.__node = node
        self.__node_vars:list[OpcuaVar] = []
        self.__node_methods:list[OpcuaMethod] = []
        self.name = (await self.__node.read_browse_name()).Name
    
        self.__subscription = await self.__client.create_subscription(500, SubHandler(self.name, client))

        node_vars = await self.__node.get_variables()
        for var in node_vars:
            handle_value = await self.__subscription.subscribe_data_change(var)
            opcua_var = await OpcuaVar.create(var, handle_value)
            self.__node_vars.append(opcua_var)

        node_methods = self.__node.get_methods()
        for method in node_methods:
            opcua_method = await OpcuaMethod.create(method)
            self.__node_methods.append(opcua_method)
        
    async def dispose(self):
        if self.__subscription != None:
            await self.__subscription.delete()