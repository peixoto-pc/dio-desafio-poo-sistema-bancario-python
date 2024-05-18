from abc import ABC, abstractmethod


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
        pass
    
    @property
    def valor(self):
        return self.valor

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = float(valor)

    @property
    def valor(self):
        return self.valor

class Historico:
    def __init__(self):
        self.transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []


    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

dep = Deposito(100)