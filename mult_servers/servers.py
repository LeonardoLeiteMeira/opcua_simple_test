# This code have the objective to create a list of OPC UA servers to test a client with multiple connections.
from opcua import Server, ua
import threading
import time
import random
import sys

sys.path.insert(0, "..")

ADDRESS = "localhost"
PORTS = [3010]

def get_set_interval(variable_to_update):
    def set_interval(parent, value):
        print("New Method")
        print("Changing value to:", value)
        print("Parent:", parent)
        variable_to_update.set_value(value)
        print("++++++++")
        return [ua.Variant(value, ua.VariantType.Float)]

    return set_interval

def create_server(port):
    server = Server()
    server.set_endpoint(f"opc.tcp://{ADDRESS}:{port}")
    server.set_server_name(f"Machine Stamping - {port}")

    sensor_uri = "Sensors"
    metadata_uri = "Metadata"

    sensor_namespace = server.register_namespace(sensor_uri)
    metadata_namespace = server.register_namespace(metadata_uri)

    objects = server.get_objects_node()

    temperature_obj = objects.add_object(sensor_namespace, "Temperature Sensor")
    sensor_value = random.randint(0, 100) / 10
    temperature_sensor_var = temperature_obj.add_variable(sensor_namespace, "value do temperatura", sensor_value)
    temperature_colect_interval = temperature_obj.add_variable(sensor_namespace, "Intervalo de coleta", 10.0)
    temperature_obj_method = temperature_obj.add_method(sensor_namespace, "SetInterval", get_set_interval(temperature_colect_interval), [ua.VariantType.Float], [ua.VariantType.Float])
    temperature_sensor_var.set_writable()
    temperature_colect_interval.set_writable()


    status_obj = objects.add_object(metadata_namespace, "Status")
    sensor_value_var = status_obj.add_variable(metadata_namespace, "value do status", True)
    sensor_value_var.set_writable()

    server.start()
    try:
        while True:
            temperature_colect_interval_value = temperature_colect_interval.get_value()
            time.sleep(temperature_colect_interval_value)
            sensor_value = random.randint(0, 100) / 10
            temperature_sensor_var.set_value(sensor_value)
            print(f"{port} New Value on {port}: {sensor_value}", flush=True)
    finally:
        server.stop()

# Criando e iniciando uma thread para cada servidor
threads = []
for port in PORTS:
    thread = threading.Thread(target=create_server, args=(port,))
    thread.start()
    threads.append(thread)

print("++++++++++++++++ Servers started ++++++++++++++++", flush=True)
# Esperar todas as threads terminarem (opcional)
for thread in threads:
    thread.join()
