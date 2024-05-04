from asyncua import Client, Node
from opcua_method import OpcuaMethod
from opcua_var import OpcuaVar

class OpcuaObject:
    def __init__(self, node:Node, client: Client) -> None:
        self.name = ""
        self.__node = node
        self.__node_vars:list[OpcuaVar]|None = None
        self.__node_methods:list[OpcuaMethod]|None = None
        self.__client = client
        self.__subscription = None

    @property
    def var_names(self):
        if self.__node_vars is None:
            return []
        return [var.name for var in self.__node_vars]

    @property
    def method_names(self):
        if(self.__node_methods == None):
            return []
        return [method.name for method in self.__node_methods]

    async def create(self):
        try:
            self.name = (await self.__node.read_browse_name()).Name
        
            # self.__subscription = await self.__client.create_subscription(500, SubHandler(self.name, client))

            node_vars = await self.__node.get_variables()
            for var in node_vars:
                # TODO verificar sobre subscricao 
                # handle_value = await self.__subscription.subscribe_data_change(var)
                opcua_var = OpcuaVar(var,1)
                await opcua_var.create()
                if(self.__node_vars == None):
                    self.__node_vars = []
                self.__node_vars.append(opcua_var)

            node_methods = await self.__node.get_methods()
            for method in node_methods:
                opcua_method = OpcuaMethod(method, self.__node)
                await opcua_method.create()
                if(self.__node_methods == None):
                    self.__node_methods = []
                self.__node_methods.append(opcua_method)
        except Exception as e:
            print("Error has occurred in opcua object!")
            print(e)
    
    def get_var(self, name:str):
        for var in self.__node_vars:
            if var.name == name:
                return var
        return None

    def get_method(self, name:str):
        for method in self.__node_methods:
            if method.name == name:
                return method
        return None
        
    async def dispose(self):
        if self.__subscription != None:
            await self.__subscription.delete()