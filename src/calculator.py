#  Copyright (c) 2024.  @Author: Aashish Mahajan
#

class Calculator:
    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y

    def display(self, x):
        print("this is a formatted way to show un-used method: {test}".format(test=x))
