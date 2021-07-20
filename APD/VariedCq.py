
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

f = open("Data/VariedCq.txt","r")

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
for i in range(len(xVar)):
    # print graphLabel[i][4:]
    label = 'C = ' + graphLabel[i][4:] + 'F'
    # print label
    plt.plot(xVar[i]*1E9, yVar[i]*1E6, linewidth = 2, label = label)

plt.xlim([8,14])
# plt.ylim([0.5,2.2])

plt.title('$\Delta$V = 1V, C$_d$ = 50fF, R$_d$ = 1k$\Omega$, R$_q$ = 500k$\Omega$')
plt.xlabel('Time [ns]')
plt.ylabel('Current [$\mu$A]')
plt.legend(loc='lower right')
# plt.savefig("Graphics/FILE.png")
plt.show()
