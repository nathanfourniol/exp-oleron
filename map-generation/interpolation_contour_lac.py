#!/usr/bin/env python3

import csv
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import polynomial as P
import json


def sign(x, y):
    """fonction sign de la différence x-y retourne -1 ou +1"""
    if x-y < 0:
        return -1
    elif x == y:
        return 0
    else:
        return 1


dataX, dataY = [], []
files = ["contour_lac_sat.csv", "contour_ile_nord.csv", "contour_ile_sud.csv"]
which_file = 0
with open(files[which_file], "r") as csv_file:
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
    print(f'New domain : {new_domain}, i : {i}')
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
        # domainX[j].append(2 * dataX[i+1] - dataX[i])
        # domainY[j].append(2 * dataY[i+1] - dataY[i])
        # domainX[j].append(3 * dataX[i+1] - 2 * dataX[i])
        # domainY[j].append(3 * dataY[i+1] - 2 * dataY[i])
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
ordre = [5, 5, 1, 1, 1]
print(len(domainX))
for i in range(0, len(domainX)):
    c.append(P.polyfit(domainX[i], domainY[i], ordre[i]))
    x_min = min(domainX[i][0], domainX[i][-1])
    x_max = max(domainX[i][0], domainX[i][-1])
    l_xnew.append(np.linspace(x_min-0.5, x_max+0.5))
# c = P.polyfit(domainX[0], domainY[0], 5)
plt.figure()
# plt.plot(dataX, dataY)
print(c)
# plt.plot(dataX[-1], dataY[-1])
for i in range(0, len(domainX)):
    plt.plot(domainX[i], domainY[i])
    plt.plot(l_xnew[i], P.polyval(l_xnew[i], c[i]))
plt.show()

write = input("Write the result in the file ? [y/n]")
liste_balises = ["lac", "ile_n", "ile_s"]
balise = liste_balises[which_file]
if write == "y":
    with open("contour.json", "r") as f2read:
        contour = json.loads(f2read.readline())
    with open("contour.json", "w") as f2write:
        coef = []
        for i in c:
            coef.append(i.tolist())
        contour[balise] = coef
        print(contour)
        f2write.write(json.dumps(contour))
