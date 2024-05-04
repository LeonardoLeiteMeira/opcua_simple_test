
import asyncio
import time
from client_node import ClientNode
from sub_handler import SubHandler


async def main():
    port = 3010
    print("Starting Client Node...")
    client_node = ClientNode(port)
    await client_node.create()
    print('\n\nLendo os nomes dos objetos')
    obj_names = client_node.objects_names
    print(obj_names)
    print('-'*30,"\n")

    print('Lendo os dados dos objetos\n')
    for obj_name in obj_names:
        print(obj_name)
        obj = client_node.get_object(obj_name)
        print('Nome das variaveis')
        print(obj.var_names, '\n')
        print('Nome dos metodos')
        print(obj.method_names, '\n')
        print('-'*30,"\n")

    print('+'*30,"\n")

    print('Agora pegando o valor da temperatura\n')
    for obj_name in obj_names:
        obj = client_node.get_object(obj_name)
        value_temperature_name = obj.var_names[0]
        temperature = obj.get_var(value_temperature_name)
        
        count = 0
        # while count<11:
        #     print('Valor atual: ',await temperature.get_value())
        #     time.sleep(1)
        #     count+=1

    print('Agora testando a variavel intervalo de coleta\n')

    temperature_sensor = client_node.get_object('Temperature Sensor')
    var_interval = temperature_sensor.get_var('Intervalo de coleta')
    print('Alterando o intervalo de coleta para 5 segundos')
    set_interval_method = temperature_sensor.get_method('SetInterval')
    await set_interval_method.call_method(5)

    print('Valor do intervalo de coleta apos a alteracao: ', await var_interval.get_value())

    print('\nFazendo a leitura da variavel com o intervalo de coleta alterado\n')
    var_temperature = temperature_sensor.get_var('value do temperatura')
    count = 0
    # while count<11:
    #     print('Valor atual: ',await var_temperature.get_value())
    #     time.sleep(1)
    #     count+=1

    sub_handler = SubHandler(port, client_node.client)
    await client_node.create_subscription(500, 'Sub1', sub_handler)

    firstObj = client_node.get_object(obj_names[0])
    var_names = firstObj.var_names
    var_to_subscribe = firstObj.get_var(var_names[0])

    await client_node.subscribe_node_var(var_to_subscribe, 'Sub1')

    while True:
        await asyncio.sleep(1)
    

if __name__ == "__main__":
    asyncio.run(main())