import asyncio
from asyncua import Client, Node
from asyncua.ua import DataChangeNotification
from datetime import datetime

# TODO
# Verificar se criar uma fila para canda instancia do SubHandler - Se e performatico, se e o ideal e etc...
class SubHandler:
    def __init__(self, id:str, client:Client) -> None:
        self.id = id
        self.client = client
        
    def datachange_notification(self, node:Node, data:any, data_change:DataChangeNotification):
        time_stamp:datetime = data_change.monitored_item.Value.SourceTimestamp
        # print("\nNew notification")
        # print("Time Stamp: ", time_stamp)   
        # print("Node of the event: ", node)
        # print("New data received: ", data)
        # print("Data Change: ", data_change)
        # print("\n")
        asyncio.create_task(self.data_change_notification(node, data, data_change, self.server_port, self.client))

    async def data_change_notification(self, node:Node, val, data:DataChangeNotification, port, client:Client):
        node_obj = client.get_node(node.nodeid)
        browse_name = await node_obj.read_browse_name()
        sensor_name = browse_name.Name
        print(f"{node} - {sensor_name}: {val}")
        # print(f"{port} - Valor alterado no {node} - {sensor_name}: {val}")

        time_stamp:datetime = data.monitored_item.Value.SourceTimestamp
        # my_queue.send_message({
        #     "time_stamp": time_stamp.isoformat(),
        #     "name": sensor_name, 
        #     "data_type": str(data),
        #     "value": val,
        # })