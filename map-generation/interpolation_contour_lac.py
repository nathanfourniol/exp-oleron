#!/usr/bin/env python3

import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from numpy.polynomial import polynomial as P


def sign(x, y):
    """fonction sign de la différence x-y retourne -1 ou +1"""
    if x-y < 0:
        return -1
    elif x == y:
        return 0
    else:
        return 1


dataX, dataY = [], []
with open("contour_lac1.csv", "r") as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        dataX.append(float(row[0]))
        dataY.append(float(row[1]))

dataX = np.array(dataX)
dataY = np.array(dataY)
xnew = np.linspace(0, 700)


# division de l'espace :
domainX = [[]]
domainY = [[]]
i, j = 0, 0
new_domain = True
while i < len(dataX)-2:
    if new_domain:
        domainX[j].append(dataX[i])
        domainX[j].append(dataX[i+1])
        domainY[j].append(dataY[i])
        domainY[j].append(dataY[i+1])
        new_domain = False
    if sign(dataX[i], dataX[i+1]) == sign(dataX[i+1], dataX[i+2]):
        domainX[j].append(dataX[i+2])
        domainY[j].append(dataY[i+2])
    else:
        # Ajout d'un point supplémentaire suivant la meme pente
        domainX[j].append(2 * dataX[i+1] - dataX[i])
        domainY[j].append(2 * dataY[i+1] - dataY[i])
        domainX[j].append(3 * dataX[i+1] - 2 * dataX[i])
        domainY[j].append(3 * dataY[i+1] - 2 * dataY[i])
        
        domainX.append([])
        domainY.append([])
        j += 1
        new_domain = True
    i += 1

# l_xnew = []  # to calculate the interpolation
# f = []
# print(len(domainX))
# for i in range(0, len(domainX)-1):
#     print(i)
#     f.append(interp1d(domainX[i], domainY[i], kind='cubic'))
#     x_min = min(domainX[i][0], domainX[i][-1])
#     x_max = max(domainX[i][0], domainX[i][-1])
#     l_xnew.append(np.linspace(x_min, x_max))

l_xnew = []  # to calculate the interpolation
c = []
ordre = [6, 5, 3, 2, 2]
print(len(domainX))
for i in range(0, len(domainX)):
    print(i)
    c.append(P.polyfit(domainX[i], domainY[i], ordre[i]))
    x_min = min(domainX[i][0], domainX[i][-1])
    x_max = max(domainX[i][0], domainX[i][-1])
    l_xnew.append(np.linspace(x_min, x_max))
# c = P.polyfit(domainX[0], domainY[0], 5)
plt.figure()
# plt.plot(dataX, dataY)
print(c)
# plt.plot(dataX[-1], dataY[-1])
for i in range(0, len(domainX)):
    plt.plot(domainX[i], domainY[i])
    plt.plot(l_xnew[i], P.polyval(l_xnew[i], c[i]))
plt.show()
