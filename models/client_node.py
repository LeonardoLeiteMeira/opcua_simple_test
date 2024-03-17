# from client import SubHandler
# from custom_queue import RabbitmqPublisher
# import asyncio
from asyncua import Client
from asyncua.ua import BrowseDirection, NodeClass
# from datetime import datetime

from models.opcua_object import OpcuaObject

class ClientNode:
    def __init__(self, port:int) -> None:
        self.__port = port
        self.__object_nodes = []
        self.__client = None

    @classmethod
    async def create(self, port:int):
        self.__object_nodes = []
        self.__port = port
        self.__client = Client(f"opc.tcp://localhost:{self.__port}")
        await self.__client.connect()

        root = self.__client.get_root_node()
        objects_node = await root.get_child(["0:Objects"])

        references = await objects_node.get_referenced_nodes(refs=31, direction=BrowseDirection.Both, nodeclassmask=NodeClass.Unspecified, includesubtypes=False)
        object_nodes = [node for node in references if node.nodeid.NamespaceIndex != 0]

        for object in object_nodes:
            self.__object_nodes.append(await
                OpcuaObject.create(object, self.__client)
            )

    async def disconnect(self):
        if self.__client != None:
            await self.__client.disconnect()

    