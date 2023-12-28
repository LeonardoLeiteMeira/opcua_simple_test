# This code from https://github.com/FreeOpcUa
from opcua import Client
from opcua.ua import BrowseDirection, NodeClass
import time
import sys
import random
sys.path.insert(0, "..")

ADDRESS = "localhost"
# ADDRESS = "192.168.0.44"

def show_node_info(node, type_node):
    print("+_+_+_+_+_+_+_+_+_+_+")
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
    print("+_+_+_+_+_+_+_+_+_+_+")
 
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

        print("DEFAULT NODES FROM OPC UA")
        for node in default_nodes:
            show_node_info(node, "Node")

        print("CUSTOM NODES FROM SERVER")
        for node in custom_nodes:
            show_node_info(node, "Node")

            print("++++++Test change var value+++++++")
            vars = node.get_variables()
            for var in vars:
                print(f"{var} - Current Value: ",var.get_value())

            new_value = round(random.random() * 100, 2)
            print("Vew var value: ", new_value) 

            methods = node.get_methods()
            node.call_method(methods[0], new_value)

            for var in vars:
                print(f"{var} - Value After Update: ",var.get_value())

            print("+++++++++++++++")
            
            print("-------- Show Info about chuildren --------")
            children = node.get_children()
            for sub_node in children:
                show_node_info(sub_node, "SubNode")
            print("----------------")
        
    finally:
        client.disconnect()