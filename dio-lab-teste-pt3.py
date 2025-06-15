from abc import ABC, abstractclassmethod,
abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._numero = numero
        self._agencia = "0001"
        self._saldo = 0
        self._cliente = cliente
        self.historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

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

    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Saldo insuficiente para saque.")

        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de {valor} realizado com sucesso.")
            return True
        
        else:
            print("Valor de saque inválido.")

        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de {valor} realizado com sucesso.")
        
        else:
            print("Valor de depósito inválido.")
            return False
    
        return True
             
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes 
             if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("Valor do saque excede o limite da conta.")
        
        elif excedeu_saques:
            print("Número máximo de saques diários excedido.")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return  f"""\
            Agência: {self._agencia}
            C/C: {self._numero}
            Titular: {self._cliente.nome}
        """

class Historico:
    def __init__(self):
        self.transacoes = []

    @property
    def_transacoes(self):
        return self.transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append{
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        }

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self._valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self._valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == d:
            depositar(clientes)

        elif opcao == s:
            sacar(clientes)

        elif opcao == e:
            exibir_extrato(clientes)

        elif opcao == nu:
            criar_cliente(clientes)
        
        elif opcao == nc:
            numero_conta = len(contas) + 1
            criar_conta(clientes, contas, numero_conta)

        elif opcao == lc:
            listar_contas(contas)

        elif opcao == q:
            break

        else:
            print("Opção inválida. Tente novamente.")

def depositar(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    valor = float(input("Digite o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [
        cliente for cliente in clientes if cliente.cpf == cpf
    ]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente não possui contas.")
        return None
    
    # FIXME: Não permite cliente escolher a conta
    return

def sacar(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    valor = float(input("Digite o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print(f"Extrato da conta {conta.numero} - {conta.agencia}")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Nenhuma transação realizada."

    else:
        for transacao in transacoes:
            extrato += f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}\n"

    print(extrato)
    print(f"Saldo atual: R$ {conta.saldo:.2f}")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return
    
    conta = ContaCorrente.nova_conta(numero=numero_conta, cliente=cliente)
    contas.append(conta)
    cliente.contas.append(conta)

    print(f"Conta {conta.numero} criada com sucesso para {cliente.nome}.")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def criar_cliente(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Cliente já cadastrado.")
        return
    
    nome = input("Digite o nome do cliente: ")
    data_nascimento = input("Digite a data de nascimento do cliente (DD/MM/AAAA): ")
    endereco = input("Digite o endereço do cliente: ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print(f"Cliente {cliente.nome} cadastrado com sucesso.")

