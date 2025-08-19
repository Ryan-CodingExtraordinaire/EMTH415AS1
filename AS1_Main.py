"""
Author: Ryan, Connor, Steven
Date: Now
Description: Code goes here to do the stuff
Notes:
The convention will be to define the career state (z) as an array of the form:
[Pay, Status, Research]
which covers the three main ODEs we will be working with. 
"""
import numpy as np
import matplotlib.pyplot as plt

## CONSTANTS ##
inflation = 0.01  # 2% inflation rate

## FUNCTIONS ##
def dpay(t, z):
    """
    This function models how the amount of pay recieved by an employee changes with time.
    Arguments:
    t : float
        The time in years.
    z : list
        A list holding the career state of the employee.
    returns:
    dPay : float
        The change in pay received by the employee at time t.
    """
    return inflation * z[0] + 0.03 * z[1] * z[0]




if __name__ == "__main__":
    #Put test sequence here.