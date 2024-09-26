""" 
========== DESAFIO SISTEMA BANCÁRIO COM USUÁRIOS =========

1. Não é necessário cadastro ou senha.                                                                                                             
2. O sistema deve permitir 3 saques diários com limite máximo de R$500,00 por saque.                                                               
3. Mensagem de saldo insuficiente caso não haja para realizar saques.                                                                              
4. Todos os depósitos saques em uma variável para cada um e exibidos na operação de extrato.                                                       
5. O saldo atual deve ser exibido após a listagem de extratos, utilizando o formato R$ xxx.xx, exemplo: 1500.45 == R$ 1500.45                      
6. Estabelecer um limite de 10 transações diárias para uma conta, se o usuário ultrapassar o limite do dia, isso deve ser informado ao usuário      
7. Mostrar no extrato a data e hora de todas as transações.                  
8. Função para criar usuário e criar conta corrente (vincular com o usuário)
9. Função de listar usuários e listar contas                                  
=====================================================

"""

from datetime import datetime

# Variável global para rastrear o número sequencial das contas
numero_conta_global = 1

# Função para registrar um novo usuário
def registrar_usuario(users):
    print("\n==== Cadastro de Usuário ====")
    
    # Loop para garantir que o CPF inserido é válido e não está cadastrado
    while True:
        cpf = input("Digite seu CPF (somente números): ").strip()
        if cpf in users:
            print("Este CPF já está cadastrado.")
        elif not cpf.isdigit():  # Verifica se o CPF contém apenas números
            print("CPF Inválido. Por favor, insira um CPF válido.")
        else:
            break

    # Loop para garantir que os dados são válidos e formatados corretamente
    while True:
        try:
            nome = input("Digite seu Nome Completo: ")
            data_nasc = input("Digite sua data de nascimento (DD/MM/AAAA): ")
            data_nascimento = datetime.strptime(data_nasc, "%d/%m/%Y")  # Verifica o formato da data
            endereco = input("Digite seu endereço (Rua, Nº - Bairro - Cidade/Sigla Estado): ")
            break  # Quebra o loop após entrada válida
        except ValueError:
            print("Data de nascimento em formato inválido. Tente novamente.")

    # Registra o usuário com as informações fornecidas
    users[cpf] = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'endereco': endereco,
        'saldo': 0.0,
        'limite_saque': 3,  # Limite de saques diários
        'extratos': [],  # Histórico de transações
        'limite_saque_valor': 500,  # Valor máximo por saque
        'limite_transacoes': 10,  # Limite de transações por dia
        'transacoes_hoje': 0,  # Contador de transações do dia
        'ultima_data': datetime.now().date(),  # Última data de transações
        'contas': []  # Lista de contas associadas ao usuário
    }

    # Registra a primeira conta automaticamente
    registrar_conta(users, cpf)

    print(f"Usuário '{nome.split()[0]}' registrado com sucesso!\n")

# Função para registrar uma nova conta bancária para o usuário
def registrar_conta(users, cpf):
    global numero_conta_global  # Usar a variável global para números de contas
    user_data = users[cpf]
    
    # Cria uma nova conta com agência fixa e número de conta sequencial
    conta = {
        'agencia': "0001",
        'numero_conta': numero_conta_global,
        'usuario': user_data['nome']
    }
    
    # Adiciona a nova conta à lista de contas do usuário
    user_data['contas'].append(conta)
    print(f"Conta registrada com sucesso! Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}.")
    
    numero_conta_global += 1  # Incrementa o número global da conta para o próximo usuário

# Função de login de usuário com CPF
def login_usuario(users):
    print("\n==== Login de Usuário ====")
    cpf = input("Digite seu CPF (somente números): ").strip()

    # Verifica se o CPF está cadastrado no sistema
    if cpf not in users:
        print("CPF de usuário não encontrado. Por favor, registre-se primeiro.\n")
        return None, None

    print(f"Login bem-sucedido! Bem-vindo, {users[cpf]['nome'].split()[0]}.\n")
    return cpf, users[cpf]

# Atualiza o limite diário de transações e saques, resetando no início de um novo dia
def atualizar_limite_diario(user_data):
    if datetime.now().date() != user_data['ultima_data']:
        user_data['limite_saque'] = 3
        user_data['transacoes_hoje'] = 0
        user_data['ultima_data'] = datetime.now().date()
    return user_data

# Função para depósito de dinheiro
def banco_deposito(user_data):
    # Verifica se o usuário atingiu o limite diário de transações
    if user_data['transacoes_hoje'] >= user_data['limite_transacoes']:
        print("Limite de transações diárias excedido. Tente novamente amanhã.")
        return
    
    try:
        deposit = float(input("Digite o valor de Depósito: R$"))
        if deposit > 0:
            user_data['saldo'] += deposit  # Atualiza o saldo do usuário
            user_data['extratos'].append(f"{datetime.now():%d/%m/%Y %H:%M:%S} - Depósito: R${deposit:.2f}")  # Registra o extrato
            user_data['transacoes_hoje'] += 1  # Incrementa o contador de transações do dia
            print(f"Depósito realizado com sucesso! Saldo Atual: R${user_data['saldo']:.2f}")
        else:
            print("Valor de Depósito Inválido.")
    except ValueError:
        print("Valor inválido! Por favor, insira um número.")

# Função para saque de dinheiro
def banco_saque(user_data):
    # Verifica se o usuário atingiu o limite diário de transações
    if user_data['transacoes_hoje'] >= user_data['limite_transacoes']:
        print("Limite de transações diárias excedido. Tente novamente amanhã.")
        return

    try:
        saque = float(input(f"Digite o valor de Saque (Máximo por saque: R$500 | Saques Restantes: {user_data['limite_saque']}): R$"))
        
        # Verifica se o saque é válido e se há saldo disponível
        if 0 < saque <= 500 and user_data['limite_saque'] > 0 and saque <= user_data['saldo']:
            user_data['saldo'] -= saque  # Deduz o valor do saldo
            user_data['limite_saque'] -= 1  # Diminui o número de saques restantes no dia
            user_data['extratos'].append(f"{datetime.now():%d/%m/%Y %H:%M:%S} - Saque: R${saque:.2f}")
            user_data['transacoes_hoje'] += 1  # Incrementa o contador de transações do dia
            print(f"Saque realizado com sucesso! Saldo Atual: R${user_data['saldo']:.2f}\n")
        else:
            print("Valor de saque inválido ou limite excedido.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número válido.")

# Função para exibir o extrato bancário do usuário
def banco_extrato(user_data):
    print("\n========== EXTRATO ==========")
    if user_data['extratos']:
        print("\n".join(user_data['extratos']))  # Exibe todas as transações registradas
    else:
        print("Nenhuma transação realizada no momento.")
    print(f"\n- Saldo Atual = R${user_data['saldo']:.2f}")
    print("=============================\n")

# Função para visualizar todos os usuários cadastrados e suas informações
def visualizar_usuarios(users):
    print("\n========== Usuários Cadastrados ==========")
    if users:
        for cpf, dados in users.items():
            # Exibe as informações do usuário
            print(f"Agência: 0001")
            print(f"CPF: {cpf}")
            print(f"Nome: {dados['nome']}")
            print(f"Data de Nascimento: {dados['data_nascimento'].strftime('%d/%m/%Y')}")
            print(f"Endereço: {dados['endereco']}")
            print(f"Saldo: R${dados['saldo']:.2f}")
            print(f"Limite de Saques Restantes: {dados['limite_saque']}")
            print(f"Transações Realizadas Hoje: {dados['transacoes_hoje']}")
            print(f"Lista de Contas Registradas: {' | '.join([f'{conta['numero_conta']}' for conta in dados['contas']]) if dados['contas'] else 'Nenhuma'}")
            print("==========================================")
    else:
        print("Nenhum usuário cadastrado.")

# Função principal que inicia o sistema bancário e controla o fluxo do programa
def main():
    users = {}
    user_logado = None

    # Loop principal do sistema
    while True:
        if user_logado is None:
            print("""\n
    ========== SISTEMA BANCÁRIO ========== 
    1: Registrar 
    2: Login 
    3: Visualizar Usuários 
    4: Sair 
    ====================================== 
            """)
            escolha = input("Digite o número da operação desejada: ").strip()

            if escolha == '1':
                registrar_usuario(users)
            elif escolha == '2':
                cpf, user_data = login_usuario(users)
                if cpf:
                    user_logado = cpf
            elif escolha == '3':
                visualizar_usuarios(users)
                input("Pressione Enter para continuar...")
            elif escolha == '4':
                print("Saindo do Sistema Bancário. Até logo!")
                break
            else:
                print("Opção Inválida. Tente novamente.\n")
        else:
            user_data_logado = atualizar_limite_diario(users[user_logado])

            if not user_data_logado['contas']:
                print("Você precisa criar uma conta para realizar transações.")
                input("Pressione Enter para voltar ao menu principal.")
                user_logado = None  # Volta ao menu principal
                continue

            print(f"""\n
    ========== SISTEMA BANCÁRIO ========== 
    Saldo Atual = R${user_data_logado['saldo']:.2f}
    Limite de Saques Restantes = {user_data_logado['limite_saque']}
    Transações Restantes Hoje = {user_data_logado['limite_transacoes'] - user_data_logado['transacoes_hoje']}
    ============= Operações: ============= 
    1: Depósito 
    2: Saque 
    3: Extrato 
    4: Registrar Nova Conta 
    5: Sair       
    """)
            menu = input("\nDigite o número da operação desejada: ")
        
            if menu == '1':
                banco_deposito(user_data_logado)
            elif menu == '2':
                banco_saque(user_data_logado)
            elif menu == '3':
                banco_extrato(user_data_logado)
                input("Pressione Enter para voltar ao menu principal.")
            elif menu == '4':
                registrar_conta(users, user_logado)
            elif menu == '5':
                print(f"Usuário '{user_logado}' deslogado com sucesso.\n")
                user_logado = None
            else:
                print("Opção Inválida. Tente novamente.\n")

if __name__ == "__main__":
   main()










