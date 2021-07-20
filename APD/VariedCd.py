
# ----------------------------
# AUTHOR: Stephen Chen
# crsID: sc2043
# COLLEGE: King's
# DATE: Feb 2021
# PURPOSE: Part III Project - Creates graphs using matplotlib from LTSpice output data (ASCII text file).
# ----------------------------

import numpy as np
import matplotlib.pyplot as plt

counter = 0 # used to separate multiple data streams e.g. an IV graph with different resistance values

# ----------------------------
# SPECIFY FILE HERE:
# ----------------------------

f = open("Data/VariedCd.txt","r")

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

time = [[] for i in range(counter+1)]
voltage = [[] for i in range(counter+1)]
current = [[] for i in range(counter+1)]
graphLabel = np.array([])

# ----------------------------
# Helper functions
# ----------------------------

def appendArray(data, count):
    global time, voltage, current
    time[count] = np.append(time[count],float(data[0]))
    voltage[count] = np.append(voltage[count],float(data[1]))
    current[count] = np.append(current[count],float(data[2]))
    return

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
# print(xVar[0], yVar[0])

# ----------------------------
# Plot graphs
# ----------------------------

fig = plt.figure(figsize=(12, 7))
ax1 = plt.subplot(121)
plt.title('(a)')
plt.xlabel('Time [ns]')
plt.ylabel('Current [$\mu$A]')
ax2 = plt.subplot(122)
plt.title('(b)')
plt.xlabel('Time [ns]')
plt.ylabel('Charge [fC]')

for i in range(len(time)):
    label = graphLabel[i][4:] + 'F'
    capacitance = int(graphLabel[i][4:-1]) # in fF
    ax1.plot(time[i]*1E9, current[i]*1E6, linewidth = 2, label = label)
    ax2.plot(time[i]*1E9, voltage[i]*capacitance, linewidth = 2, label = label)

# plt.xlim([8,12])
# plt.ylim([0.5,2.2])
ax1.legend(loc='upper right', frameon=False)
# plt.suptitle('$\Delta$V = 1V, R$_d$ = 1k$\Omega$, R$_q$ = 500k$\Omega$, C$_q$ = 20fF')
# plt.savefig("Graphics/VariedCdFINAL.png")
plt.show()
