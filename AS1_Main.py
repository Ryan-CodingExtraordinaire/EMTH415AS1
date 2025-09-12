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

# setting some parameters constant so that the recognition parameter can be explored,
# the parameters have been tweaked to make the model replicate the real data
RECOGNITION_VAL = 0.01
ALPHA_R_VAL = 0.05
ALPHA_T_VAL = 0.01
BETA_VAL = 0.5

female_reduction_factor = 0.51546 # found by running "male vs female recognition" section 

## PARAMETERS ##
def recognition(t, val):#, activation):
    """
    Recognition factor for pay increase due to status.
    Can vary with time or career state.
    """
    return val# * H(t-activation)

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

def career_evolution(t, z, params):#, activation):
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
    # ------------------ Standard career simulation ------------------
    t = np.linspace(0, 40, 1000)  # Assume a 40-year career
    z0 = [78856, 0.5, 0.5]  # Initial state: [Pay, Status, Research]
    
    ## Solve the system using solve_ivp
    solution_male = solve_ivp(career_evolution, [t[0], t[-1]], z0, t_eval=t, method='RK45', args=([RECOGNITION_VAL, ALPHA_R_VAL, ALPHA_T_VAL, BETA_VAL],))

    ## Extract the results
    pay_male = solution_male.y[0]
    status_male = solution_male.y[1]
    research_male = solution_male.y[2]

    ## Calculate lifetime pay (integral of pay over time)
    #lifetime_pay = np.trapz(pay, t)

    solution_female = solve_ivp(career_evolution, [t[0], t[-1]], z0, t_eval=t, method='RK45', args=([RECOGNITION_VAL * female_reduction_factor, ALPHA_R_VAL, ALPHA_T_VAL, BETA_VAL],))

    ## Extract the results
    pay_female = solution_female.y[0]
    status_female = solution_female.y[1]
    research_female = solution_female.y[2]

    plt.figure(figsize=(12, 8))

    ## Subplot for Pay
    plt.subplot(2, 1, 1)
    # real career pay data
    data = np.loadtxt('UC_Academic_Career_Salary_2025_40yr.csv', delimiter=',', skiprows=1, usecols=(0, 1))
    years = data[:, 0]
    salaries = data[:, 1]
    plt.plot(years, salaries, label="Actual Salary Data", marker='o')
    plt.plot(t, pay_male, label="Pay $ (Male)", color="blue")
    plt.plot(t, pay_female, label="Pay $ (Female)", color="orange")
    plt.xlabel("Time (years)")
    plt.ylabel("Modelled Pay")
    plt.title("Pay Evolution Over Time")
    plt.grid()
    plt.legend()

    ## Subplot for Status and Research
    plt.subplot(2, 1, 2)
    plt.plot(t, status_male, label="Status", color="green")
    plt.plot(t, research_male, label="Research", color="red")
    plt.xlabel("Time (years)")
    plt.ylabel("Values")
    plt.title("Status and Research Evolution Over Time")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

    # # ---------------- sensitivity analysis ----------------
    # t = np.linspace(0, 40, 1000)  # Assume a 40-year career
    # z0 = [50000, 0.5, 0.5]  # Initial state: [Pay, Status, Research]

    # base_param_set = [0.03, 0.1, 0.05, 0.5] # [recognition_val, alpha_R_val, alpha_T_val, beta_val]
    # perterbations = np.linspace(0.1, 2, 100)  # 10% to 200% of the base value
    # param_sets = []
    # for i in range(len(base_param_set)):
    #     for p in perterbations:
    #         perturbed_param_set = base_param_set.copy()
    #         perturbed_param_set[i] *= p
    #         param_sets.append(perturbed_param_set)
    # final_pays = []
    # # print(np.array(param_sets))
    # for param_set in param_sets:
    #     solution = solve_ivp(career_evolution, [t[0], t[-1]], z0, t_eval=t, method='RK45', args = (param_set,))
    #     final_pays.append(solution.y[0][-1])

    # # Extract beta and recognition values from param_sets
    # beta_values = [params[3] for params in param_sets]
    # recognition_values = [params[0] for params in param_sets]

    # final_pays = np.array(final_pays).reshape(len(base_param_set), len(perterbations))
    
    # # Plot final_pays against perterbations
    # plt.figure(figsize=(10, 6))
    # for i, param_name in enumerate(["Recognition", "Alpha_R", "Alpha_T", "Beta"]):
    #     plt.plot(perterbations, final_pays[i], label=f"{param_name} Perturbation", marker='o')

    # plt.xlabel("Perturbation Factor")
    # plt.ylabel("Final Pay")
    # plt.title("Sensitivity Analysis of Final Pay to Parameter Perturbations")
    # plt.legend()
    # plt.grid()
    # plt.show()


    # # ------------------- male vs female recognition -------------------
    # t = np.linspace(0, 40, 1000)  # Assume a 40-year career
    # z0 = [78856, 0.5, 0.5]  # Initial state: [Pay, Status, Research]
    # lifetime_pays_male = []
    # lifetime_pays_female = []
    # delta_lifetime_pays = []
    # reduction_constants = np.linspace(0, 1, 100)
    # for a in reduction_constants:
    #     adjusted_rec_val = RECOGNITION_VAL * a  # Assuming
    #     ## Solve the system using solve_ivp
    #     solution_male = solve_ivp(career_evolution, [t[0], t[-1]], z0, t_eval=t, method='RK45', args=([RECOGNITION_VAL, ALPHA_R_VAL, ALPHA_T_VAL, BETA_VAL],))
    #     solution_female = solve_ivp(career_evolution, [t[0], t[-1]], z0, t_eval=t, method='RK45', args=([adjusted_rec_val, ALPHA_R_VAL, ALPHA_T_VAL, BETA_VAL],))
    #     ## Extract the results
    #     pay_male = solution_male.y[0]
    #     status_male = solution_male.y[1]
    #     research_male = solution_male.y[2]

    #     pay_female = solution_female.y[0]
    #     status_female = solution_female.y[1]
    #     research_female = solution_female.y[2]

    #     lifetime_pay_male = np.trapz(pay_male, t)
    #     lifetime_pay_female = np.trapz(pay_female, t)
    #     lifetime_pays_male.append(lifetime_pay_male)
    #     lifetime_pays_female.append(lifetime_pay_female)

    #     delta_lifetime_pays.append(np.array(lifetime_pay_male) - np.array(lifetime_pay_female))
        
    # plt.figure(figsize=(10, 6))
    # # print(reduction_constants.shape, delta_lifetime_pays.shape)
    # plt.plot(reduction_constants, delta_lifetime_pays, label="Delta Lifetime Pay", marker='o')
    # # find and plot what a is when delta lifetime pay is 400000
    # for i in range(len(delta_lifetime_pays)-1):
    #     if delta_lifetime_pays[i] >= 400000 and delta_lifetime_pays[i+1] <= 400000:
    #         a_400k = reduction_constants[i] + (400000 - delta_lifetime_pays[i]) * (reduction_constants[i+1] - reduction_constants[i]) / (delta_lifetime_pays[i+1] - delta_lifetime_pays[i])
    #         plt.axvline(x=a_400k, color='r', linestyle='--', label=f"a for $400k gap: {a_400k:.2f}")
    #         print(f"a for $400k gap: {a_400k:.5f}")
    #         break
    
    # plt.xlabel("a")
    # plt.ylabel("Delta Lifetime Pay (Male pay - Female pay)")
    # plt.legend()
    # plt.grid()
    # plt.show()

    
  