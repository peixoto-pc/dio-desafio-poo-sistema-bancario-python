from abc import ABC, abstractmethod
from typing import List

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        # Implementação para registrar depósito
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        # Implementação para registrar saque
        pass

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

class Conta:
    def __init__(self, cliente, numero):
        self.cliente = cliente
        self.numero = numero
        self.saldo = 0
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    def nova(self, cliente, numero):
        # Implementação para criar nova conta
        pass

    def sacar(self, valor):
        # Implementação para realizar saque
        pass

    def depositar(self, valor):
        # Implementação para realizar depósito
        pass

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite, limite_saques):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        # Implementação para realizar transação
        pass
