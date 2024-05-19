from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

    @property
    @abstractmethod
    def valor(self):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = float(valor)
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
    @property
    def valor(self):
        return self._valor

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = float(valor)

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []


    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nasc):
        self. cpf = cpf
        self.nome = nome
        self.data_nasc = data_nasc

        super().__init__(endereco)

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 500
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    #Método de fábrica para criar uma instância de Conta
    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@\n")
        
        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===\n")
            
            return True
        
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@\n")
            
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===\n")

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@\n")
            return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        self._limite = limite
        self._limite_saques = limite_saques
        super().__init__(numero, cliente)

    def sacar(self, valor):
        #Busca a quantidade de transações do tipo saque já efetuadas
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_limite_saques = numero_saques >= self._limite_saques
        
        if excedeu_limite_saques:
            print("\n@@@ Operação falhou! A quantidade de saques foi excedida! @@@\n")

        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor limite para saque foi excedido! @@@\n")

        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


def menu(titulo):
    # Menu de opcoes
    titulo_formatado = "" + titulo.center(len(titulo) + 20, "=")
    print(titulo_formatado)

    opcao = int(input(
        f'''
    Informe a opção desejada:

    [1] -> Saque
    [2] -> Depósito
    [3] -> Extrato
    [4] -> Cadastrar Cliente
    [5] -> Cadastrar Conta Corrente
    [6] -> Listar Contas
    [0] -> Sair
    '''
    ))

    return opcao

def sacar(clientes):
    cpf = input(f"Informe o seu CPF:")
    
    # Valida se o cliente está cadastrado
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\n@@@ Operação falhou! Cliente não cadastrado. @@@\n")
        return
    
    #valida se o cliente possui uma conta
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print("\n@@@ Operação falhou! Cliente não possui conta cadastrada. @@@\n")
        return
    
    valor = float(input(f"Informe o valor do saque:\n"))

    transacao = Saque(valor)

    cliente.realizar_transacao(conta, transacao)

def depositar(clientes):
    cpf = input(f"Informe o seu CPF:")
    
    # Valida se o cliente está cadastrado
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\nOperação falhou! Cliente não cadastrado.\n")
        return
    
    #valida se o cliente possui uma conta
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print("\nOperação falhou! Cliente não possui conta cadastrada.\n")
        return
    
    valor = float(input(f"Informe o valor do depósito:\n"))

    transacao = Deposito(valor)

    cliente.realizar_transacao(conta, transacao)

def filtrar_clientes(cpf, clientes):
    for cliente in clientes:
        cliente_existe = cliente.cpf == cpf

        if cliente_existe:
            return cliente

def recuperar_conta_cliente(cliente):

    if not cliente.contas:
        return
    
    return cliente.contas[0]

def cadastrar_cliente(clientes):
    cpf = input("Informe o CPF do cliente:\n")

    cliente = filtrar_clientes(cpf, clientes)

    if cliente:
        print("Cliente já cadastrado.")
        return
    
    nome = input("Informe o nome do cliente:\n")
    endereco = input("Informe o endereço do cliente:\n")
    data_nasc = input("Informe a data de nascimento do cliente:\n")

    cliente = PessoaFisica(endereco, cpf, nome, data_nasc)

    print("\nCliente cadastrado com sucesso\n")

    clientes.append(cliente)

def cadastrar_conta(numero, clientes, contas):
    cpf = input("Informe o CPF do cliente:\n")

    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print(f"\n @@@ Operação falhou! Cliente não cadastrado para o CPF: {cpf}. @@@\n")
        return    
    
    conta = ContaCorrente.nova_conta(numero, cliente)
    contas.append(conta)
    cliente.contas.append(conta)

    print(f"\n @@@ Conta cadastrada para o cliente {cliente.nome}  @@@\n")

def listar_contas(contas):
    print("\n====== Contas Cadastradas ======\n")

    if len(contas) == 0:
        print("@@@ Operação falhou! Nenhuma conta cadastrada! @@@ \n")
        return

    for conta in contas:
        print(f"Conta: {conta.numero}")
        print(f"CPF: {conta.cliente.cpf}")
        print(f"Nome: {conta.cliente.nome}\n")        

def exibir_extrato(clientes):
    cpf = input("Informe o seu CPF:\n")
    
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print("\n@@@ Operação falhou! Cliente não cadastrado! @@@\n")
        return
    
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        print(f"\n@@@ Operação falhou! Conta não cadastrada para o CPF: {cliente.cpf}! @@@\n")
        return

    transacoes = conta.historico.transacoes

    print(f"\n====== Extrato conta número: {conta.numero} ======\n")

    if len(transacoes) > 0:
        for transacao in transacoes:
            print(f"{transacao["tipo"]}     R${transacao["valor"]:.2f}      {transacao["data"]}")
    
    else:
        print("\n Conta ainda não possui transações.\n")

    print(f"\n Saldo: R$ {conta.saldo:.2f}\n")
    print(f"\n====== Fim Extrato ======\n")

def main():    
    clientes = []
    contas = []
    
    while True:
        # Menu de opcoes
        opcao = menu("Banco PC")

        # Operação de Saque
        if (opcao == 1):
            sacar(clientes)
                    
        #Operação depositar
        elif(opcao == 2):
            depositar(clientes)

        #Operação exibir extrato
        elif(opcao == 3):
            exibir_extrato(clientes)

        #Operação cadastrar cliente
        elif(opcao == 4):            
            cadastrar_cliente(clientes)

        #Operação cadastrar conta
        elif(opcao == 5):
            numero = len(contas) + 1
            cadastrar_conta(numero, clientes, contas)

        #Operação listar contas
        elif(opcao == 6):
            listar_contas(contas)

        elif(opcao == 0):
            break

        else:
            print("Operação falhou. Digite uma opção válida.")

main()