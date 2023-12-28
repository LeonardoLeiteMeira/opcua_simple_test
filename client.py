# This code from https://github.com/FreeOpcUa
from opcua import Client
from opcua.ua import BrowseDirection, NodeClass
import time
import sys
import random
sys.path.insert(0, "..")

ADDRESS = "localhost"
# ADDRESS = "192.168.0.44"
 
if __name__ == "__main__":
    client = Client(f"opc.tcp://{ADDRESS}:3009")
    try:
        client.connect()
        # Client has a few methods to get proxy to UA nodes that should always be in address space
        root = client.get_root_node()
        print("Root is: ", root)
        
        objectId = root.get_child(["0:Objects"])
        print("OBJ List: ", objectId)

        #IMPORTANT
        # Aqui ele retorna os nodos filhos, Root, FoolderType, Server e aqueles criados no servidor
        # Os parametros da funcao filtram os objetos
        # mas provavelmente terei que separa os objetos do servidor dos objetos criados no servidor (q eu quero)
        references = objectId.get_referenced_nodes(refs=31, direction=BrowseDirection.Both, nodeclassmask=NodeClass.Unspecified, includesubtypes=False)

        print("References: ", references)
        print("===")
        for node in references:
            print("+_+_+_+_+_+_+_+_+_+_+")
            print("node ",node)
            print("node.get_browse_name: ",node.get_browse_name())
            print("node.get_variables: ",node.get_variables())
            print("node.get_display_name: ",node.get_display_name())
            print("node.get_children: ",node.get_children())
            #TODO Testar a execucao de um metodo
            print("node.get_methods: ",node.get_methods())
            print("node.get_parent: ",node.get_parent())
            print("+++++++++++++")

                    
        print("===")







        obj = root.get_child(["0:Objects", "2:Machine1"])
        temperature = root.get_child(["0:Objects", "2:Machine1", "2:Temperature"])
        m1Datetime = root.get_child(["0:Objects", "2:Machine1", "2:M1Datetime"])
        change_temperature = root.get_child(["0:Objects", "2:Machine1", "2:AdjustTemperature"])
        print("Method: ", change_temperature)
        print("myobj is: ", obj)
        print("myData1 is: ", temperature)
        print("M1Datetime is: ", m1Datetime)
        while True:
            print("myData1 = %4.1f" %client.get_node(temperature).get_value())
            # print("Mais info sobre myData1 = %4.1f" %client.get_node(myData1)...any item that is a variable)
            # print("myData1 = %4.1f" %client.get_node("ns=2;i=2").get_value())
            print("m1Datetime = ", client.get_node(m1Datetime).get_value().strftime("%Y-%m-%d     %H:%M:%S"))
            # print("myDataDatetime = ", client.get_node("ns=2;i=3").get_value().strftime("%Y-%m-%d     %H:%M:%S"))
            new_value = random.random() * 100
            # root.call_method(change_temperature, new_value)
            time.sleep(4)
    finally:
        client.disconnect()