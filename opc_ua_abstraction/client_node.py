# from client import SubHandler
# from custom_queue import RabbitmqPublisher
# import asyncio
from asyncua import Client
from asyncua.ua import BrowseDirection, NodeClass
# from datetime import datetime
from opcua_var import OpcuaVar
from opcua_object import OpcuaObject
from subscription_manager import SubscriptionManager
    

class ClientNode:
    def __init__(self, port:int) -> None:        
        self.__port:int = port
        self.__object_nodes:list[OpcuaObject] = []
        self.__client:Client = None
        self.__subscriptions:list[SubscriptionManager] = []

    @property
    def client(self):
        return self.__client
    
    @property
    def port(self):
        return self.__port
    
    @property
    def subscriptions(self):
        return [sub["name"] for sub in self.__subscriptions]
    
    @property
    def objects_names(self)->list[str]:
        return [obj.name for obj in self.__object_nodes]

    async def create(self):
        try:
            self.__client = Client(f"opc.tcp://localhost:{self.__port}")
            await self.__client.connect()

            root = self.__client.get_root_node()
            objects_node = await root.get_child(["0:Objects"])
            references = await objects_node.get_referenced_nodes(refs=31, direction=BrowseDirection.Both, nodeclassmask=NodeClass.Unspecified, includesubtypes=False)
            object_nodes = [node for node in references if node.nodeid.NamespaceIndex != 0]

            for object in object_nodes:
                obj = OpcuaObject(object, self.__client)
                await obj.create()
                self.__object_nodes.append(obj)
        except Exception as e:
            error = f"Error has occurred to client node! {e}"
            print(error)
            raise Exception(error)

    def get_object(self, name:str)->OpcuaObject|None:
        for obj in self.__object_nodes:
            if obj.name == name:
                return obj
        return None

    async def create_subscription(self, interval:int, name:str, handler):
        subscription = await self.__client.create_subscription(interval, handler)
        subData = SubscriptionManager(name, subscription)
        self.__subscriptions.append(subData)

    async def subscribe_node_var(self, node_var:OpcuaVar, subscription_name:str):
        sub = [sub for sub in self.__subscriptions if sub.name == subscription_name]
        if len(sub) == 0:
            return
        await sub[0].create_subscription(node_var)

    async def delete_subscription_by_name(self, name:str):
        sub = [sub for sub in self.__subscriptions if sub["name"] == name]
        if len(sub) == 0:
            return
        sub[0].delete()
        self.__subscriptions.remove(sub[0])

    async def delete_all_subscriptions(self):
        if len(self.__subscriptions)==0:
            return         
        [sub.delete() for sub in self.__subscriptions]

    async def disconnect(self):
        if self.__client != None:
            await self.__client.disconnect()

    