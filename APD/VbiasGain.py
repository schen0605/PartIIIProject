
# ----------------------------
# AUTHOR: Stephen Chen
# crsID: sc2043
# COLLEGE: King's
# DATE: Feb 2021
# PURPOSE: Part III Project - Creates graphs using matplotlib from LTSpice output data (ASCII text file).
# ----------------------------

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy import optimize

counter = 0 # used to separate multiple data streams e.g. an IV graph with different resistance values

# ----------------------------
# SPECIFY FILE HERE:
# ----------------------------

f = open("Data/VbiasGain.txt","r")

# ----------------------------
# Initialises global data arrays
# ----------------------------

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

xVar = [[] for i in range(counter+1)]
yVar = [[] for i in range(counter+1)]
graphLabel = np.array([])

# ----------------------------
# Helper functions
# ----------------------------

def appendArray(data, count):
    global xVar, yVar
    xVar[count] = np.append(xVar[count],float(data[0]))
    yVar[count] = np.append(yVar[count],float(data[1]))
    return

def linFunc(x, m):
    return m*x

# ----------------------------
# Main function
# ----------------------------

# Reset back to beginning of the file
counter = 0
f.seek(0)
f.readline()

for line in f:
    # print(repr(line))
    line = line.strip()
    row = line.split()
    # variable[0] = np.append(variable[0],1.1)
    # print(variable)

    try: # test if the line contains data values
        floatTest = float(row[0])
    except ValueError:
        counter += 1
        graphLabel = np.append(graphLabel,row[2])
        continue # moves on to next line if the line does not contain data

    appendArray(row, counter - 1)

f.close()

# ----------------------------
# Calculate gain
# ----------------------------

ELECTRON_CHARGE = 1.6E-19
V_BREAK = 1
C_d = 50E-15
C_q = 20E-15

gain = np.zeros(len(xVar))
overvoltage = np.zeros(len(xVar))
theoretical = np.zeros(len(xVar))


for i in range(len(xVar)):
    yVar[i] -= yVar[i][0]
    xVar[i] -= 10E-9

    index = np.where(xVar[i] > 0)[0][0]
    xVar[i] = xVar[i][index:]
    yVar[i] = yVar[i][index:]

    gain[i] = np.trapz(yVar[i], xVar[i]) / ELECTRON_CHARGE
    overvoltage[i] = float(graphLabel[i][7:]) - V_BREAK

theoretical = ((C_d+C_q)*overvoltage)/ELECTRON_CHARGE

print gain *1E-6
print theoretical *1E-6


# ----------------------------
# Linear fit
# ----------------------------

# params, covariance = optimize.curve_fit(linFunc, overvoltage, gain)
# print params

# ----------------------------
# Plot graphs
# ----------------------------

fig = plt.figure(figsize=(12, 7))

plt.plot(overvoltage, gain*1E-6, '+', markersize=10)
plt.plot(overvoltage, theoretical*1E-6, '--r',linewidth = 2, label = 'Theoretical')
# plt.plot(overvoltage, linFunc(overvoltage, params[0])*1E-6, 'k')

# plt.title('SiPM_2 Vbias Gain')
plt.xlabel('Overvoltage [V]')
plt.ylabel('Gain [x10$^{6}$]')
plt.legend(loc='lower right', frameon=False, ncol = 3)

plt.xlim([0,10])

plt.savefig("Graphics/VbiasGainFINAL.png")
plt.show()
