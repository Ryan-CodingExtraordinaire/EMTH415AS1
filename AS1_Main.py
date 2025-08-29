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
inflation = 0.01  # 1% inflation rate [I don't know if this is the right value]

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
    return inflation * z[0] + 0.03 * z[1] * z[0]

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
    alpha_R = 0.2 # Research contribution to status change
    alpha_T = 0.05  # Teaching contribution to status change
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
    beta = 0.05 #* S  # Research growth rate, is it a function of status?
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

    t = np.linspace(0, 100, 1000)  # Assume a 40-year career
    z0 = [50000, 0.5, 0.5]  # Initial state: [Pay, Status, Research]
    
    # Solve the system using solve_ivp
    solution = solve_ivp(career_evolution, [t[0], t[-1]], z0, t_eval=t, method='RK45')

    # Extract the results
    pay = solution.y[0]
    status = solution.y[1]
    research = solution.y[2]

    # Calculate lifetime pay (integral of pay over time)
    #lifetime_pay = np.trapz(pay, t)

    # Create a grid for the stream plot
    pay_vals = np.linspace(20000, 200000, 40)
    status_vals = np.linspace(0, 1, 20)
    reseacrch_vals = np.linspace(0, 1, 20)
    pay_grid, status_grid = np.meshgrid(pay_vals, status_vals)

    # Compute the derivatives on the grid
    dPay_grid = np.zeros_like(pay_grid)
    dStatus_grid = np.zeros_like(status_grid)
    for i in range(pay_grid.shape[0]):
        for j in range(pay_grid.shape[1]):
            z_temp = [pay_grid[i, j], status_grid[i, j], 0.5]  # Assume constant research level
            dz = career_evolution(0, z_temp)
            dPay_grid[i, j] = dz[0]
            dStatus_grid[i, j] = dz[1]

    # Normalize the vectors for better visualization
    magnitude = np.sqrt(dPay_grid**2 + dStatus_grid**2)
    dPay_grid /= magnitude
    dStatus_grid /= magnitude

    # Plot the stream plot
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

    # hello