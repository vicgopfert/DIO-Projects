""" 
========== DESAFIO SISTEMA BANCÁRIO SIMPLES =========

1. Não é necessário cadastro ou senha.                                       
2. O sistema deve permitir 3 saques diários com limite máximo de R$500,00 por saque.                                                                   
3. Mensagem de saldo insuficiente caso não haja para realizar saques.        
4. Todos os depósitos saques em uma variável para cada um e exibidos na operação de extrato.                                           
5. O saldo atual deve ser exibido após a listagem de extratos, utilizando o formato R$ xxx.xx, exemplo: 1500.45 == R$ 1500.45               

=====================================================

"""

def banco_deposito(saldo, extrato):
    try:
        deposit = float(input("Digite o valor de Depósito: R$"))
        if deposit <= 0:
            print("Valor de Depósito Inválido.")
        else:    
            saldo += deposit
            extrato.append(f"Depósito realizado no valor de R${deposit:.2f}")
            print(f"Depósito realizado com sucesso! Saldo Atual: R${saldo:.2f}")
    except ValueError:
        print("Valor inválido! Por favor, insira um número.")

    return saldo, extrato

def banco_saque(saldo, limite_saque, extrato, LIMITE_SAQUE_DIARIO, LIMITE_SAQUE_VALOR):
    try:
        saque = float(input(f"Digite o valor de Saque (Limite: R${LIMITE_SAQUE_VALOR} | Saques restantes: {limite_saque}) : R$"))    
        if saque <= 0:
            print("Valor de Saque Inválido.")
        elif saque > LIMITE_SAQUE_VALOR:
            print(f"Valor de saque acima do permitido. Limite é R${LIMITE_SAQUE_VALOR}.")
        elif limite_saque <= 0:
            print("Limite de saques diários excedido.")
        elif saque > saldo:
            print("Saldo insuficiente.")
        else:
            saldo -= saque
            limite_saque -= 1
            extrato.append(f"Saque realizado no valor de R${saque:.2f}")
            print(f"Saque realizado com sucesso! Saldo Atual: R${saldo:.2f}")
    except ValueError:
        print("Valor inválido! Por favor, insira um número.")
                        
    return saldo, limite_saque, extrato

def exibir_extrato(extrato, saldo):
    print("\n========== EXTRATO ==========")
    if not extrato:
        print("Nenhuma transação realizada no momento.")
    else:
        for transacao in extrato:
            print(transacao)
    print(f"\n- Saldo Atual = R${saldo:.2f}")
    print("=============================\n")

def main():
    saldo = 0
    limite_saque = 3
    extrato = []
    LIMITE_SAQUE_VALOR = 500 
    LIMITE_SAQUE_DIARIO = 3   
    
    while True:
        print(f"""
          \n========== SISTEMA BANCÁRIO ==========
        Saldo Atual = R${saldo:.2f}
    Limite de Saques Restantes = {limite_saque}
============= Operações: =============
1: Depósito
2: Saque
3: Extrato
4: Sair       
          """)
        menu = input("\nDigite o número da operação desejada: ")
        
        if menu == '1':
            saldo, extrato = banco_deposito(saldo, extrato)
        elif menu == '2':
            saldo, limite_saque, extrato = banco_saque(saldo, limite_saque, extrato, LIMITE_SAQUE_DIARIO, LIMITE_SAQUE_VALOR)
        elif menu == '3':
            exibir_extrato(extrato, saldo)
        elif menu == '4':
            print("Saindo do Sistema Bancário...")
            break            
        else:
            print("Opção Inválida. Tente novamente.")    

if __name__ == "__main__":
    main()