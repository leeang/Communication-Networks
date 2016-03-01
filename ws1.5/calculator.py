# -*- coding: utf-8 -*-

import sys

while 1:
    option = input('input option')
    if option == 1:
        num1 = input('add 1st')
        num2 = input('add 2nd')
        print num1 + num2
    elif option == 2:
        num1 = input('subtract 1st')
        num2 = input('subtract 2nd')
        print num1 - num2
    elif option == 3:
        num1 = input('multiply 1st')
        num2 = input('multiply 2nd')
        print num1 * num2
    elif option == 4:
        num1 = input('divide 1st')
        num2 = input('divide 2nd')
        print num1 / num2
    elif option == 5:
        sys.exit();
