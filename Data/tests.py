from django.test import TestCase
import subprocess


# Create your tests here.
def show():
    a= [1, 2, 4, 5, 6]
    b = [3, 5, 6]
    return a, b

a = show()
print(a[0])
print(a[1])

