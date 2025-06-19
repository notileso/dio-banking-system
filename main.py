menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=> """


def convert_and_valid_value(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def deposit(balance: float, value: float, statement: str) -> tuple[float, str]:
    if value > 0:
        balance += value
        statement += f"Depósito: R$ {value:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return balance, statement


def withdraw(
    *,
    balance: float,
    value: float,
    statement: str,
    limit: float,
    number_of_withdrawals: int,
    withdrawal_limit: int,
) -> tuple[float, str, int]:
    exceeded_balance = value > balance
    exceeded_limit = value > limit
    exceeded_withdrawals = number_of_withdrawals >= withdrawal_limit

    if exceeded_balance:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif exceeded_limit:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif exceeded_withdrawals:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif value > 0:
        balance -= value
        statement += f"Saque: R$ {value:.2f}\n"
        number_of_withdrawals += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return balance, statement, number_of_withdrawals


def display_statement(balance: float, statement: str) -> None:
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not statement else statement)
    print(f"\nSaldo: R$ {balance:.2f}")
    print("==========================================")


def main():
    balance = 0
    limit = 500
    statement = ""
    number_of_withdrawals = 0
    WITHDRAWAL_LIMIT = 3
    while True:

        menu_option = input(menu)

        if menu_option == "d":
            value = input("Informe o valor do depósito: ")
            value = convert_and_valid_value(value)

            if value is None:
                print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
                continue

            balance, statement = deposit(balance, value, statement)

        elif menu_option == "s":
            value = input("Informe o valor do saque: ")
            value = convert_and_valid_value(value)

            if value is None:
                print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
                continue

            balance, statement, number_of_withdrawals = withdraw(
                balance=balance,
                value=value,
                statement=statement,
                limit=limit,
                number_of_withdrawals=number_of_withdrawals,
                withdrawal_limit=WITHDRAWAL_LIMIT,
            )

        elif menu_option == "e":
            display_statement(balance, statement)
        elif menu_option == "q":
            exit()

if __name__ == "__main__":
    main()