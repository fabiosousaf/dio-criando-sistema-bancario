# "*" obriga o uso de argumentos nomeados (keyword only).
# Verifica se o valor excede saldo, limite ou número de saques.
# Se tudo estiver certo, atualiza saldo, extrato e numero_saques.

def sacar (*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques


    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1 

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

# O "/" obriga que os argumentos sejam passados por posição.
# Soma o valor ao saldo e registra no extrato, se o valor for válido.

def depositar(saldo, valor, extrato, /):

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"

    else:
        print("Operação falhou! O valor informado é invalido.")
    
    return saldo, extrato

# Recebe o saldo por posição e o extrato por nome.
# Mostra as movimentações feitas ou informa que nenhuma foi realizada.

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================") # Imprime um cabeçalho bonitinho para separar visualmente o extrato
    print("Não foram realizadas movimentações. " if not extrato else extrato) # Se extrato estiver vazio (""), imprime: "Não foram realizadas movimentações. Caso contrário, imprime o conteúdo da variável extrato, que contém o histórico de depósitos e saques." 
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("===========================================")

# Solicita nome, CPF, nascimento e endereço.
# Usa filtrar_usuario() para evitar CPFs duplicados.
# Adiciona o novo usuário à lista.

def criar_usuarios(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    cpf = " ".join(filter(str.isdigit, cpf)) # Remove caracteres não numéricos do CPF. #''.join(...) junta tudo de volta em uma única string.
    usuario = filtrar_usuario(cpf, usuarios) # "filtrar_usuario" é uma função que verifica se o CPF já existe na lista de usuários.	

    if usuario:
        print("Já existe um usuário com esse CPF.")
        return
    
    nome = input("Informe o nome completo: ")
    nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/UF): ")

    usuarios.append ({"nome": nome,"nascimento": nascimento, "cpf": cpf, "endereco": endereco}) # Adiciona o novo usuário à lista de usuários.
    print("Usuário criado com sucesso!")
















menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Operação falhou! O valor informado é invalido.")
    
    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        excedeu_saldo = valor > saldo

        excedeu_limite = valor > limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite")
        
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
        
        else:
            print("Operação falhou! O valor informado é inválido.")

    
    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações. " if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("===========================================")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
