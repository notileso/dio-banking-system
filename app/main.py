import textwrap
from typing import TypedDict
from app.models import *

class User(TypedDict):
    document_number: str
    name: str
    birth_date: str
    address: str

def menu():
    menu = """
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo Cliente
    [q] Sair
    => """
    return input(textwrap.dedent(menu))


def convert_and_valid_value(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None

def filter_customer(document_number: str, customers: list[NaturalPerson]) -> Customer | None:
    return next((customer for customer in customers if customer.document_number == document_number), None)

def get_customer_account(customer: NaturalPerson | Customer):
    if not customer.accounts:
        print("\n@@@ Cliente não possui conta! @@@")
        return
    return customer.accounts[0]

def request_customer_data(customers: list[NaturalPerson]):
    document_number = input("Informe o CPF (somente número): ")
    customer = filter_customer(document_number, customers)
    if not customer:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    return customer

def deposit(customers: list[NaturalPerson]):
    if not (customer:=request_customer_data(customers)): return
    value = input("Informe o valor do depósito: ")
    value = convert_and_valid_value(value)
    if not value:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return
    transaction = Deposit(value)
    if not (account:=get_customer_account(customer)): return
    customer.carry_out_transaction(account, transaction)
    print("\n=== Depósito realizado com sucesso! ===")

def withdraw(
    customers: list[NaturalPerson],
):
    if not (customer:=request_customer_data(customers)): return

    if not (account:=get_customer_account(customer)): return

    value = float(input("Informe o valor do saque: "))
    transaction = Withdraw(value)
    customer.carry_out_transaction(account, transaction)
    print("\n=== Saque realizado com sucesso! ===")


def display_statement(customers: list[NaturalPerson]):
    if not (customer:=request_customer_data(customers)): return
    if not (account:=get_customer_account(customer)): return
    print("\n================ EXTRATO ================")
    transactions = account.history.transactions
    if not transactions:
        print("Não foram realizadas movimentações.")
    else:
        for transaction in transactions:
            print(f"{transaction.date}\t{transaction.__class__.__name__}\t{transaction.value:.2f}")
    print(f"\nSaldo:\t\t{account.balance:.2f}")
    print("==========================================")


def create_account(number: int, customers: list[NaturalPerson]):
    if not (customer:=request_customer_data(customers)): return
    CheckingAccount.add_account(customer, number)
    print("\n=== Conta criada com sucesso! ===")


def list_accounts(accounts: list[Account]):
    for account in accounts:
        print("=" * 100)
        print(textwrap.dedent(str(account)))


def create_customer(customers: list[NaturalPerson]):
    document_number = input("Informe o CPF (somente número): ")
    customer = filter_customer(document_number, customers)
    if customer:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return
    name = input("Informe o nome completo: ")
    _birth_date = input("Informe a data de nascimento (dd-mm-aaaa): ")
    birth_date = datetime.strptime(_birth_date, "%d-%m-%Y")
    address = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    customers.append(NaturalPerson(document_number, name, birth_date, address))
    print("=== Cliente criado com sucesso! ===")


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



def main():
    customers: list[NaturalPerson] = []
    accounts: list[Account] = []
    while True:

        menu_option = menu()

        if menu_option == "d":
            deposit(customers)
        elif menu_option == "s":
            withdraw(customers)

        elif menu_option == "e":
            display_statement(customers)

        elif menu_option == "nu":
            create_customer(customers)

        elif menu_option == "nc":
            create_account(len(accounts) + 1, customers)
        
        elif menu_option == "lc":
            list_accounts(accounts)

        elif menu_option == "q":
            exit()

if __name__ == "__main__":
    main()