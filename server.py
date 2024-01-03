# This code is based in https://github.com/FreeOpcUa
from opcua import ua, Server
import sys
import time
from datetime import datetime
import random
sys.path.insert(0, "..")

ADDRESS = "leonardo.local"


def get_set_temperature(variable_to_update):
    def set_temperature(parent, value):
        print("New Method")
        print("Changing temperature to:", value)
        print("Parent:", parent)
        variable_to_update.set_value(value)
        print("++++++++")
        return [ua.Variant(value, ua.VariantType.Float)]

    return set_temperature


def adjust_temperature(parent, value):
    print("Changing temperature to:", value)
    print("Parent:", parent)
    return [ua.Variant(value, ua.VariantType.Float)]

server = Server()
server.set_endpoint(f"opc.tcp://{ADDRESS}:3009")
server.set_server_name("Test OPC UA Server")
enums = server.load_enums()
# setup our own namespace, not really necessary but should as spec
uri1 = "Leonardo"
uri2 = "Maju"
idx1 = server.register_namespace(uri1)
idx2 = server.register_namespace(uri2)
print("IDX1: ", idx1)
print("IDX2: ", idx2)
objects = server.get_objects_node()
#+++++++++++++++++++++++++++++++++
machine5Obj = objects.add_object(idx1, "5. MACHINE_STAMPING")
machine5Obj.add_object(idx1, "Sensor Temperature")
sensor_value = random.randint(0, 100)/10
sensor_value_var5 = machine5Obj.add_variable(idx1, "Temperature", sensor_value)
machine_last_update_var1 = machine5Obj.add_variable(idx1, "LastUpdate", datetime.now())

sensor_value_var5.set_writable()
machine_last_update_var1.set_writable()
method = machine5Obj.add_method(idx1, "AdjustTemperature", get_set_temperature(sensor_value_var5), [ua.VariantType.Float], [ua.VariantType.Float])
#+++++++++++++++++++++++++++++++++
machine4Obj = objects.add_object(idx2, "4. MACHINE_STAMPING")
machine4Obj.add_object(idx2, "Sensor Temperature")
sensor_value = random.randint(0, 100)/10
sensor_value_var4 = machine4Obj.add_variable(idx2, "Temperature", sensor_value)
machine_last_update_var2 = machine4Obj.add_variable(idx2, "LastUpdate", datetime.now())

sensor_value_var4.set_writable()
machine_last_update_var2.set_writable()
method = machine4Obj.add_method(idx2, "AdjustTemperature", get_set_temperature(sensor_value_var4), [ua.VariantType.Float], [ua.VariantType.Float])
#+++++++++++++++++++++++++++++++++


server.start()
try:
    count = 0
    while True:
        time.sleep(2)
        machine_last_update_var1.set_value(datetime.now())
        machine_last_update_var2.set_value(datetime.now())

        # Remove comments to update the value of the variables on server
        sensor_value = random.randint(0, 100)/10
        # sensor_value_var5.set_value(sensor_value)

        sensor_value = random.randint(0, 100)/10
        # sensor_value_var4.set_value(sensor_value)
finally:
    #close connection, remove subcsriptions, etc
    server.stop()