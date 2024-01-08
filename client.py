# This is basee in https://github.com/FreeOpcUa
from opcua import Client, Node
from opcua.ua import BrowseDirection, NodeClass, DataChangeNotification, EventFilter, ObjectIds
import time
import sys
import random
sys.path.insert(0, "..")

ADDRESS = "localhost"
# ADDRESS = "192.168.0.44"

def show_node_info(node:Node, type_node):
    print("\n+_+_+_+_+_+_+_+_+_+_+")
    print(type_node)
    print("node ",node)
    browse_name = node.get_browse_name()
    print("node.get_browse_name: ",browse_name)
    print("node.get_variables: ",node.get_variables())
    print("node.get_display_name: ",node.get_display_name())
    children = node.get_children()
    print("node.get_children: ",children)
    print("node.get_parent: ",node.get_parent())
    methods = node.get_methods()
    print("node.get_methods: ",methods)
    print("+_+_+_+_+_+_+_+_+_+_+\n")

class SubHandler():
    def datachange_notification(self, node:Node, data:any, data_change:DataChangeNotification):
        time_stamp = data_change.monitored_item.Value.SourceTimestamp
        print("\nNew notification")
        print("Time Stamp: ", time_stamp)   
        print("Node of the event: ", node)
        print("New data received: ", data)
        print("Other: ", data_change)
        print("\n")
 
if __name__ == "__main__":
    client = Client(f"opc.tcp://{ADDRESS}:3009")
    try:
        client.connect()
        
        # Client has a few methods to get proxy to UA nodes that should always be in address space
        root = client.get_root_node()
        print("Root is: ", root)
        
        objectId = root.get_child(["0:Objects"])
        print("OBJ List: ", objectId)

        # IMPORTANT
        # Aqui ele retorna os nodos filhos, Root, FoolderType, Server e aqueles criados no servidor
        # Os parametros da funcao filtram os objetos
        references = objectId.get_referenced_nodes(refs=31, direction=BrowseDirection.Both, nodeclassmask=NodeClass.Unspecified, includesubtypes=False)
        names = client.get_namespace_array()
        print("References: ", references)

        # NamespaceIndex = 0 => Node Padrao do OPC UA
        # NamespaceIndex != 0 => Node criado no servidor
        default_nodes = [node for node in references if node.nodeid.NamespaceIndex == 0]
        custom_nodes = [node for node in references if node.nodeid.NamespaceIndex != 0]


        # print("======== Subscriptions ========")
        subscription = client.create_subscription(500, SubHandler())
        node_vars = [node.get_variables() for node in custom_nodes]
        handles = [subscription.subscribe_data_change(node_var) for node_var in node_vars]

        time.sleep(3)

        # print("======== Events ========")
        # This code is not working
        # event_filter = EventFilter()
        # event_filter.add_select_clause(ObjectIds.ConditionType_ConditionName)
        # event_filter.add_select_clause(ObjectIds.ConditionType_Severity)
        # event_filter.add_select_clause(ObjectIds.ConditionType_Message)
        # event_filter.add_select_clause(ObjectIds.ConditionType_ConditionState)



        time.sleep(3)

        print("DEFAULT NODES FROM OPC UA")
        for node in default_nodes:
            show_node_info(node, "Node")

        print("CUSTOM NODES FROM SERVER")
        for node in custom_nodes:
            show_node_info(node, "Node")

            print("\n++++++Test change var value+++++++")
            vars = node.get_variables()
            for var in vars:
                print(f"{var} - Current Value: ",var.get_value())

            new_value = round(random.random() * 100, 2)
            print("Vew var value: ", new_value) 

            methods = node.get_methods()
            node.call_method(methods[0], new_value)

            for var in vars:
                print(f"{var} - Value After Update: ",var.get_value())

            print("+++++++++++++++\n")
            
            print("-------- Show Info about chuildren --------")
            children = node.get_children()
            for sub_node in children:
                show_node_info(sub_node, "SubNode")
            print("----------------\n")


        while True:
            #Listem de changes on server
            pass

        
    finally:
        client.disconnect()