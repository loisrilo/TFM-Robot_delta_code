#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from tfm_delta.msg import Pulsos
from std_msgs.msg import UInt16
from tfm_delta.msg import trayectorias

from time import sleep

from svg.path import parse_path
import numpy as np
import matplotlib.pyplot as plt
from lxml import etree
import delta_kinematics as dk
import itertools


envio = trayectorias()

f1_int = []
f2_int = []
f3_int = []
b1_int = []
b2_int = []
b3_int = []








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
        # if str(type(path[curva])) == "<class 'svg.path.path.Line'>":  # if wanted...
            # ignorar (escribir accion si necesario)
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
    for i in range(len(r)):
        px, py = puntos_contorno(r[i], 1, 0.01) #0.05
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
        px, py = puntos_contorno(r[i], escala, 0.01) #0.05
        px = list(itertools.chain.from_iterable(px))
        py = list(itertools.chain.from_iterable(py))
        dib_x.append(px)
        dib_y.append(py)
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
    return dib_x, dib_y


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


def aproximacion_inicial(a1, a2, a3):
    # anyade aproximacion inicial para las trayectorias.
    longi = np.ceil(max(max(a1[0], a2[0]), a3[0])/0.1)
    l1 = list(np.arange(0, a1[0], a1[0]/longi))
    l1 = [round(elem, 2) for elem in l1]
    l2 = list(np.arange(0, a2[0], a2[0]/longi))
    l2 = [round(elem, 2) for elem in l2]
    l3 = list(np.arange(0, a3[0], a3[0]/longi))
    l3 = [round(elem, 2) for elem in l3]
    print l1
    print l2
    print l3
    sal1 = l1 + a1
    sal2 = l2 + a2
    sal3 = l3 + a3
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





# sinusoide 180:
#tra_f = [63,255,255,255,255,127,223,190,247,119,109,173,106,170,148,146,68,33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#tra_b = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,34,36,146,149,85,90,219,109,221,239,191,127,191,255,251,255,255,225]

# sinusoide 90:
tra_f = [63,255,255,191,119,109,106,146,68,0,0,0,0,0,0,0,0,0,0,0]
tra_b = [0,0,0,0,0,0,0,0,0,0,0,4,146,171,109,189,247,255,239,254]

# aproximacion y circulo:
cir_f1 = [0,0]
cir_b1 = [0,0]
cir_f2 = [0,0]
cir_b2 = [0,0]
cir_f3 = [0,0]
cir_b3 = [0,0]

# recibe trayectorias:
trayec = trayectorias()











pulso_test = Pulsos()
def nopulses():
    pulso_test.id = int(0)
    pulso_test.p1f = int(0)
    pulso_test.p1b = int(0)
    pulso_test.p2f = int(0)
    pulso_test.p2b = int(0)
    pulso_test.p3f = int(0)
    pulso_test.p3b = int(0)


def callback(data):
    global trayec
    trayec = data
    cir_f1 = data.f1
    cir_b1 = data.b1
    cir_f2 = data.f2
    cir_b2 = data.b2
    cir_f3 = data.f3
    cir_b3 = data.b3
    rospy.loginfo('recibido')


def talker():
    rospy.init_node('generador_pulsos', anonymous=False)
    rospy.loginfo('estoy aqui')
    pub = rospy.Publisher('trenes_pulsos', Pulsos, queue_size=10)
    pub2 = rospy.Publisher('num_pulso', UInt16, queue_size=10)
    rate = rospy.Rate(15.625/2) # 10hz
    i = 0
    sleep(5)
    while not rospy.is_shutdown():
        pulso_test.id = i
        pulso_test.p1f = f1_int[i-1]
        pulso_test.p1b = b1_int[i-1]
        pulso_test.p2f = f2_int[i-1]
        pulso_test.p2b = b2_int[i-1]
        pulso_test.p3f = f3_int[i-1]
        pulso_test.p3b = b3_int[i-1]
        if i < len(f1_int): # len(tra_f) para sinusoide   (aantes cir_f1) trayec.f1
            rospy.loginfo(i)
            i += 1
        # if i >= len(tra_f):
        #     nopulses()
        #     rospy.loginfo('trayectoria finalizada')
        pub.publish(pulso_test)
        if i >= len(f1_int): # len(tra_f) para sinusoide   (aantes cir_f1) trayec.f1
            nopulses()
            rospy.loginfo('trayectoria finalizada')
        pub2.publish(i)
        rate.sleep()



if __name__ == '__main__':
    archivo = "/home/esaii/Desktop/pruebas_potrace/cara_chico.svg"
    # archivo = "/home/esaii/Desktop/pruebas_potrace/circulo.svg"
    # archivo = "/home/esaii/Desktop/pruebas_potrace/test_simplified.svg"
    r = extraer_recorridos(archivo)
    pz = 200  # coordenada z del dibujo
    try:
        dx, dy = dimensionado(r, 200, 180, 1)
        #CONVERTIR PUNTOS EN ANGULOS DEL MOTOR
        dz = 210
        ang1 = []
        ang2 = []
        ang3 = []
        for i in range(len(dx)):
            angulos = dk.inverse(-dx[i], -dy[i], -dz)
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
        # plt.show()


        #APROXIMACION AL PUNTO INICIAL:

        print 'hola'
        print ang1[0], ang2[0], ang3[0]
        ang1, ang2, ang3 = aproximacion_inicial(ang1, ang2, ang3)



        #PRODUCIR TRENES DE PULSOS PARA CADA MOTOR

        f1, b1 = generar_pulsos(ang1, 1)
        f2, b2 = generar_pulsos(ang2, 2)
        f3, b3 = generar_pulsos(ang3, 3)
        # si hay mucho residuo habria que mejorar la funcion teniendo con ampliaciones intermedias para dar tiempo a
        # movimientos largos. Realizar plot absoluto. Inicio! posicion inicial!

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

        talker()

    except rospy.ROSInterruptException:
        pass