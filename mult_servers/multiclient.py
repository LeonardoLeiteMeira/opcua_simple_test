from initial_tests.client import SubHandler
from custom_queue import RabbitmqPublisher
import asyncio
from asyncua import Client
from asyncua.ua import BrowseDirection, NodeClass
# from datetime import datetime


my_queue = RabbitmqPublisher()

my_map = {}

async def subscribe_to_node(port:int):
    client = Client(f"opc.tcp://localhost:{port}")
    await client.connect()
    root = client.get_root_node()

    # server_node = client.nodes.server
    # server_state = await server_node.get_child("0:ServerStatus")
    # server_name = await (
    #         await (
    #             await server_state.get_child("0:BuildInfo")
    #         ).get_child("0:ProductName")
    #     ).read_value()
    
    # print("Nome do Servidor:", server_name)
    server_node = client.get_node("ns=0;i=2253")  # NodeId para o objeto Server
    server_name = await(await server_node.get_child(["0:ServerStatus", "0:BuildInfo", "0:ProductName"])).get_value()
    print("Nome do Servidor:", server_name)

    objects_node = await root.get_child(["0:Objects"])
    references = await objects_node.get_referenced_nodes(refs=31, direction=BrowseDirection.Both, nodeclassmask=NodeClass.Unspecified, includesubtypes=False)
    custom_nodes = [node for node in references if node.nodeid.NamespaceIndex != 0]
    subscription = await client.create_subscription(500, SubHandler(port, client))
    node_vars_list = [await node.get_variables() for node in custom_nodes]
    handles = []

    for node in custom_nodes:
        node_obj = client.get_node(node.nodeid)
        browse_name = await node_obj.read_browse_name()
        print(f"+++++++++++++")
        print(f"Node: {node} - {browse_name.Name}")        
        print(f"+++++++++++++")
        # print(f"Browse Name: {browse_name.Name}\n")

    for node_vars in node_vars_list:
        for node in node_vars:
            handles.append(await subscription.subscribe_data_change(node))
            node_obj = client.get_node(node.nodeid)
            browse_name = await node_obj.read_browse_name()
            print(f"+++++++++++++")
            print(f"Node: {node} - {browse_name.Name}")
            print(f"+++++++++++++")

    return client, subscription, handles

async def main():
    ADDRESS = "localhost"
    PORTS = [3010]
    # PORTS = [3010, 3011, 3012, 3013, 3014, 3015, 3016]

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
