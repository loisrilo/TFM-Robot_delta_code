# -*- coding: utf-8 -*-
# Copyright 2016 Lois Rilo Antelo (loisriloantelo@gmail.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import math

# Specific geometry for my delta robot:
e = 100.0  # small triangle side (EE)
f = 215.0  # support triangle side
re = 350.0  # upper arm length
rf = 250.0  # lower arm length
hf = math.sqrt(0.75*(f**2))
he = math.sqrt(0.75*(e**2))

dtr = math.pi / 180.0  # degrees to radians

# Initial points
A1 = [hf/3, 0, 0]
A2 = [-A1[0]*math.cos(60*dtr), -A1[0]*math.sin(60*dtr), 0]
A3 = [A2[0], -A2[1], 0]


def punto_codo(theta):
    theta *= dtr
    b1 = [A1[0]+rf*math.cos(theta), 0.0, rf*math.sin(theta)]
    return b1

sin120 = math.sin(120*dtr)
cos120 = math.cos(120*dtr)
def rotacion120(ent):
    sal = [0.0, 0.0, 0.0]
    sal[0] = cos120*ent[0]+sin120*ent[1]
    sal[1] = -sin120*ent[0]+cos120*ent[1]
    sal[2] = ent[2]
    return sal


sin240 = math.sin(240*dtr)
cos240 = math.cos(240*dtr)
def rotacion240(ent):
    sal = [0.0, 0.0, 0.0]
    sal[0] = cos240*ent[0]+sin240*ent[1]
    sal[1] = -sin240*ent[0]+cos240*ent[1]
    sal[2] = ent[2]
    return sal


def sumav(v1, v2):
    s = [0.0, 0.0, 0.0]
    s[0] = v1[0] + v2[0]
    s[1] = v1[1] + v2[1]
    s[2] = v1[2] + v2[2]
    return s


vhe1 = [he/3, 0.0, 0.0]
vhe2 = rotacion120(vhe1)
vhe3 = rotacion120(vhe2)
def punto_ee(ee, brazo):
    sal = [0.0, 0.0, 0.0]
    if brazo == 1:
        sal = sumav(ee, vhe1)
    elif brazo == 2:
        sal = sumav(ee, vhe2)
    elif brazo == 3:
        sal = sumav(ee, vhe3)
    return sal


def rotacion_y(ent, ang):
    sal = [0.0, 0.0, 0.0]
    sal[0] = ent[0]*math.cos(ang) - ent[2]*math.sin(ang)
    sal[1] = ent[1]
    sal[2] = -ent[0]*math.sin(ang) + ent[2]*math.cos(ang)
    return sal

def angulos_codo(codo, ee, brazo):
    if brazo == 2:
        codo = rotacion240(codo)
        ee = rotacion240(ee)
    elif brazo == 3:
        codo = rotacion120(codo)
        ee = rotacion120(ee)
    if (codo[0]-ee[0]) != 0:
        ang_a = math.atan((ee[2]-codo[2])/(codo[0]-ee[0]))
    else:
        ang_a = 1.570796326794897
    # prep
    codo = rotacion_y(codo, ang_a)
    ee = rotacion_y(ee, ang_a)
    # calc
    if (codo[0]-ee[0]) != 0:
        ang_b = math.atan((ee[1])/(codo[0]-ee[0]))
    else:
        ang_b = 0
    return [ang_a, ang_b]


angulos = [30, 40, 45]
punto = [53.93, -20.0572, 414.4331]

# p = delta_kinematics.forward(angulos[0], angulos[1], angulos[2])
c1 = punto_codo(angulos[0])
p1 = punto_ee(punto, 1)
[a1_a, a1_b] = angulos_codo(c1, p1, 1)

c2 = punto_codo(angulos[1])
c2 = rotacion120(c2)  # B2 en matlab
p2 = punto_ee(punto, 2)
[a2_a, a2_b] = angulos_codo(c2, p2, 2)

c3 = punto_codo(angulos[2])
c3 = rotacion240(c3)
p3 = punto_ee(punto, 3)
[a3_a, a3_b] = angulos_codo(c3, p3, 3)

# print c1
# print p1
print [a1_a, a1_b]
print [a1_a/dtr, a1_b/dtr]
# print rotacion240(c2)
# print p2
print [a2_a, a2_b]
print [a2_a/dtr, a2_b/dtr]
# print rotacion120(c3)
# print p3
print [a3_a, a3_b]
print [a3_a/dtr, a3_b/dtr]
