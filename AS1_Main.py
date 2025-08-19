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
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

## CONSTANTS ##
inflation = 0.01  # 1% inflation rate

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

def dstatus(t, z):
    """
    This function models how the status of an employee changes with time.
    ds = alpha * Status * (1 - Status)
    alpha = alpha_R * R + alpha_T * T
    1 = R + T
    where R is the research level and T is the teaching level.
    0 <= R, T <= 1

    Arguments:
    t : float
        The time in years.
    z : list
        A list holding the career state of the employee.
    returns:
    dStatus : float
        The change in status of the employee at time t.
    """
    alpha_R = 0.1  # Research contribution to status change
    alpha_T = 0.05  # Teaching contribution to status change
    S = z[1]  # Status
    R = z[2]  # Research level

    return (alpha_R * R + alpha_T * (1 - R)) * S * (1 - S)

def dresearch(t, z):
    """
    This function models how the research level of an employee changes with time.
    dr = beta * (1 - R) * R
    Arguments:
    t : float
        The time in years.
    z : list
        A list holding the career state of the employee.
    returns:
    dResearch : float
        The change in research level of the employee at time t.
    """
    R = z[2]  # Research level
    beta = 0.05  # Research growth rate
    return beta * (1 - R) * R

def career_evolution(t, z):
    """
    This function describes the change in career state of an employee over time.
    Arguments:
    t : float
        The time in years.
    z : list
        A list holding the career state of the employee.
    returns:
    dz : list
        A list containing the changes in pay, status, and research level at time t.
    """
    dPay = dpay(t, z)
    dStatus = dstatus(t, z)
    dResearch = dresearch(t, z)
    
    return [dPay, dStatus, dResearch]

if __name__ == "__main__":

    t = np.linspace(0, 40, 100)  # Assume a 40-year career
    z = [50000, 0.5, 0.5]  # Initial state: [Pay, Status, Research]
    
    # Solve the system using solve_ivp
    solution = solve_ivp(career_evolution, [t[0], t[-1]], z, t_eval=t, method='RK45')

    # Extract the results
    pay = solution.y[0]
    status = solution.y[1]
    research = solution.y[2]

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(t, pay/100000, label="Pay (per 100k)")
    plt.plot(t, status, label="Status")
    plt.plot(t, research, label="Research")
    plt.xlabel("Time (years)")
    plt.ylabel("Values")
    plt.title("Career Evolution Over Time")
    plt.legend()
    plt.grid()
    plt.show()