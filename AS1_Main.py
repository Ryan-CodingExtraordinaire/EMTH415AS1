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
#inflation = 0.01  # 1% inflation rate [I don't know if this is the right value]
# inflation equals some random number between -2 and 10%:



## FUNCTIONS ##
def dpay(t, z):
    """
    This function models how the amount of pay recieved by an academic changes with time.
    Arguments:
    t : float
        The time in years.
    z : list
        A list holding the career state of the academic.
    returns:
    dPay : float
        The change in pay received by the academic at time t.
    """

    inflation = np.random.uniform(0.01, 0.06)
    max_pay = 500000
    pay_limit = (max_pay - z[0])/max_pay
    return (inflation * z[0] + 0.03 * z[1] * z[0]) * pay_limit

def dstatus(t, z):
    """
    This function models how the status of an academic changes with time.
    ds = alpha * Status * (1 - Status)
    alpha = alpha_R * R + alpha_T * T
    1 = R + T
    where R is the research level and T is the teaching level.
    0 <= R, T <= 1

    Arguments:
    t : float
        The time in years.
    z : list
        A list holding the career state of the academic.
    returns:
    dStatus : float
        The change in status of the academic at time t.
    """
    alpha_R = np.random.normal(0.2, 0.1) # Research contribution to status change
    alpha_T = np.random.normal(0.05, 0.01) # Teaching contribution to status change
    S = z[1]  # Status
    R = z[2]  # Research level

    return (alpha_R * R + alpha_T * (1 - R)) * S * (1 - S)

def dresearch(t, z):
    """
    This function models how the research level of an academic changes with time.
    dr = beta * (1 - R) * R
    Arguments:
    t : float
        The time in years.
    z : list
        A list holding the career state of the academic.
    returns:
    dResearch : float
        The change in research level of the academic at time t.
    """
    R = z[2]  # Research level
    S = z[1]  # Status
    beta = np.random.normal(0.05, 0.5) * (S)#1/0.05*np.sin(S)  # Research growth rate, is it a function of status?
    return beta * (1 - R) * R

def career_evolution(t, z):
    """
    This function describes the change in career state of an academic over time.
    Arguments:
    t : float
        The time in years.
    z : list
        A list holding the career state of the academic.
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
    z0_pay = 50000  # Initial pay

    n_runs = 10  # Number of random initial conditions
    all_pay = []
    all_status = []
    all_research = []
    all_lifetime_pay = []

    fig, ax = plt.subplots(2, sharex=True, figsize=(10, 6))

    for i in range(n_runs):
        z0_status = np.random.uniform(0.05, 0.5)
        z0_research = np.random.uniform(0, 0.5)
        z0 = [z0_pay, z0_status, z0_research]

        solution = solve_ivp(career_evolution, [t[0], t[-1]], z0, t_eval=t, method='RK45')

        pay = solution.y[0]
        status = solution.y[1]
        research = solution.y[2]
        lifetime_pay = np.trapz(pay, t)

        all_pay.append(pay)
        all_status.append(status)
        all_research.append(research)
        all_lifetime_pay.append(lifetime_pay)

        ax[0].plot(t, pay/100000, alpha=0.5)
        ax[1].plot(t, status, 'b', alpha=0.5)
        ax[1].plot(t, research, 'g', alpha=0.5)

    ax[0].set_ylabel("Pay (per 100k)")
    ax[0].set_title(f"{n_runs} Random Career Trajectories")
    ax[0].grid()

    ax[1].set_xlabel("Time (years)")
    ax[1].set_ylabel("Status / Research")
    ax[1].grid()

    plt.tight_layout()
    plt.show()