import pygame
from Diccionario import*
from funciones_logica import *  # Importa el módulo con las funciones de lógica
from constantes import *

pygame.init()

PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
clock = pygame.time.Clock()
fuente = pygame.font.Font(None, 30)


icono = pygame.image.load("Recursos\elabc.png")
pygame.display.set_icon(icono)

pygame.display.set_caption("Descubre las Palabras") #nombre ventana



while bandera:

    clock.tick(FPS)
    letras_superiores, letras_inferiores = inicializar_letras_y_en_intervalos()

    num_letras_inferiores = len([letra for letra in letras_inferiores if letra["letra"]]) #contamos cuantas letras hay en el rectangulo inferior
    mostrar_boton_ingresar = num_letras_inferiores >= 3

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            bandera = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pygame.mixer.music.load( "Recursos\click.mp3") 
            pygame.mixer.music.play(0)

            # colidepoint es nuestra colision con los botones
            if boton_shuffle.collidepoint(event.pos):
                shuffle_superiores(letras_superiores) # el cambio de orden en las letras
                pygame.mixer.music.load( "Recursos\erandom.mp3") 
                pygame.mixer.music.play(0)

            if boton_cruz2.collidepoint(event.pos):
                        estado_actual = 8#pasamos al estado final

                        sonido_borrar2 = pygame.mixer.Sound("Recursos\eborrar.mp3")

                        
                        sonido_borrar2.play()                        
                        

            if boton_tilde2.collidepoint(event.pos):
                        estado_actual = (estado_actual + 1) % len(estados)
                        tiempo_inicial = tiempo_actual = 0
                        pygame.mixer.music.load( "Recursos\eacierto.mp3") 
                        pygame.mixer.music.play(0)

            apretar_letra(event)# lo que sería la colision del click

            if boton_borrar.collidepoint(event.pos): # el tacho de basura
                borrar_letras_superiores_e_inferiores(letras_superiores, letras_inferiores)
                sonido_borrar = pygame.mixer.Sound("Recursos\eborrar.mp3")

                sonido_borrar.play()
                
                sonido_borrar.play(1)


            if mostrar_boton_ingresar and boton_ingresar.collidepoint(event.pos):
                palabra_formada = obtener_palabra_inferior(letras_inferiores) #la lectura de la palabra de abajo
                
                # leemos las palabras compatibles desde el archivo JSON
                with open("palabras_compatibles.json", 'r') as archivo_compatibles:
                    datos_compatibles = json.load(archivo_compatibles)
                    palabras_compatibles = datos_compatibles.get("palabras_compatibles", [])

                # si hay concidencia de la palabra
                if palabra_formada in palabras_validas: # pero ya la habíamos puesto antes
                    palabras_invalidas.append(palabra_formada) 
                    tiempo_mostrar_cruz = pygame.time.get_ticks()  # Iniciar el temporizador para mostrar la cruz
                else: # si no la habíamos puesto antes 
                    if palabra_formada in palabras_compatibles: #y hay coincidencia
                        palabras_validas.append(palabra_formada)#almacenamos la lista de palabras validas
                        print(palabras_validas) 
                        tiempo_mostrar_tilde = pygame.time.get_ticks()  #temporizador para mostrar el tilde
                        pygame.mixer.music.load( "Recursos\eacierto.mp3") 
                        pygame.mixer.music.play(0)
                    else:
                        palabras_invalidas.append(palabra_formada)
                        tiempo_mostrar_cruz = pygame.time.get_ticks()  #temporizador para mostrar la cruz
                        pygame.mixer.music.load( "Recursos\error.mp3") 
                        pygame.mixer.music.play(0)
                        


                with open("palabras_validas.json", 'w') as archivo: #creamos un json modo escritura de las palabras validas
                    json.dump({"palabras_validas": palabras_validas}, archivo)


    tiempo_actual = pygame.time.get_ticks() // 1000 #contamos por cada 1000 milisegundos

    if tiempo_inicial is None: #si no hay tiempo
        tiempo_inicial = tiempo_actual

    estado = estados[estado_actual] #lecutra de estados para mi bucle

    match estado:
        case "final":
            # Muestra el mensaje "Tiempo Finalizado" en el centro
            tiempo_surface = fuente.render("Juego Finalizado", True, BLANCO, NEGRO)
            tiempo_rect = tiempo_surface.get_rect()
            tiempo_rect.center = (ANCHO // 2, ALTO // 2)
            #
            sistema = False
            puntaje = True
            pregunta = False
            
            


        case "inicio":
            pregunta = False
            sistema = False

            letras_superiores.clear() #quería usar la funcion borrar q contenía a las 2 pero me fallaba
            letras_inferiores.clear()


            tiempo_restante = tiempo_intervalo - (tiempo_actual - tiempo_inicial)
            tiempo_surface = fuente.render(f"Cargando", True, BLANCO, NEGRO)

            #condicion para cambio de estado 
            if tiempo_actual - tiempo_inicial >= tiempo_intervalo:
                estado_actual = (estado_actual + 1) % len(estados)
                tiempo_inicial = tiempo_actual
        
        case "fase":
            pregunta = False

            if tiempo_inicial is None:
                tiempo_inicial = tiempo_actual

            sistema = True

            tiempo_restante = 30 - (tiempo_actual - tiempo_inicial)
            
            tiempo_surface = fuente.render(f"Ronda: {tiempo_restante}", True, BLANCO, NEGRO) # mi reloj para el case fase

            y_validas = ALTO - 50
            for palabra_valida in palabras_validas:
                mostrar_informacion(palabra_valida, ANCHO // 4, y_validas)
                y_validas += 30

            if tiempo_actual - tiempo_inicial >= 30:
                estado_actual = (estado_actual + 1) % len(estados)
            
        case "pregunta":
            sistema = False
            pregunta = True
            tiempo_inicial = tiempo_actual = 0


    PANTALLA.fill(NEGRO)

    if pregunta:
        mostrar_informacion("¿Quieres jugar otra ronda?", 200, 200) #cuadro

        # generamos nuevas posiciones porque las de los botones tilde y cruz se superponian
        x_boton_tilde = ANCHO // 3
        x_boton_cruz = (2 * ANCHO) // 3
   

        # Configura el rectángulo para el botón de la tilde
        boton_tilde2 = pygame.Rect(x_boton_tilde, ALTO // 2, 100, 100)

        # Configura el rectángulo para el botón de la cruz
        boton_cruz2 = pygame.Rect(x_boton_cruz, ALTO // 2, 100, 100)

        # funciones dibujado
        pygame.draw.rect(PANTALLA, BLANCO, boton_tilde2)
        PANTALLA.blit(imagen_tilde2, boton_tilde2.topleft)

        pygame.draw.rect(PANTALLA, BLANCO, boton_cruz2)
        PANTALLA.blit(imagen_cruz2, boton_cruz2.topleft)

    if sistema:
        rectangulo_superior = pygame.Rect(0, 0, ANCHO, 100)
        pygame.draw.rect(PANTALLA, BLANCO, rectangulo_superior)
        rectangulo_inferior = pygame.Rect(0, 150, ANCHO, 100)
        pygame.draw.rect(PANTALLA, BLANCO, rectangulo_inferior)

        dibujar_letras(letras_superiores, PANTALLA)
        dibujar_letras(letras_inferiores, PANTALLA)

        PANTALLA.blit(imagen_shuffle, boton_shuffle)
        PANTALLA.blit(imagen_borrar, boton_borrar)

        if mostrar_boton_ingresar:
            PANTALLA.blit(imagen_ingresar, boton_ingresar)

        mostrar_palabras_validas(palabras_validas, PANTALLA)

        tiempo_mostrar_tilde = mostrar_imagen_temporal(tiempo_mostrar_tilde, tiempo_mostrar_tilde_duracion, imagen_tilde, boton_tilde)
        tiempo_mostrar_cruz = mostrar_imagen_temporal(tiempo_mostrar_cruz, tiempo_mostrar_cruz_duracion, imagen_cruz, boton_cruz)

    if puntaje:
        
        pygame.mixer.music.load( "Recursos\puntaje.mp3" ) 
        pygame.mixer.music.play(-1)
        cantidad_letras_validas = len(palabras_validas)
        mostrar_informacion(f"Cantidad de palabras válidas: {cantidad_letras_validas}", 100, 100)

        palabras_por_longitud = {}
        for palabra in palabras_validas:
            longitud = len(palabra)
            palabras_por_longitud[longitud] = palabras_por_longitud.get(longitud, 0) + 1#obtenemos la cantidad de palabras diferencias por su len(suma las q tienen el mismo tamaño en listas)
        y_actual = (ALTO // 2) + 10
        for longitud, cantidad in palabras_por_longitud.items(): #a cada len distinto via items le vamos a poner crear un cuadro con sus datos correspondientes
            mostrar_informacion(f"Palabras de {longitud} caracteres: {cantidad}", ANCHO // 4, y_actual)
            y_actual += 30  # Espacio entre cantidades

        # Calcula el puntaje final y muestra la información
        puntaje_final = sum([longitud * cantidad for longitud, cantidad in palabras_por_longitud.items()])
        mostrar_informacion(f"Puntaje Final: {puntaje_final}", ANCHO - 200, ALTO - 50)

    else:
        # Renderiza el tiempo en la esquina inferior derecha
        tiempo_rect = tiempo_surface.get_rect()
        tiempo_rect.bottomright = (ANCHO - 10, ALTO - 10) #coordenadas del reloj
        PANTALLA.blit(tiempo_surface, tiempo_rect.topleft)

    pygame.display.update()

pygame.quit()

