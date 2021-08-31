#!/usr/bin/env python3 
# Step 1 : Recupérer la liste des points
# => afficher l'image
# => récupérer les coordonées des points
# => diviser l'espace inteligeament
# => interpolation : https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp2d.html
import numpy as np
import cv2


img = cv2.imread('lac_oleron_sat.png')  # echelle : 130px <=> 10m
size_img = np.shape(img)  # (pxl sur y, pxl sur x, canaux RGB)

pressedkey = cv2.waitKey(0)
mouseX, mouseY = 0, 0
echelle = [130, 10]  # 130 pxls <=> 10 m


def draw_circle(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 3, (255, 255, 255), -1)
        mouseX, mouseY = x, y


def chgmt_repere_echelle(size_img, echelle, x, y):
    """
    Changement de repere pour avoir la ref 0,0 en bas à gauche (opencv le fai depuis le coin en haut à gauche)
    Mise à l'echelle : echelle passage du nombre de pixel en coordonnée variable : [nb_pxl, distance_reelle]
    """
    facteur_echelle = echelle[1]/echelle[0]
    xnew = x*facteur_echelle
    ynew = (size_img[0] - y) * facteur_echelle
    return xnew, ynew


f = open("contour_lac_sat.csv", 'a')
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)
while(1):
    cv2.imshow('image', img)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print(mouseX, mouseY)
        xscaled, yscaled = chgmt_repere_echelle(size_img, echelle, mouseX, mouseY)
        f.write("{}, {}\n".format(xscaled, yscaled))  # en pixel depuis l'angle haut à gauche
f.close()
