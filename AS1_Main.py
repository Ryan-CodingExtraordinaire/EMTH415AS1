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
inflation = 0.02  # Annual inflation rate

## PARAMETERS ##
def recognition(t, val):
    """
    Recognition factor for pay increase due to status.
    Can vary with time or career state.
    """
    return val 

def alpha_R(t, val):
    """
    Research contribution to status change.
    Can vary with time or career state.
    """
    return val 

def alpha_T(t, val):
    """
    Teaching contribution to status change.
    Can vary with time or career state.
    """
    return val

def beta(t, val):
    """
    Research growth rate.
    Can vary with time or career state.
    """
    return val

## ODEs ##
def dpay(t, z, params):
    """
    This function models how the amount of pay received by an academic changes with time.
    """
    r = recognition(t, params[0])
    return inflation*z[0] + r*z[1]*z[0]

def dstatus(t, z, params):
    """
    This function models how the status of an academic changes with time.
    """
    S = z[1]  # Status
    R = z[2]  # Research level
    a_R = alpha_R(t, params[1])
    a_T = alpha_T(t, params[2])
    return (a_R*R + a_T*(1 - R))*S*(1 - S)

def dresearch(t, z, params):
    """
    This function models how the research level of an academic changes with time.
    """
    R = z[2]  # Research level
    b = beta(t, params[3])
    return b * (1 - R) * R

def career_evolution(t, z, params):
    """
    This function describes the change in career state of an academic over time.
    Arguments:
    t : float
        The time in years.
    z : list
        A list holding the career state of the academic.
    params : list
        Additional parameters for the ODEs used to modify the value/behaviour.
        formated as [recognition_val, alpha_R_val, alpha_T_val, beta_val]
    returns:
    dz : list
        A list containing the changes in pay, status, and research at time t.
    """
    dPay = dpay(t, z, params)
    dStatus = dstatus(t, z, params)
    dResearch = dresearch(t, z, params)
    
    return [dPay, dStatus, dResearch]

if __name__ == "__main__":
    # # Standard career simulation
    # t = np.linspace(0, 40, 1000)  # Assume a 40-year career
    # z0 = [50000, 0.5, 0.5]  # Initial state: [Pay, Status, Research]
    
    # ## Solve the system using solve_ivp
    # solution = solve_ivp(career_evolution, [t[0], t[-1]], z0, t_eval=t, method='RK45', args=([0.03, 0.1, 0.05, 0.5],))

    # ## Extract the results
    # pay = solution.y[0]
    # status = solution.y[1]
    # research = solution.y[2]

    # ## Calculate lifetime pay (integral of pay over time)
    # #lifetime_pay = np.trapz(pay, t)

    # plt.figure(figsize=(12, 8))

    # ## Subplot for Pay
    # plt.subplot(2, 1, 1)
    # plt.plot(t, pay / 100000, label="Pay (per 100k)", color="blue")
    # plt.xlabel("Time (years)")
    # plt.ylabel("Pay (per 100k)")
    # plt.title("Pay Evolution Over Time")
    # plt.grid()
    # plt.legend()

    # ## Subplot for Status and Research
    # plt.subplot(2, 1, 2)
    # plt.plot(t, status, label="Status", color="green")
    # plt.plot(t, research, label="Research", color="red")
    # plt.xlabel("Time (years)")
    # plt.ylabel("Values")
    # plt.title("Status and Research Evolution Over Time")
    # plt.legend()
    # plt.grid()
    # plt.tight_layout()
    # plt.show()

    # sensitivity analysis
    t = np.linspace(0, 40, 1000)  # Assume a 40-year career
    z0 = [50000, 0.5, 0.5]  # Initial state: [Pay, Status, Research]

    base_param_set = [0.03, 0.1, 0.05, 0.5]
    perterbations = np.linspace(0.1, 2, 100)  # 75% to 125% of base values
    param_sets = []
    for i in range(len(base_param_set)):
        for p in perterbations:
            perturbed_param_set = base_param_set.copy()
            perturbed_param_set[i] *= p
            param_sets.append(perturbed_param_set)
    final_pays = []
    # print(np.array(param_sets))
    for param_set in param_sets:
        solution = solve_ivp(career_evolution, [t[0], t[-1]], z0, t_eval=t, method='RK45', args = (param_set,))
        final_pays.append(solution.y[0][-1])

    # Extract beta and recognition values from param_sets
    beta_values = [params[3] for params in param_sets]
    recognition_values = [params[0] for params in param_sets]

    final_pays = np.array(final_pays).reshape(len(base_param_set), len(perterbations))
    
    # Plot final_pays against perterbations
    plt.figure(figsize=(10, 6))
    for i, param_name in enumerate(["Recognition", "Alpha_R", "Alpha_T", "Beta"]):
        plt.plot(perterbations, final_pays[i], label=f"{param_name} Perturbation", marker='o')

    plt.xlabel("Perturbation Factor")
    plt.ylabel("Final Pay")
    plt.title("Sensitivity Analysis of Final Pay to Parameter Perturbations")
    plt.legend()
    plt.grid()
    plt.show()
