#!/usr/bin/python3.6

class Animal():
    def __init__(self,name,age):
        self.name=name
        self.age=age

animal_1=Animal("dog","8")
print ("Animal 1 is")
print (animal_1.name)
print ("Animal 1 age is")
print (animal_1.age)
