import textwrap
from typing import TypedDict

class User(TypedDict):
    document_number: str
    name: str
    birth_date: str
    address: str

class Account(TypedDict):
    agency: str
    number: str
    user: User




def menu():
    menu = """
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q] Sair
    => """
    return input(textwrap.dedent(menu))


def convert_and_valid_value(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def deposit(balance: float, value: float, statement: str, /) -> tuple[float, str]:
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

def filter_user(document_number: str, users: list[User]) -> User | None:
    return next((user for user in users if user["document_number"] == document_number), None)



def create_user(users: list[User]):
    document_number = input("Informe o CPF (somente número): ")
    user = filter_user(document_number, users)

    if user:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return
    
    name = input("Informe o nome completo: ")
    birth_date = input("Informe a data de nascimento (dd-mm-aaaa): ")
    address = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    users.append(
        {
            "name": name,
            "document_number": document_number,
            "birth_date": birth_date,
            "address": address,
        }
    )

    print("=== Usuário criado com sucesso! ===")

def create_account(agency: str, number: str, users: list[User]) -> Account | None:
    document_number = input("Informe o CPF (somente número): ")
    user = filter_user(document_number, users)

    if user:
        print("\n=== Conta criada com sucesso! ===")
        return {
            "agency": agency,
            "number": number,
            "user": user,
        }
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

def list_accounts(accounts: list[Account]):
    for account in accounts:
        print("=" * 100)
        print(f"Agência:\t{account['agency']}")
        print(f"C/C:\t\t{account['number']}")
        print(f"Titular:\t{account['user']['name']}")
        print("=" * 100)


def main():
    users: list[User] = []

    accounts: list[Account] = []
    AGENCY = "0001"

    balance = 0
    limit = 500
    statement = ""
    number_of_withdrawals = 0
    WITHDRAWAL_LIMIT = 3
    while True:

        menu_option = menu()

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

        elif menu_option == "nu":
            create_user(users)

        elif menu_option == "nc":
            number = str(len(accounts) + 1)
            account = create_account(agency=AGENCY, number=number,users=users)

            if account:
                accounts.append(account)
        
        elif menu_option == "lc":
            list_accounts(accounts)

        elif menu_option == "q":
            exit()

if __name__ == "__main__":
    main()