# -*- coding: utf-8 -*-
# Copyright 2016 Lois Rilo Antelo (loisriloantelo@gmail.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from svg.path import parse_path
import numpy as np
import matplotlib.pyplot as plt
from lxml import etree
import delta_kinematics as dk
import itertools


def bezier_to_points(p0, p1, p2, p3, t, res):
    # t: escala
    # res: resolucion
    bx = []
    by = []
    for i in np.arange(0, 1.001, res):
        x = np.real(p0)*(1-i)**3 + 3*i*np.real(p1)*(1-i)**2 + 3*np.real(p2)*(i**2)*(1-i) + np.real(p3)*(i**3)
        bx.append(t*x)
        y = np.imag(p0)*(1-i)**3 + 3*i*np.imag(p1)*(1-i)**2 + 3*np.imag(p2)*(i**2)*(1-i) + np.imag(p3)*(i**3)
        by.append(t*y)
    return bx, by


def puntos_contorno(path, esc, res):
    p_x = []
    p_y = []
    for curva in range(len(path)):
        if str(type(path[curva])) == "<class 'svg.path.path.CubicBezier'>":
            a, b = bezier_to_points(path[curva].start, path[curva].control1, path[curva].control2, path[curva].end, esc,
                                    res)
            p_x.append(a)
            p_y.append(b)
        # elif str(type(path[curva])) == "<class 'svg.path.path.Line'>":  # if wanted...
            # ignorar (escribir accion si necesario)
        #     print 'tioo aquii aquii'
        #     print path[curva]
        # else:
        #     print 'y esto?'
    return p_x, p_y


def extraer_recorridos(svg_directory):
    # svg_directory: ruta absoluta hasta el archivo (svg y filtrado con inkscape)
    svg_file = etree.parse(svg_directory)
    # print etree.tostring(svg_file, pretty_print=True)
    svg_root = svg_file.getroot()
    recorrido = []
    for index1 in range(len(svg_root)):
        if svg_root[index1].tag == '{http://www.w3.org/2000/svg}g':
            for index2 in range(len(svg_root[index1])):
                p = svg_root[index1][index2].attrib
                if 'd' in p:
                    recorrido.append(parse_path(svg_root[index1][index2].attrib['d']))
    # print recorrido
    # print len(recorrido)
    return recorrido


# def joan(iterables):
#     meow = []
#     # chain.from_iterable(['ABC', 'DEF']) --> A B C D E F
#     for it in iterables:
#         for element in it:
#             #print 'meow'
#             meow.append(element)
#     return meow


def dimensionado(r, ancho_deseado, alto_deseado, dibujar):
    # Transforma el conjunto de trayectorias de un dibujo en una sola ajustado a un tamanno y centrada en el origen
    # r: recorridos a dimensionar
    # dibujar: si es 1 dibuja el resultado
    max_x = []
    min_x = []
    max_y = []
    min_y = []
    cambio_de_trazo = [] #recoge el indice del array donde se produce un cambio de path.
    indice = 0
    for i in range(len(r)):
        px, py = puntos_contorno(r[i], 1, 0.05) #0.05
        # plt.plot(px, py, 'ro')
        # plt.show()
        pmx = list(itertools.chain.from_iterable(px))
        pmy = list(itertools.chain.from_iterable(py))
        max_x.append(max(pmx))
        min_x.append(min(pmx))
        max_y.append(max(pmy))
        min_y.append(min(pmy))
    ancho = max(max_x) - min(min_x)
    alto = max(max_y) - min(min_y)
    if dibujar:
        print ancho, alto
    escala_ancho = ancho_deseado / ancho
    escala_alto = alto_deseado / alto
    escala = min(escala_alto, escala_ancho)
    if dibujar:
        print 'la escala es: %r' % escala
    # SITUACION:
    desp_x = (ancho * escala) / 2 + min(min_x) * escala
    desp_y = (alto * escala) / 2 + min(min_y) * escala
    # print "despx: %r despy: %r" % (desp_x, desp_y)
    # DIBUJO ESCALADO Y COLOCADO EN EL CENTRO:
    dib_x = []
    dib_y = []
    for i in range(len(r)):
        px, py = puntos_contorno(r[i], escala, 0.01) #0.01
        px = list(itertools.chain.from_iterable(px))
        py = list(itertools.chain.from_iterable(py))
        # Se guarda el indice donde se cambia de trazo para levantar el lapiz en el disenyo de la trayectoria.
        dib_x.append(px)
        dib_y.append(py)
        indice += len(px)
        cambio_de_trazo.append(indice-1)
    dib_x = list(itertools.chain.from_iterable(dib_x))
    dib_y = list(itertools.chain.from_iterable(dib_y))
    dib_x = [x - desp_x for x in dib_x]
    dib_y = [y - desp_y for y in dib_y]
    if dibujar:
        print "dibujo en x entre %r y %r siendo ancho %r" % (max(dib_x), min(dib_x), max(dib_x) - min(dib_x))
        print "dibujo en y entre %r y %r siendo el alto %r" % (max(dib_y), min(dib_y), max(dib_y) - min(dib_y))
    plt.plot(dib_x, dib_y, 'ro')
    if dibujar:
        plt.show()
    return dib_x, dib_y, cambio_de_trazo


def entrada_inicial(dx, dy, dz):
    longi = 100
    inc = 30.0
    e1 = [dx[0]]*longi
    e2 = [dy[0]]*longi
    e3 = [dz[0] - inc + inc * indice / longi for indice in range(longi)]
    dx = e1 + dx
    dy = e2 + dy
    dz = e3 + dz
    return dx, dy, dz


def cambios_trazo(dx, dy, dz, cdt):
    # anyade puntos de subida en los cambios de trazo:
    for trazo in list(reversed(range(len(cdt) - 1))):
        # puntos iniciales y finales del cambio de trazo.
        x_ini = dx[cdt[trazo]]
        x_fin = dx[cdt[trazo] + 1]
        y_ini = dy[cdt[trazo]]
        y_fin = dy[cdt[trazo] + 1]
        # puntos intermedios:
        num_puntos = 200
        num_bajada = 20
        inc_x = (x_fin - x_ini) / num_puntos
        inc_y = (y_fin - y_ini) / num_puntos
        # insertar puntos:
        for j in range(num_puntos):  # inserta puntos.
            dx.insert(cdt[trazo] + j + 1, x_ini + inc_x * j)
            dy.insert(cdt[trazo] + j + 1, y_ini + inc_y * j)
            if j < 10:
                dz.insert(cdt[trazo] + j + 1, pz - 25)
            elif j > (num_puntos - num_bajada):
                dz.insert(cdt[trazo] + j + 1, pz - (float(num_puntos - j) / num_bajada) * 40)
            else:
                dz.insert(cdt[trazo] + j + 1, pz - 40)
        for j in range(10):
            dx.insert(cdt[trazo] + num_puntos + j + 1, x_fin)
            dy.insert(cdt[trazo] + num_puntos + j + 1, y_fin)
            dz.insert(cdt[trazo] + num_puntos + j + 1, pz)
        print dz
            # print 'subida'
            # print x_ini - x_fin, y_ini  - y_fin
            # print dx[cdt[i]:cdt[i] + 2 + num_puntos + 10]
            # print dy[cdt[i]:cdt[i] + 2 + num_puntos + 10]
            # print dz[cdt[i]:cdt[i] + 2 + num_puntos + 10]
    return dx, dy, dz


def conversion_angulos(dx, dy, dz):
    # convierte puntos cartesianos en angulos del motor.
    ang1 = []
    ang2 = []
    ang3 = []
    for i in range(len(dx)):
        angulos = dk.inverse(-dx[i], -dy[i], -dz[i])
        ang1.append(round(angulos[1], 1))
        ang2.append(round(angulos[3], 1))
        ang3.append(round(angulos[2], 1))
    print ang1
    print ang2
    print ang3
    plt.subplot(3, 1, 1)
    plt.plot(ang1)
    plt.subplot(3, 1, 2)
    plt.plot(ang2)
    plt.subplot(3, 1, 3)
    plt.plot(ang3)
    return ang1, ang2, ang3


def generar_pulsos(ang, dibujar):
    # convierte la trayectoria de posicion angular del motor en pulsos de stepper
    # return: pf (tren de pulsos forward), pb (tren de pulsos backwards)
    step = 1.8/8
    pf = [0]
    pb = [0]
    inc = 0.0
    for i in range(1, len(ang)):
        inc = inc + ang[i] - ang[i - 1]
        if inc >= step:
            pf.append(1)
            pb.append(0)
            inc -= step
        elif inc <= step:
            pf.append(0)
            pb.append(1)
            inc += step
        else:
            pf.append(0)
            pb.append(0)
    print 'incremento residual: %r' % inc
    #dibujar:
    if dibujar != 0:
        abs = 0.0
        plt.subplot(3, 1, dibujar)
        # plt.plot(ang1)
        for k in range(len(pf)):
            if pf[k] == 1:
                abs += step
            if pb[k] == 1:
                abs -= step
            plt.plot(k, abs, 'ro')
        # plt.show()
    return pf, pb


def generar_pulsos_2(ang1, ang2, ang3, dibujar):
    # convierte la trayectoria de posicion angular del motor en pulsos de stepper
    # return: pf (tren de pulsos forward), pb (tren de pulsos backwards)
    step = 1.8/8
    pf1 = [0]
    pb1 = [0]
    pf2 = [0]
    pb2 = [0]
    pf3 = [0]
    pb3 = [0]
    inc1 = 0.0
    inc2 = 0.0
    inc3 = 0.0
    for i in range(1, len(ang1)):
        inc1 = inc1 + ang1[i] - ang1[i - 1]
        inc2 = inc2 + ang2[i] - ang2[i - 1]
        inc3 = inc3 + ang3[i] - ang3[i - 1]
        while True: # inc1 >= step or inc2 >= step or inc3 >= step:
            if inc1 >= step:
                pf1.append(1)
                pb1.append(0)
                inc1 -= step
            elif inc1 <= step:
                pf1.append(0)
                pb1.append(1)
                inc1 += step
            else:
                pf1.append(0)
                pb1.append(0)
            # 2
            if inc2 >= step:
                pf2.append(1)
                pb2.append(0)
                inc2 -= step
            elif inc2 <= step:
                pf2.append(0)
                pb2.append(1)
                inc2 += step
            else:
                pf2.append(0)
                pb2.append(0)
            # 3
            if inc3 >= step:
                pf3.append(1)
                pb3.append(0)
                inc3 -= step
            elif inc3 <= step:
                pf3.append(0)
                pb3.append(1)
                inc3 += step
            else:
                pf3.append(0)
                pb3.append(0)
            if inc1 < step*2 and inc2 < step*2 and inc3 < step*2:
                break
    print 'incremento residual: %r' % inc1
    print 'incremento residual: %r' % inc2
    print 'incremento residual: %r' % inc3
    # dibujar:
    if dibujar != 0:
        abs = 0.0
        plt.subplot(3, 1, 1)
        # plt.plot(ang1)
        for k in range(len(pf1)):
            if pf1[k] == 1:
                abs += step
            if pb1[k] == 1:
                abs -= step
            plt.plot(k, abs, 'ro')
        abs = 0.0
        plt.subplot(3, 1, 2)
        # plt.plot(ang1)
        for k in range(len(pf2)):
            if pf2[k] == 1:
                abs += step
            if pb2[k] == 1:
                abs -= step
            plt.plot(k, abs, 'ro')
        abs = 0.0
        plt.subplot(3, 1, 3)
        # plt.plot(ang1)
        for k in range(len(pf3)):
            if pf3[k] == 1:
                abs += step
            if pb3[k] == 1:
                abs -= step
            plt.plot(k, abs, 'ro')
        # plt.show()
    return pf1, pb1, pf2, pb2, pf3, pb3


def aproximacion_inicial(a1, a2, a3):
    # anyade aproximacion inicial para las trayectorias.
    longi = np.ceil(max(max(a1[0], a2[0]), a3[0])/0.1)
    l1 = list(np.arange(0, a1[0], a1[0]/longi))
    l1 = [round(elem, 2) for elem in l1]
    l2 = list(np.arange(0, a2[0], a2[0]/longi))
    l2 = [round(elem, 2) for elem in l2]
    l3 = list(np.arange(0, a3[0], a3[0]/longi))
    l3 = [round(elem, 2) for elem in l3]
    if len(l1) != len(l2) or len(l1) != len(l3) or len(l2) != len(l3):
        print 'liada'
    if len(l1) != longi:
        print 'liada1'
        l1.pop()
    sal1 = l1 + a1
    sal2 = l2 + a2
    sal3 = l3 + a3
    return sal1, sal2, sal3


def mover(ori1, ori2, ori3, dest1, dest2, dest3):
    longi = 200.0
    l1 = list(np.arange(ori1, dest1, (dest1 - ori1) / (longi-1)))
    l1 = [round(elem, 2) for elem in l1]
    l1.append(dest1)
    l2 = list(np.arange(ori2, dest2, (dest2 - ori2) / (longi-1)))
    l2 = [round(elem, 2) for elem in l2]
    l2.append(dest2)
    l3 = list(np.arange(ori3, dest3, (dest3 - ori3) / (longi-1)))
    l3 = [round(elem, 2) for elem in l3]
    l3.append(dest3)
    if len(l1) != len(l2) or len(l1) != len(l3) or len(l2) != len(l3):
        print 'error. longitudes diferentes!'
    if len(l1) != longi:
        l1.pop()
    return l1, l2, l3


def salida_final(a1, a2, a3, tipo):
    #levanta el actuador al final de la trayectoria.
    p, p1, p2, p3 = dk.forward(a1[-1], a2[-1], a3[-1])
    pun_ini = [p1, p2, p3]
    inc = 40.0
    dim = 100
    p_x = [pun_ini[0] for indice in range(dim)]
    p_y = [pun_ini[1] for indice in range(dim)]
    p_z = [pun_ini[2] - indice * inc / dim for indice in range(dim)]
    s1, s2, s3 = conversion_angulos(p_x, p_y, p_z)
    sal1 = a1 + s1
    sal2 = a2 + s2
    sal3 = a3 + s3
    if tipo == 1:
        #levanta y despues vuelve al origen.
        o1, o2, o3 = mover(s1[-1], s2[-1], s3[-1], 0, 0, 0)
        sal1 += o1
        sal2 += o2
        sal3 += o3
    return sal1, sal2, sal3


def division_pulsos(p):
    #Agrupa de 8 en 8 los pulsos para enviarlos como integer.
    p_int = []
    for i in range(len(p) / 8):
        cadena = ''
        for j in range(i * 8, (i + 1) * 8):
            cadena += str(p[j])
        # print cadena
        # print int(cadena, 2)
        p_int.append(int(cadena, 2))
    return p_int


if __name__ == '__main__':
    #inkscape simplified
    # archivo = "/home/esaii/Desktop/pruebas_potrace/cara_chico.svg"
    # archivo = "/home/esaii/Desktop/pruebas_potrace/circulo.svg"
    # archivo = "/home/esaii/Desktop/pruebas_potrace/test_simplified.svg"
    #sin inkscape
    archivo = "/home/esaii/Desktop/pruebas_potrace/borralla/careto.svg"
    # imagenes simplificadas ocn inkscape:
    r = extraer_recorridos(archivo)
    pz = 215  # coordenada z del dibujo
    try:
        dx, dy, cdt = dimensionado(r, 200, 180, 1) #cdt: cambio de trazo
        dz = [pz]*len(dx)

        ######### working here
        print cdt
        # ANYADE PUNTOS DE SUBIDA EN LOS CAMBIOS DE TRAZO:
        dx, dy, dz = cambios_trazo(dx, dy, dz, cdt)
        # dx, dy, dz = entrada_inicial(dx, dy, dz)
        print dz
        quit()
        ####################

        # CONVERTIR PUNTOS EN ANGULOS DEL MOTOR
        ang1, ang2, ang3 = conversion_angulos(dx, dy, dz)

        # APROXIMACION AL PUNTO INICIAL:
        ang1, ang2, ang3 = aproximacion_inicial(ang1, ang2, ang3)

        # SALIDA FINAL:
        ang1, ang2, ang3 = salida_final(ang1, ang2, ang3, 1)

        # PRODUCIR TRENES DE PULSOS PARA CADA MOTOR

        # f1, b1 = generar_pulsos(ang1, 1)
        # f2, b2 = generar_pulsos(ang2, 2)
        # f3, b3 = generar_pulsos(ang3, 3)
        # # si hay mucho residuo habria que mejorar la funcion teniendo con ampliaciones intermedias para dar tiempo a
        # # movimientos largos. Realizar plot absoluto. Inicio! posicion inicial!
        #
        # plt.show()

        f1, b1, f2, b2, f3, b3 = generar_pulsos_2(ang1, ang2, ang3, 1)
        print 'longitud f1 %r' % len(f1)
        print len(f2)
        print len(f3)

        plt.show()

        #ENVIAR TRENES DE PULSOS:

        # agrupar por bytes

        l = np.ceil(len(f1)/8.0)*8
        # print l-len(f1)

        for i in range(int(l-len(ang1))):
            f1.append(0)
            f2.append(0)
            f3.append(0)
            b1.append(0)
            b2.append(0)
            b3.append(0)

        f1_int = division_pulsos(f1)
        f2_int = division_pulsos(f2)
        f3_int = division_pulsos(f3)
        b1_int = division_pulsos(b1)
        b2_int = division_pulsos(b2)
        b3_int = division_pulsos(b3)

        print len(f1_int)
        print f1_int
        print len(b1_int)
        print b1_int
        print len(f2_int)
        print f2_int
        print len(b2_int)
        print b2_int
        print len(f3_int)
        print f3_int
        print len(b3_int)
        print b3_int


    except:
        print 'error'
