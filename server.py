# This code is based in https://github.com/FreeOpcUa
from opcua import ua, Server
import sys
import time
import datetime
sys.path.insert(0, "..")

ADDRESS = "leonardo.local"

def adjust_temperature(parent, value):
    print("Changing temperature to:", value)
    print("Parent:", parent)
    global myData1  # Referenciar a variável global
    myData1.set_value(value) 
    return [ua.Variant(value, ua.VariantType.Float)]
 
if __name__ == "__main__":
    server = Server()
    server.set_endpoint(f"opc.tcp://{ADDRESS}:3009")
    
    # setup our own namespace, not really necessary but should as spec
    uri = "Leonardo Leite Meira"
    idx = server.register_namespace(uri)
    print("IDX: ", idx)
    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()
    # populating our address space
    myobj = objects.add_object(idx, "Machine1")
    myData1 = myobj.add_variable(idx, "Temperature", 20)
    myDataDatetime = myobj.add_variable(idx, "M1Datetime", 0)
    myData1.set_writable()    # Set MyVariable to be writable by clients
    myDataDatetime.set_writable()    # Set MyVariable to be writable by clients
    # Create a function that will be called when a client calls the method
    method = myobj.add_method(idx, "AdjustTemperature", adjust_temperature, [ua.VariantType.Float], [ua.VariantType.Float])
    # starting!
    server.start()
    try:
        count = 0
        while True:
            time.sleep(2)
            count = myData1.get_value()
            count += 0.1
            myDataDatetime.set_value(datetime.datetime.now())
            myData1.set_value(count)
    finally:
        #close connection, remove subcsriptions, etc
        server.stop()