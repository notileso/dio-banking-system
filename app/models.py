from abc import ABC, abstractmethod
from datetime import datetime, UTC
from collections.abc import Generator


class Customer:
    """
    Cliente
    """

    def __init__(self, address: str, name: str):
        self.address = address
        self.name = name
        self.accounts: list["Account"] = []

    def add_account(self, account: "Account"):
        self.accounts.append(account)

    def carry_out_transaction(self, account: "Account", transaction: "Transaction"):
        if len(account.history.todays_transactions()) >= 10:
            print("\n@@@ Você excedeu o número máximo de transações diárias. @@@")
        transaction.register(account)


class NaturalPerson(Customer):
    """
    Pessoa Física
    """

    def __init__(
        self, document_number: str, name: str, birth_date: datetime, address: str
    ):
        super().__init__(address, name)
        self.document_number = document_number
        self.birth_date = birth_date


class Account:
    """
    Conta
    """

    _agency: str = "0001"

    def __init__(self, number: int, customer: Customer, balance: float = 0.0):
        self._number = number
        self._customer = customer
        self._balance = balance
        self._history = History()

    @property
    def agency(self):
        return self._agency

    @property
    def number(self):
        return self._number

    @property
    def customer(self):
        return self._customer

    @property
    def history(self):
        return self._history

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float):
        self._balance = value

    def deposit(self, value: float) -> bool:
        if value <= 0:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False
        self._balance += value
        print("\n=== Depósito realizado com sucesso! ===")
        return True

    def withdraw(self, value: float) -> bool:
        exceeded_balance = value > self.balance
        if exceeded_balance:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif value > 0:
            self.balance -= value
            print("\n=== Saque realizado com sucesso! ===")

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    @classmethod
    def add_account(cls, customer: Customer, number: int):
        customer.accounts.append(cls(number, customer))

    def __str__(self) -> str:
        return f"""
            Agência:\t{self.agency}
            C/C:\t\t{self.number}
            Titular:\t{self.customer.name}
        """


class CheckingAccount(Account):
    """
    Conta Corrente
    """

    def __init__(
        self,
        number: int,
        customer: Customer,
        balance: float = 0.0,
        limit: float = 100.0,
        limit_withdrawals: int = 3,
    ):
        self._number = number
        self._customer = customer
        self._balance = balance
        self._history = History()
        self.limit = limit
        self._limit_withdrawals = limit_withdrawals

    def withdraw(self, value: float) -> bool:
        number_of_withdrawals = len(
            [
                transaction
                for transaction in self.history.transactions
                if isinstance(transaction, Withdraw)
            ]
        )
        exceeded_withdrawals = number_of_withdrawals >= self._limit_withdrawals
        exceeded_limit = value > self.limit
        if exceeded_withdrawals:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif exceeded_limit:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        return super().withdraw(value)

class AccountIterator:
    def __init__(self, accounts: list[Account | CheckingAccount]):
        self._accounts = accounts
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._accounts):
            raise StopIteration
        account = self._accounts[self._index]
        self._index += 1
        return account

class Transaction(ABC):
    """
    Transação
    """

    _date: datetime
    _value: float

    def __init__(self, value: float):
        self._value = value
        self._date = datetime.now(UTC)

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def value(self) -> float:
        return self._value

    @abstractmethod
    def register(self, account: Account):
        pass


class Deposit(Transaction):
    def register(self, account: Account):
        if account.deposit(self.value):
            account.history.add_transaction(self)


class Withdraw(Transaction):
    def register(self, account: Account):
        if account.withdraw(self.value):
            account.history.add_transaction(self)


class History:
    """
    Histórico
    """

    _transactions: list[Transaction] = []

    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction: Transaction):
        self._transactions.append(transaction)

    def generate_report(
        self, type_transaction: type[Transaction] | None = None
    ) -> Generator[Transaction, None, None]:
        for transaction in self._transactions:
            if not type_transaction or isinstance(transaction, type_transaction):
                yield transaction

    def todays_transactions(self) -> list[Transaction]:
        today = datetime.now(UTC).date()
        return [
            transaction
            for transaction in self.transactions
            if transaction.date.date() == today
        ]