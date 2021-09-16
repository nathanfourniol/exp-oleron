#!/usr/bin/env python3

import time
import json
import random as rd

import roblib

import matplotlib.pyplot as plt
import numpy as np
import numpy.polynomial.polynomial as P


def contour_domain(contour):
    """
    From contour find the intersection between two consecutive polynome and return the intersection in a "counter clockwise"
    return : xdomain : { 'key' : [root0, root1, ..., rootn], 'key2' : [...], ...}
    read the return first polynom domain [rootn, root0], second [root0, root1], ...
    """
    xdomain = {}
    for key in contour:  # Parcours sur les clefs de contour
        xdomain[key] = []
        for i in range(0, len(contour[key])):  # Parcours des polynomes
            if i == len(contour[key])-1:
                j = 0
            else:
                j = i+1
            poly = np.array(contour[key][i] + [0]*max((len(contour[key][j])-len(contour[key][i])), 0))  # Pour etre consistant avec les dimensions
            poly_next = np.array(contour[key][j] + [0]*max((len(contour[key][i])-len(contour[key][j])), 0))
            roots = P.polyroots(poly-poly_next)
            for root in roots:
                # print(f'{key}, {i} : {root}')
                if -0.001 < root.imag and root.imag < 0.001:
                    if 2 < root.real and root.real < 80 and root.real not in xdomain[key]:  # Tricks to choose the right roots, criteria from the display of the point cloud contour
                        xdomain[key].append(root.real)
    return xdomain


def find_domainX(i, intersection_list_absisse):
    """
    from xdomain and the polynom indix find the x domain associated to be evaluate
    return : linspace(xmin, xmax)
    """
    xmin = intersection_list_absisse[i-1]
    xmax = intersection_list_absisse[i]
    # print(f'[ {xmin}, {xmax} ]')
    return np.linspace(xmin, xmax, 50, True)


def f(x, u):
    """
    Evolution function of the robot state
    """
    x = x.flatten()
    v = 3
    return np.array([[v*np.cos(x[2])], [v*np.sin(x[2])], [u]])


def collide(x, y, poly, domain):
    """
    Return true if (x,y) resolve the polynomila equation over the domain
    """
    dy = 1
    if min(domain[0], domain[1]) <= x and x <= max(domain[0], domain[1]):
        yeval = P.polyval(x, poly)
        # print(f'yeval = {yeval}, y = {y}, x : {x}')
        return (yeval-dy <= y and y <= yeval+dy)
    else:
        return False


def collision(state, contour, xdomain):
    """
    Return Bool of the collision between the state and the contour of the lake
    """
    x, y = state[0][0], state[1][0]
    for key in contour:
        for i in range(0, len(contour[key])):
            # print(f'key : {key}, i : {i}, contour : {contour[key][i]}')
            if collide(x, y, contour[key][i], [xdomain[key][i-1], xdomain[key][i]]):
                return True
    # input()
    return False


def control_u(x, heading_d):
    k = 2
    theta_tilde = heading_d - x[2, 0]
    u = k * roblib.sawtooth(theta_tilde)
    return u


def heading_to_follow(t_prime, list_heading, list_time, current_state, previous_state, hit):
    print(f't_prime : {t_prime}, hit : {hit}, Temps: {list_time}, state : {current_state}')
    if current_state == 0:
        if hit:
            previous_state = current_state
            current_state = 3
            heading_d = list_heading[3]
            list_time[2] = t_prime
            t_prime = 0
        elif previous_state == 3 and t_prime > list_time[0]:
            previous_state = current_state
            current_state = 1
            heading_d = list_heading[1]
            t_prime = 0
        else:
            heading_d = list_heading[0]
            
    elif current_state == 1:
        if hit:
            previous_state = current_state
            current_state = 2
            heading_d = list_heading[2]
            list_time[1] = t_prime + (rd.random()-0.5)*0.6*t_prime
            t_prime = 0
        elif previous_state == 2 and t_prime > list_time[3]:
            previous_state = current_state
            current_state = 3
            heading_d = list_heading[3]
            t_prime = 0
        else:
            heading_d = list_heading[1]

    elif current_state == 2:
        if hit:
            previous_state = current_state
            current_state = 1
            heading_d = list_heading[1]
            list_time[3] = t_prime + (rd.random()-0.5)*0.6*t_prime
            t_prime = 0
        elif previous_state == 1 and t_prime > list_time[1]:
            previous_state = current_state
            current_state = 0
            heading_d = list_heading[0]
            t_prime = 0
        else:
            heading_d = list_heading[2]

    elif current_state == 3:
        if hit:
            previous_state = current_state
            current_state = 0
            heading_d = list_heading[0]
            list_time[0] = t_prime + (rd.random()-0.5)*0.6*t_prime
            t_prime = 0
        elif previous_state == 0 and t_prime > list_time[2]:  # To do : remttre les temps à infini une fois la condition passée !
            previous_state = current_state
            current_state = 2
            heading_d = list_heading[2]
            t_prime = 0
        else:
            heading_d = list_heading[3]
    return heading_d, current_state, t_prime, list_time, previous_state


if __name__ == "__main__":

    # Recuperation des coefficients des polynomes de contours
    # contour = { lac :[[], [], ...]}
    with open("contour.json", "r") as f_contour:
        contour = json.loads(f_contour.readline())
    xdomain = contour_domain(contour)

    # Preparation pour l'affichage
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    ax.xmin = 0
    ax.xmax = 75
    ax.ymin = 0
    ax.ymax = 80

    state = np.array([[10], [30], [0]])
    u = 0
    list_heading = [0, np.pi/2, -np.pi/2, np.pi]
    list_time = [10, float('inf'), 10, float('inf')]
    previous_state = 3
    current_state = 0

    t = 0
    t_simu = 500
    t_prime = 0
    t_hit = 2
    dt = 0.1
    hit = False
    while t < t_simu:
        plt.cla()
        for key in contour:
            for i in range(0, len(contour[key])):
                x = find_domainX(i, xdomain[key])
                ax.plot(x, P.polyval(x, contour[key][i]))
        ax.arrow(state[0][0], state[1][0], 2*np.cos(state[2][0]), 2*np.sin(state[2][0]))
        ax.plot(state[0], state[1], 'bo')

        hit = False
        if collision(state, contour, xdomain) and t_hit > 2:  # minimum 1 sec entre 2 hits pour contrer les multiples hits
            print(" CROSS ")
            hit = True
            t_hit = 0  # compte le temps entre chaqeu hit
            # state[2, 0] += 2*np.pi/3
            ax.plot(state[0], state[1], 'r+')
        plt.draw()
        plt.pause(0.001)
        # time.sleep(dt)
        h_d, current_state, t_prime, list_time, previous_state = heading_to_follow(t_prime, list_heading, list_time, current_state, previous_state, hit)
        u = control_u(state, h_d)
        state = state + dt * f(state, u)
        print(f'STATE : {current_state}, HEADING : {h_d}')
        # print(f'x : {state[0,0]}, y : {state[1,0]}, theta : {a}')
        t += dt
        t_hit += dt
        t_prime += dt
