from Diccionario import*
import json
import pygame
from random import shuffle
from constantes import *

#llamamos al diccionario 
def cargar_letras_json(): #el objetivo de esta función mas que nada era crear retornables en logica.py e intentar vincular el valor con su dibujado en pygame
    diccionario() 

    global lista_letras_json  # pedimos por la global de letras anterior

    try:#intetamos leer el json de palabras compatibles e igualamos cada letra elegida
        with open("palabras_compatibles.json", "r", encoding="utf-8") as entrada_json:
            datos = json.load(entrada_json)
            letras_elegidas = datos["letras_elegidas"]
            lista_letras_json = letras_elegidas  # Asigna los valores correctamente
            return lista_letras_json
    except FileNotFoundError:
        lista_letras_json = []  # Establece una lista vacía en caso de excepción

def inicializar_letras_y_en_intervalos(): #esta funcion me sirve para solo realizar la carga de letras cuando no haya ninguna
    global letras_superiores, letras_inferiores  #llamamos a las globales
    
    if not letras_superiores and not letras_inferiores: #si no hay entnces las generamos
        lista_letras_json = cargar_letras_json()
        
        for i, letra in enumerate(lista_letras_json):   #en este bucle se enumera cada letra de la lista generada
            letra_info = {
                "letra": letra,
                "x": x_inicial + i * (letra_size + espacio_entre_letras),
                "y": 50,  # En el cuadro superior
                "rect": None,
            }
            letra_info["rect"] = pygame.Rect(letra_info["x"], letra_info["y"], letra_size, letra_size)
            letras_superiores.append(letra_info) #marcamos  sus coordenadas y estilo de dibujo

        for i in range(num_letras): # esta va a ser la distancia horizontal entre cada recta
            letra_info = {
                "letra": "",
                "x": x_inicial + i * (letra_size + espacio_entre_letras),
                "y": 200,  # En el cuadro inferior
                "rect": None,
            }
            letra_info["rect"] = pygame.Rect(letra_info["x"], letra_info["y"], letra_size, letra_size)
            letras_inferiores.append(letra_info)

    return letras_superiores, letras_inferiores #y lo retornamos 

def borrar_letras_superiores_e_inferiores(letras_superiores, letras_inferiores): #funcion para borrar los dibujos y almacenamiento de las letras(sirve en los intervalos)
    letras_superiores.clear()
    letras_inferiores.clear()


def apretar_letra(event): #esta función es para que al apretar click sobre una letra cambie su comportamiento entre palabra inferior o superior
    for i, letra_info in enumerate(letras_superiores):
        if letra_info["rect"].collidepoint(event.pos):#si es clickeado el dibujo de una letra
            if "" not in [letra_info["letra"] for letra_info in letras_inferiores]:
                continue #y hay espacio en el cuadro de abajo
            for j, letra_inferior in enumerate(letras_inferiores): #buscamos el espacio
                if letra_inferior["letra"] == "":
                    letras_inferiores[j]["letra"] = letra_info["letra"]
                    letras_superiores[i]["letra"] = ""
                    break #y lo transformamos


#el bloque se repite tanto para inferior como superior
    for i, letra_info in enumerate(letras_inferiores):
        if letra_info["rect"].collidepoint(event.pos):
            if "" not in [letra_info["letra"] for letra_info in letras_superiores]:
                continue
            for j, letra_superior in enumerate(letras_superiores):
                if letra_superior["letra"] == "":
                    letras_superiores[j]["letra"] = letra_info["letra"]
                    letras_inferiores[i]["letra"] = ""


def shuffle_superiores(letras_superiores):#luego de dibujar las letras intente cambiar el orden segun el boton así que con el shufle
    #aca revisa q las letras solo sean las del cuadro de arriba
    letras_actuales = [letra_info["letra"] for letra_info in letras_superiores]

    #u aca recien los mezcla
    random.shuffle(letras_actuales)

    # no solo basta con mezclar sino que hay que actualizar el lo que sería las letras superiroes para que se refleje en pygame
    for i, letra_info in enumerate(letras_superiores):
        letra_info["letra"] = letras_actuales[i]

#sin pygame init cualquier funcion que lleve pygame no funcionaria
pygame.init() 
fuente = pygame.font.Font(None, 36) #sin la fuente aca algunas funciones no respondían

def dibujar_letras(letras, superficie):#esta funcion es la que completa lo que es el manejo del dibujo y clickeado de las letras
    for letra_info in letras: #por cada letra q leamos
        letra_surface = fuente.render(letra_info["letra"].upper(), True, ROJO)
        letra_rect = letra_surface.get_rect()
        letra_rect.topleft = (letra_info["x"], letra_info["y"])
        pygame.draw.circle(superficie, AZUL, letra_rect.center, 28, 2)
        superficie.blit(letra_surface, letra_rect.topleft)
        #vamos a dibujarla, darle color y contorno, tambien su información correspondiente

def obtener_palabra_inferior(letras_inferiores): #esta funcion fue para tomar las letras del cuadro inferior y transformarlas en un string segun su orden
    palabra = "".join([letra_info["letra"] for letra_info in letras_inferiores])
    subir_letras_inferiores_a_superiores(letras_superiores, letras_inferiores)
    return palabra # y así poder ver q palabras estabamos formando


def subir_letras_inferiores_a_superiores(letras_superiores, letras_inferiores): #la tuve q crear porque originalmente solo podía pasar letras para el cuadro inferior pero en el juego si la apretabas abajo podian volver arriba
    for i, letra_info in enumerate(letras_superiores):
        if letra_info["letra"] == "":
            # Encuentra la primera letra vacía en el cuadro superior
            for j, letra_inferior in enumerate(letras_inferiores):
                if letra_inferior["letra"] != "":
                    # Sube la letra del cuadro inferior al superior
                    letras_superiores[i]["letra"] = letra_inferior["letra"]
                    letras_inferiores[j]["letra"] = ""
                    break


def mostrar_imagen_temporal(tiempo_inicio, duracion, imagen, rectangulo): #esta funcion trabaja lo q es la aparicion por tiempo de las imagenes
    tiempo_actual = pygame.time.get_ticks()# aca toma el tiempo 
    if tiempo_inicio is not None: 
        if tiempo_actual - tiempo_inicio <= duracion: #las condiciones para q aparezca la imagen
            PANTALLA.blit(imagen, rectangulo)
        else:
            tiempo_inicio = None  # Restablece tiempo_inicio cuando la duración ha transcurrido
    return tiempo_inicio



def mostrar_informacion(texto, x, y, color=BLANCO): # esta funcion me sirve para simplificar lo q es los textos del puntaje
    texto_superficie = fuente.render(texto, True, color, NEGRO)
    rectangulo_texto = texto_superficie.get_rect()
    rectangulo_texto.topleft = (x, y)
    PANTALLA.blit(texto_superficie, rectangulo_texto.topleft)


def mostrar_palabras_validas(palabras_validas, pantalla):
    x = 10
    y = ALTO - 150 

    pygame.draw.rect(pantalla, BLANCO, (x, y, ANCHO - 20, 100))  # Dibuja el cuadro blanco
    for palabra_valida in palabras_validas:
        palabra_surface = fuente.render(palabra_valida, True, NEGRO)
        pantalla.blit(palabra_surface, (x, y))

        x += palabra_surface.get_width() + 10  
        if x + palabra_surface.get_width() >= ANCHO - 20 or palabra_surface.get_width() >= ANCHO - 20:
            # Si la palabra está a punto de llegar al ancho final de la pantalla, baja el y
            y += 30
            x = 10
    if y < ALTO - 60:
        y = ALTO - 60  # Asegura que el rectángulo no se salga de la pantalla