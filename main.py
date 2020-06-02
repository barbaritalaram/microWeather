#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Capítulo de sensores climáticos, python, microservicios y más

@author: Barbarita Lara
"""
#Debemos importar todas los modulos que ocuparemos

import time
import serial
import subprocess
import hug
import threading

#definimos una función que permita adquirir los datos desde el microbit que está conectado en la raspberry pi
def adqData():
    #el módulo serial leerá el puerto USB a una velocidad en específico
    ser = serial.Serial('/dev/ttyACM0',115200)
    #flushInput se encargará de limpiar el buffer de cualquier residuo de información que haya quedado de pruebas anteriores
    ser.flushInput()
    #ahora comenzaremos un ciclo, que dice, así: mientras sea verdad, pasará lo siguiente
    while True: 
        #leeremos la linea que viene por el microbit
        line = ser.readline()
        #decodificaremos en utf-8
        decoded_line = line.decode("utf-8")
        #crearemos y abriremos un archivo de texto llamado data
        f = open("data.txt","a")
        #escribiremos el momento en que lleguen los datos gracias a time y luego concatenaremos los datos del microbit
        f.write(str(time.time())+(',')+decoded_line)
        #cerraremos el archivo para no tener problemas
        f.close()
#crearemos un hilo para poder estar constatemente adquiriendo datos
hilo = threading.Thread(target=(adqData), daemon=True)
#y luego partiremos el hilo
hilo.start()

#usaremos hug que dice ser la API del futuro
"""Genera código obvio, limpio y radicalmente simple.
Tiene un rendimiento sin igual. (Esto ya que se compila utilizando Cython, obteniendo todas las ventajas que esto conlleva)
Incorpora una sencilla y eficiente gestión de versiones para nuestras APIs. (Podemos exponer múltiples versiones de un API de forma sencilla)
Genera documentación automáticamente. (Gracias a que se vale de las cadenas de documentación y anotaciones de tipo que incluyamos en nuestro código)
Realiza validaciones utilizando las anotaciones de tipo.
Sigue la ideología de «Escribe una vez, usa en todas partes», ya que separa el API y la lógica de negocio que la expone, lo que significa que puede exponerse utilizando HTTP, línea de comandos y el propio intérprete de Python de una sola vez
~ Explicación de laesporadelhongo.com ~ """
@hug.get()
@hug.local()
#crearemos una función
def microWeather():
    #haremos un pequeño truco para leer la última linea del archivo data con un subproceso
    line = subprocess.check_output(['tail','-1','data.txt'])
    #decodificaremos nuevamente utf-8
    line = line.decode("utf-8")
    #haremos una lista para manejar mejor los datos. Este pedazo de código, va cortando de , en , y guardando en una lista
    line = list(line.split(","))
    
    #y la función retornará lo siguiente
    return {
        #una linea de debug para ver toda la lista y luego veremos campo por campo
       'usb_microbit'  : line,
       #tiempo
        'Time'  : line[0], 
       #temperatura 
        'Temperatura': line[1],
       #humedad 
        'Humedad'   : line[2],
       #presión 
        'Presión'   : line[3],
       #altitud 
        'Altitud'   : line[4],
       #humedad de la tierra 
        'Humedad Tierra' : line[5],
       #temperatura de la tierra 
        'Temperatura Tierra'    : line[6],
       #velocidad del viento
        'Velocidad Viento'  : line[7],
       #dirección del viento
        'Dirección Viento'  : line[8], 
       #lluvia 
        'Lluvia'    : line[9]
        } 
#eso es todo! si instalamos bien hug solo nos ayudará a exponer esta simple API       
if __name__ == '__main__':
    print('hola mundo')
