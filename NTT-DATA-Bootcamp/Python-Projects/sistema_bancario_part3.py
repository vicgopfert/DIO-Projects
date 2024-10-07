from datetime import datetime

# Classe Transacao
class Transacao:
    def __init__(self, valor: float):
        self.valor = valor
        self.data = datetime.now()

    def registrar(self, conta):
        pass  # A implementação específica será nas subclasses Depósito e Saque


# Subclasse Depósito que herda de Transacao
class Deposito(Transacao):
    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)
        conta.transacoes_hoje += 1
        print(f"Depósito de R${self.valor:.2f} realizado com sucesso!")


# Subclasse Saque que herda de Transacao
class Saque(Transacao):
    def registrar(self, conta):
        if conta.saldo >= self.valor and conta.limite_saque > 0 and conta.transacoes_hoje < conta.limite_transacoes and self.valor <= 500:
            conta.saldo -= self.valor
            conta.limite_saque -= 1
            conta.transacoes_hoje += 1
            conta.historico.adicionar_transacao(self)
            print(f"Saque de R${self.valor:.2f} realizado com sucesso!")
        else:
            print("Saque não realizado. Verifique saldo, limite de saque ou número de transações diárias.")


# Classe Historico para registrar as transações
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(f"{transacao.data:%d/%m/%Y %H:%M:%S} - {type(transacao).__name__}: R${transacao.valor:.2f}")


# Classe Conta
class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()
        self.limite_saque = 3  # Limite de saques diários
        self.limite_transacoes = 10  # Limite de transações diárias
        self.transacoes_hoje = 0
    
    def saldo_atual(self):
        return self.saldo

    def sacar(self, valor):
        saque = Saque(valor)
        saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        deposito.registrar(self)


# Classe Cliente
class Cliente:
    def __init__(self, nome, endereco, data_nascimento, cpf):
        self.nome = nome
        self.endereco = endereco
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


# Subclasse PessoaFisica que herda de Cliente
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(nome, endereco, data_nascimento, cpf)


# Função para registrar um novo cliente
def registrar_cliente():
    print("\n==== Cadastro de Cliente ====")
    cpf = input("Digite seu CPF (somente números): ").strip()
    if not cpf.isdigit():
        print("CPF Inválido. Tente Novamente.")
    else:
        try:
            nome = input("Digite seu Nome Completo: ")
            data_nasc = input("Digite sua data de nascimento (DD/MM/AAAA): ")
            data_nascimento = datetime.strptime(data_nasc, "%d/%m/%Y")
            endereco = input("Digite seu endereço: ")

            cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
            conta = Conta(cliente, numero_conta_global)
            cliente.adicionar_conta(conta)

            print(f"Cliente {nome} registrado com sucesso!")
            return cliente
        except ValueError:
            print("Data de nascimento em formato inválido. Tente novamente.")


# Função para exibir extrato bancário
def exibir_extrato(conta):
    print("\n===== EXTRATO =====")
    for transacao in conta.historico.transacoes:
        print(transacao)
    print(f"\nSaldo atual: R${conta.saldo_atual():.2f}")
    print("===================")


# Função de login com CPF
def login(clientes):
    cpf = input("Digite seu CPF para login: ").strip()
    cliente = next((c for c in clientes if c.cpf == cpf), None)
    if cliente:
        print(f"Bem-vindo(a), {cliente.nome}!")
        return cliente
    elif not cpf.isdigit():
        print("CPF Inválido.")
    else:
        print("Cliente não encontrado.")
        return None


# Função para exibir lista de todas as contas no banco
def exibir_lista_contas(clientes):
    print("\n===== LISTA DE CONTAS DO BANCO =====")
    for cliente in clientes:
        print(f"\n\n----- CPF: {cliente.cpf} -----")
        print(f"Nome: {cliente.nome}")
        print(f"Data de Nascimento: {cliente.data_nascimento.strftime('%d/%m/%Y')}")
        print(f"Endereço: {cliente.endereco}")
        if cliente.contas:
            for conta in cliente.contas:
                print("==========================================")
                print(f"Agência: {conta.agencia}")
                print(f"Número da Conta: {conta.numero}")
                print(f"Saldo: R${conta.saldo_atual():.2f}")
                print(f"Limite de Saques Restantes: {conta.limite_saque}")
                print(f"Transações Realizadas Hoje: {conta.transacoes_hoje}")
        else:
            print("Nenhuma conta registrada.")

    print("==========================================")


# Função para registrar uma nova conta para um cliente logado
def registrar_nova_conta(cliente):
    global numero_conta_global
    nova_conta = Conta(cliente, numero_conta_global)
    cliente.adicionar_conta(nova_conta)
    print(f"Nova conta registrada com sucesso! Nº da Conta: {nova_conta.numero}")
    numero_conta_global += 1


# Função principal para gerenciar o fluxo do sistema bancário
def main():
    clientes = []
    global numero_conta_global
    numero_conta_global = 1  # Variável global para controle de contas

    while True:
        print("\n========== SISTEMA BANCÁRIO ==========")
        print("1: Registrar Cliente")
        print("2: Login")
        print("3: Visualizar Usuários")
        print("4: Sair")
        escolha = input("\nEscolha uma opção: ")

        if escolha == '1':
            cliente = registrar_cliente()
            clientes.append(cliente)
            numero_conta_global += 1
        elif escolha == '2':
            cliente_logado = login(clientes)
            if cliente_logado:
                menu_cliente(cliente_logado)
        elif escolha == '3':
            exibir_lista_contas(clientes)
        elif escolha == '4':
            print("Saindo do sistema bancário. Até logo!")
            break
        else:
            print("Opção inválida.")


# Função de menu para o cliente após login
def menu_cliente(cliente_logado):
    while True:
        conta = cliente_logado.contas[0]  # Acessando a primeira conta
        print("\n===== Informações da Conta =====")
        print(f"Saldo Atual: R${conta.saldo_atual():.2f}")
        print(f"Limite de Saques Restantes: {conta.limite_saque}")
        print(f"Transações Restantes Hoje: {conta.limite_transacoes - conta.transacoes_hoje}")

        print("\n===== Menu do Cliente =====")
        print("1: Depósito")
        print("2: Saque")
        print("3: Extrato")
        print("4: Registrar Nova Conta")
        print("5: Sair")
        escolha = input("\nEscolha uma opção: ")

        if escolha == '1':
            valor = float(input("Digite o valor do depósito: R$"))
            if valor > 0:
                conta.depositar(valor)  # Depósito na conta do cliente
            else:
                print("Valor de Depósito Inválido. Tente Novamente.")
        elif escolha == '2':
            valor = float(input(f"Digite o valor de Saque (Máximo por saque: R$500 | Saques Restantes: {conta.limite_saque}): R$"))
            if valor > 0:
                conta.sacar(valor)  # Saque na conta do cliente
            else:
                print("Valor de Saque Inválido. Tente Novamente.")
        elif escolha == '3':
            exibir_extrato(conta)  # Exibe extrato da conta do cliente
        elif escolha == '4':
            registrar_nova_conta(cliente_logado)  # Registra uma nova conta para o cliente logado
        elif escolha == '5':
            print("Saindo do menu do cliente.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()

