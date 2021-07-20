
# ----------------------------
# AUTHOR: Stephen Chen
# crsID: sc2043
# COLLEGE: King's
# DATE: Feb 2021
# PURPOSE: Part III Project - Creates graphs using matplotlib from LTSpice output data (ASCII text file).
# ----------------------------

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import scipy.integrate as integrate

# ----------------------------
# SPECIFY FILE HERE:
# ----------------------------

f = open("Data/SingleCurrent+Voltage.txt","r")

# ----------------------------
# Initialises global data arrays and constants
# ----------------------------

time = np.array([])
current = np.array([])
voltage = np.array([])
R_q = 500E3
C_q = 20E-15
C_d = 50E-15
THEORETICAL_tau = R_q * (C_q + C_d)

# ----------------------------
# Helper functions
# ----------------------------

def appendArray(data):
    global time, current, voltage

    # retrieves data from string
    time = np.append(time,float(data[0]))
    voltage = np.append(voltage,float(data[1]))
    current = np.append(current,float(data[2]))

    return

# to calculate linear fit for recovery time
def linFunc(x, m, c):
    return m * x + c

# ----------------------------
# Main function
# ----------------------------

counter = 0
f.readline() # ignore header

for line in f:

    line = line.strip()
    row = line.split()

    try: # test if the line contains data values
        floatTest = float(row[0])
    except ValueError:
        counter += 1
        continue # moves on to next line if the line does not contain data

    appendArray(row)

f.close()

# ----------------------------
# Plot graphs
# ----------------------------

fig = plt.figure(figsize=(12, 7))
ax2 = plt.subplot(122)
ax2.plot(time*1E9, (voltage*C_d)*1E15, linewidth = 2)
# plt.title('(b)')
plt.xlabel('Time [ns]')
plt.ylabel('Charge [fC]')

ax1 = plt.subplot(121)
plt.plot(time*1E9, current*1E6, linewidth = 2)
# plt.title('(a)')
# plt.plot(time*1E9, np.log(current*1E6), linewidth = 2)

# plt.title('$\Delta$V = 1V, R$_d$ = 1k$\Omega$, C$_d$ = 50fF, R$_q$ = 500k$\Omega$, C$_q$ = 20fF')
plt.xlabel('Time [ns]')
plt.ylabel('Current [$\mu$A]')

# plt.savefig("Graphics/SingleCurrentChargeFINAL.png")
plt.show()

# ----------------------------
# Calculate recovery time from current data: Use 'RecoveryTime.txt'
# ----------------------------

# finalTau = 0
# finalPerError = 100
#
# for i in range(2,len(time)):
#     # slice the array
#     timeShift = (time - 1.04E-8)[:i]
#     lnCurrent = np.log(current[:i])
#
#     params, covariance = optimize.curve_fit(linFunc, timeShift, lnCurrent)
#
#     tau = -1.0/params[0]
#     perError = (tau - THEORETICAL_tau)/THEORETICAL_tau * 100
#     print tau
#
#     if (np.abs(perError) < finalPerError):
#         finalPerError = perError
#         finalTau = tau
#
# print finalTau*1E9, finalPerError

# ----------------------------
# TEST: calculate gain
# ----------------------------

# ELECTRON_CHARGE = 1.6E-19
# C_d = 50E-15
# C_q = 20E-15
# print((C_d+C_q)/ELECTRON_CHARGE)
# # print(((C_d+C_q)*2)/ELECTRON_CHARGE)
# print THEORETICAL_tau
# test = np.trapz(current[1:40], time[1:40])
# print time
# print (test / ELECTRON_CHARGE)
