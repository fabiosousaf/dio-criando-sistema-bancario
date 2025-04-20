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
    cpf = ' '.join(filter(str.isdigit, cpf)) # Remove caracteres não numéricos do CPF. #''.join(...) junta tudo de volta em uma única string.
    usuario = filtrar_usuario(cpf, usuarios) # "filtrar_usuario" é uma função que verifica se o CPF já existe na lista de usuários.	

    if usuario:
        print("Já existe um usuário com esse CPF.")
        return
    
    nome = input("Informe o nome completo: ")
    nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/UF): ")

    usuarios.append ({"nome": nome,"nascimento": nascimento, "cpf": cpf, "endereco": endereco}) # Adiciona o novo usuário à lista de usuários.
    print("Usuário criado com sucesso!")

# Função auxiliar para buscar um usuário pelo CPF.

def filtrar_usuario(cpf, usuarios):
    # Para cada usuario dentro da lista usuarios, verifique se o usuario["cpf"] é igual ao CPF que recebemos como argumento.
    # Se for, coloque esse usuário na lista usuarios_filtrados
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf] # Filtra a lista de usuários para encontrar o CPF informado.
    return usuarios_filtrados[0] if usuarios_filtrados else None # Retorna o primeiro usuário encontrado ou None se não houver correspondência.

# for usuario in usuarios: Aqui o Python está percorrendo cada item da lista usuarios, e chamando cada item de usuario dentro do laço.
# if usuario["cpf"] == cpf: Para cada usuario, o Python verifica se o valor da chave "cpf" desse dicionário é igual ao cpf que a pessoa digitou.
# Se bater: O usuario (ou seja, o dicionário inteiro daquela pessoa) é adicionado na nova lista usuarios_filtrados.

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário:")
    usuarios = filtrar_usuario(cpf,usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("Usuário não encontrado. Conta não criada.")

# contas → É a lista completa de todas as contas bancárias (uma lista de dicionários).
# conta → É apenas um elemento da lista contas (um dicionário individual).
# Durante o loop for conta in contas, a cada iteração:
# Na 1ª iteração: conta = {'agencia': '0001', 'numero_conta': '1234-5', ...}
# Na 2ª iteração: conta = {'agencia': '0001', 'numero_conta': '5678-9', ...}

def listar_contas(contas):
    for conta in contas:
        print(f"\nAgência: {conta['agencia']}")
        print(f"C/C: {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']['nome']}")

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
[nu] Novo usuário
[nc] Nova conta
[lc] Listar contas

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
usuarios = []
contas = []


while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = depositar(saldo, valor, extrato)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato, numero_saques = sacar(
            saldo = saldo,
            valor = valor,
            extrato = extrato,
            limite = limite,
            numero_saques = numero_saques,
            limite_saques = LIMITE_SAQUES
        )

    elif opcao == "e":
        exibir_extrato(saldo, extrato=extrato)

    elif opcao == "nu":
        criar_usuarios(usuarios)

    elif opcao == "nc":
        numero_conta = len(contas) + 1
        conta = criar_conta("0001", numero_conta, usuarios)
        if conta:
            contas.append(conta)

    elif opcao == "lc":
        listar_contas(contas)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")