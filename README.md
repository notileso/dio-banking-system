# Sistema Bancário em Python
Este projeto é a resolução do desafio "Criando um sistema bancário" do bootcamp Santander 2025 - Back-End com Python da DIO.

## 🎯 Objetivo
O objetivo era criar um sistema bancário simples em Python, com as funcionalidades de depósito, saque e extrato. A primeira versão do sistema foi desenvolvida para um único usuário, sem a necessidade de identificação de agência ou conta.

## 💻 Desafio
Fomos contratados por um grande banco para desenvolver seu novo sistema em Python para modernizar suas operações. A primeira versão deveria implementar as três operações básicas:

### Depósito

### Saque

### Extrato

## Regras de Negócio
### Operação de Depósito
- Deve ser possível depositar apenas valores positivos.

- Todos os depósitos devem ser armazenados e exibidos na operação de extrato.

### Operação de Saque
- O sistema permite um máximo de 3 saques diários.

- Cada saque tem um limite máximo de R$ 500,00.

- Caso o saldo seja insuficiente, o sistema deve exibir uma mensagem de erro.

- Todos os saques devem ser armazenados e exibidos na operação de extrato.

### Operação de Extrato
- Deve listar todos os depósitos e saques realizados.

- Ao final da listagem, deve exibir o saldo atual da conta.

- Os valores devem ser formatados como R$ xxx.xx.

- Se não houver movimentações, deve exibir a mensagem: "Não foram realizadas movimentações.".