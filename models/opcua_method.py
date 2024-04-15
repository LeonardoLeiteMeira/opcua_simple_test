from asyncua import Node

# TODO
# Verificar sobre pegar metadados que definem o que o metodo faz, parametros e etc...

# TODO 
# No servers foi criado uma variavel que armazena o valor do intervalo de coleta, e um metodo que altera esse valor
# Devo testar esse metodo para varia o intervalo de coleta 
# Basicametne rodar o client_node se conectar com sucesso ao server e chamar esse metodo que foi criado
# Para isso devo criar um ponto que iniciar a classe client_node, lista os metodos de cada servidor e dar a opcao de chamar um metodo passando um valor
# depois disso verificar sobre como coletar a informacao de que esse metodo recebe como parametro um float
# e depois verificar como checar se o metodo foi chamado com sucesso

class OpcuaMethod:
    def __init__(self, node:Node, node_parent:Node) -> None:
        self.__node_parent = node_parent
        self.__node = node
        self.name = ""

    @classmethod
    async def create(self, node:Node, node_parent:Node):
        self.__node_parent = node_parent
        self.__node = node
        self.name = (await self.__node.read_browse_name()).Name
    
    def call_method(self, value):
        self.__node_parent.call_method(self.__node, value)