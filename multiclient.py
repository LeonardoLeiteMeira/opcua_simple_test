import asyncio
from asyncua import Client, Node
from asyncua.ua import BrowseDirection, NodeClass, DataChangeNotification, EventFilter, ObjectIds
import time

async def data_change_notification(node, val, data, port):
    print(f"{port} - Valor alterado no {node}: {val}")
    print(f"{port} - Tarefa demorada concluida")

async def subscribe_to_node(port:int):
    client = Client(f"opc.tcp://localhost:{port}")
    await client.connect()
    root = client.get_root_node()
    objects_node =await  root.get_child(["0:Objects"])
    references = await objects_node.get_referenced_nodes(refs=31, direction=BrowseDirection.Both, nodeclassmask=NodeClass.Unspecified, includesubtypes=False)
    custom_nodes = [node for node in references if node.nodeid.NamespaceIndex != 0]
    subscription = await client.create_subscription(500, SubHandler(port))
    node_vars_list = [await node.get_variables() for node in custom_nodes]
    handles = []
    for node_vars in node_vars_list:
        temp_handles = [await subscription.subscribe_data_change(node_var) for node_var in node_vars]
        handles.append(temp_handles)

    return client, subscription, handles
    

class SubHandler:
    def __init__(self, port:int) -> None:
        self.server_port = port
        
    def datachange_notification(self, node:Node, data:any, data_change:DataChangeNotification):
        time_stamp = data_change.monitored_item.Value.SourceTimestamp
        # print("\nNew notification")
        # print("Time Stamp: ", time_stamp)   
        # print("Node of the event: ", node)
        # print("New data received: ", data)
        # print("Data Change: ", data_change)
        # print("\n")
        asyncio.create_task(data_change_notification(node, data, data_change, self.server_port))

async def main():
    ADDRESS = "localhost"
    PORTS = [3010, 3011, 3012, 3013, 3014, 3015, 3016]

    tasks = [subscribe_to_node(port) for port in PORTS]
    results = await asyncio.gather(*tasks)

    print("Subscrições ativas. Pressione Ctrl+C para sair.")
    try:
        while True:
            await asyncio.sleep(1)  # Sleep por 1 segundo
    except KeyboardInterrupt:
        print("Encerrando programa...")
    finally:
        print("Fechando conexões...")
        for client, subscription, handles in results:
            await subscription.delete()
            await client.disconnect()
        print("Encerramento concluido.")

if __name__ == "__main__":
    asyncio.run(main())
