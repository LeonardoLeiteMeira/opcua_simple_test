from asyncua import Node

# TODO
# Verificar sobre pegar metadados que definem o que o metodo faz, parametros e etc...
class OpcuaMethod:
    def __init__(self, node:Node, node_parent:Node) -> None:
        self.__node_parent = node_parent
        self.__node = node
        self.name = ""

    @classmethod
    async def create(self, node:Node, node_parent:Node):
        self.__node_parent = node_parent
        self.__node = node
        self.name = (await self.__node.read_browse_name()).Name
    
    def call_method(self, value):
        self.__node_parent.call_method(self.__node, value)