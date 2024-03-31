import json
import random
import string
import re

def quitar_acentos(palabra):
    # vamos filtrando desde el txt al csv así no hay problemas futuros
    equivalencias = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'
    }
    
    palabra_sin_acentos = ''.join(equivalencias.get(c, c) for c in palabra)
    
    return palabra_sin_acentos


def abrir_archivo(txt_inicial):  #abrimos el txt
    lista_longitud = [] #creamos lista
    with open(txt_inicial, 'r', encoding='utf-8') as entrada: #lo leemos en modo lectura
        for linea in entrada: #por cada linea 
            palabra = linea.strip()
            palabra_sin_acentos = quitar_acentos(palabra)
            if 3 <= len(palabra_sin_acentos) <= 6: #solo nos quedamos con los que tengan esta longitud
                lista_longitud.append(palabra_sin_acentos)
    return lista_longitud #retornamos la lista

def convertir_a_csv(txt_inicial, csv_generado): # el propopisto es que se haga un csv del segundo parametro, segun lo puesto en el primer parametro
    palabras = abrir_archivo(txt_inicial) #usamos la funcion anterior

    with open(csv_generado, 'w+', newline='', encoding='utf-8') as salida: #generamos el csv, w+ para modo escritura lectura y utf para q acepte caracteres con acento
        for palabra in palabras:
            salida.write(palabra + '\n')  #Agregamos el salto de linea para diferenciar



def elegir_letras_random(cantidad=6):
    alfabeto = string.ascii_lowercase  # Obtenemos el alfabeto en minúsculas
    vocales = 'aeiou'  # Definimos las vocales

    while True:
        letras_al_azar = ''.join(random.sample(alfabeto, cantidad)) # metemos de forma aleatoria las letras del alfabeto
        if len(re.findall(f"[{vocales}]", letras_al_azar)) >= 2: #aseguramos que al menos tengamos 2 vocales(en el juego de ejemplo siempre habían 2 vocales)
            break # solo en caso de tener 2 vocales salimos del bloque

    letras_al_azar = list(letras_al_azar)  # la convertimos en una lista para poder cambiar su orden a futuro

    return letras_al_azar #guardamos las letras generadas


def encontrar_letras_compatibles(csv_generado):
    palabras_compatibles = []
    lista_letras = []

    while not palabras_compatibles:
        letras_al_azar = elegir_letras_random() #generamos letras randoms hasta romper el bucle

        with open(csv_generado, 'r', encoding='utf-8') as entrada:
            lineas = entrada.readlines()  # Leemos todas la lineas del csv

        for linea in lineas:#en cada linea
            palabra = linea.strip()  
            if (all(letra in palabra for letra in letras_al_azar)): #si hay una coincidencia de todas las letras
                lista_letras = letras_al_azar #guardamos la lista de letras a usar a futuro
                palabras_compatibles.append(palabra) #añadimos una palabra a la lista para romper el bucle

    # for palabra in palabras_compatibles:  
    #     print(palabra)

    # if lista_letras is not None:
    #     print(f"Las letras compatibles son: {lista_letras}")

    #estos comentarios sirven de referencia para ver q esta bien todo en la terminal
    
    return lista_letras #retornamos la las letras que usaremos en el programa


lista_letras_json = None
palabras_formadas = []

def crear_json(): #para finalmente crear nuestro json
    global lista_letras_json #las letras voy a cambiarlas seguido en el cambiode estado asi q mejor la trato como el datos normalizados del stark

    lista_letras_json = encontrar_letras_compatibles('ListaPalabras.csv')

    if lista_letras_json is not None: #cuando encuentre letras compatibles con la funcion anterior arrancamos
        archivo_json = "palabras_compatibles.json"
        palabras_compatibles = []

        with open('ListaPalabras.csv', 'r', encoding='utf-8') as entrada: #abrimos en modo lectura
            for linea in entrada:
                palabra = linea.strip().lower()
                if all(letra in lista_letras_json for letra in palabra):#si todas las letras estan en nuestras lestras generadas
                    palabras_compatibles.append(palabra) #agregamos la palabra

        datos = {
            "letras_elegidas": lista_letras_json,
            "palabras_compatibles": palabras_compatibles,
            "palabras_formadas": palabras_formadas
        }

        with open(archivo_json, 'w+', encoding='utf-8') as salida: #mi salida va a ser la escritura 
            json.dump(datos, salida, ensure_ascii=False, indent=4)


#cesta fue la mejor manera que encontre para poder exportar estas 2 funciones que necesito a otros archivos de la carpeta
def diccionario():
    convertir_a_csv('diccionarioRAE.txt', 'ListaPalabras.csv')
    crear_json()
#esta fue porque sino figuraba 2 veces que realizaba la acción
if __name__ == "__main__":
    diccionario()