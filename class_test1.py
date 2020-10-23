#!/usr/bin/python3.6

class Account():
    def __init__(self, number, name):
        self.number=number
        self.name=name
        self.balance=0
    def deposit(self,amount):
        if (amount<=0):
            raise ValueError('must be positive')
        self.balance=self.balance+amount
    def withdraw(self,amount):
        if amount <= self.balance:
            self.balance=self.balance-amount
        else:
            raise RuntimeError('balance is not enough')

Jonathan=Account('123-333-98108','Jonathan')
print ("Jonathan account number is")
print (Jonathan.number)
Jonathan.deposit(100)
print ("Jonathan balance is")
print (Jonathan.balance)
Jonathan.withdraw(30)
print ("Jonathan balance is")
print (Jonathan.balance)

