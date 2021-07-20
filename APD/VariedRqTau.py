
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

counter = 0 # used to separate multiple data streams e.g. an IV graph with different resistance values

# ----------------------------
# SPECIFY FILE HERE:
# ----------------------------

f = open("Data/VariedRqTau.txt","r")

# ----------------------------
# Initialises global data arrays and constants
# ----------------------------

# R_q = 500E3
C_q = 20E-15
C_d = 50E-15
# THEORETICAL_tau = R_q * (C_q + C_d)

# Ignore header lines
f.readline()
f.readline()

for line in f:
    line = line.strip()
    row = line.split()
    try: # test if the line contains data values
        floatTest = float(row[1])
    except ValueError:
        counter += 1

time = [[] for i in range(counter+1)]
current = [[] for i in range(counter+1)]
resistance = np.array([])

# ----------------------------
# Helper functions
# ----------------------------

def appendArray(data, count):
    global time, current

    # retrieves data from string
    time[count] = np.append(time[count],float(data[0]))
    current[count] = np.append(current[count],float(data[1]))

    return

# to calculate linear fit for recovery time
def linFunc(x, m, c):
    return m * x + c

# ----------------------------
# Main function
# ----------------------------

counter = 0
f.seek(0)
f.readline() # ignore header

for line in f:

    line = line.strip()
    row = line.split()

    try: # test if the line contains data values
        floatTest = float(row[0])
    except ValueError:
        counter += 1
        resistance = np.append(resistance,float(row[2][4:-1])*1E3)
        continue # moves on to next line if the line does not contain data

    appendArray(row, counter - 1)

f.close()

# ----------------------------
# Calculate recovery time from current data
# ----------------------------

recoveryTime = np.zeros(len(current))
timeError = np.zeros(len(current))
# theoretical recovery time = R_q * (C_q + C_d)
theoreticalTau = resistance * (C_d+C_q)

for i in range(len(current)):
    # print current[i]
    # print np.amax(current[i])
    index = np.where(current[i] == np.amax(current[i]))[0][0]

    current[i] = current[i][index:]
    time[i] = time[i][index:]
    # print time[i]

    # prepares the arrays for linear regression
    current[i] = np.log(current[i])
    timeShift = time[i][0]
    time[i] = time[i] - timeShift


    finalTau = 0
    finalPerError = 100

    for j in range(2,len(current[i])):

        tempTime = time[i][:j]
        tempCurrent = current[i][:j]

        params, covariance = optimize.curve_fit(linFunc, tempTime, tempCurrent)

        tau = -1.0/params[0]
        perError = (tau - theoreticalTau[i])/theoreticalTau[i] * 100
        # print tau
        # print perError

        if (np.abs(perError) < finalPerError):
            finalPerError = perError
            finalTau = tau

    recoveryTime[i] = finalTau
    timeError[i] = finalPerError

# ----------------------------
# Plot graphs
# ----------------------------

fig = plt.figure(figsize=(12, 7))


plt.plot(resistance*1E-3, recoveryTime*1E9,'+', markersize=10)
plt.plot(resistance*1E-3, theoreticalTau*1E9, '--r',linewidth = 2, label = 'Theoretical')

# plt.title('$\Delta$V = 1V, R$_d$ = 1k$\Omega$, C$_d$ = 50fF, C$_q$ = 20fF, $\\tau_{theory}$=R$_q$(C$_d$+C$_q$)')

plt.xlim([100,1000])

plt.xlabel('R$_q$ [k$\Omega$]')
plt.ylabel('Recovery Time [ns]')
plt.legend(loc='lower right', frameon=False)

# plt.savefig("Graphics/VariedRqTauFINAL.png")
plt.show()


#
