import pygame
pygame.init()
bandera = True

ANCHO = 800
ALTO = 600
FPS = 30
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))


# Definir los estados del juego
estados = ["inicio", "fase", "final"]#este es el patron loop q hace mi codigo
inicio = ["inicio", "inicio2","inicio3"];
preguntas = ["pregunta","pregunta2"]
estado = estados[0]
estado_actual = estado



# Cargar letras iniciales
letra_size = 60
espacio_entre_letras = 40

num_letras = 6
total_ancho_letras = (letra_size + espacio_entre_letras) * num_letras #calculo distancia entre letras

# Calcular x_inicial
x_inicial = (ANCHO - total_ancho_letras) // 2

# Variables para rastrear las letras seleccionadas
letras_seleccionadas = [False] * num_letras

#mis letras nacieron vacias y fueron llenadas en las funciones
letras_info = []
letras_superiores = []  
letras_inferiores = []  

palabras_validas = []
palabras_invalidas = []


# Inicializa las variables de tiempo y estado
tiempo_intervalo =3
tiempo_actual = 0
tiempo_inicial = 0  # Inicializa tiempo_inicial a cero
estado_actual = 0
#originalmente tenía un tiempo fase pero no respondía bien

tiempo_surface = None  # esta orientada al dibujado del reloj

sistema = False  # Inicializa sistema al comienzo del bucle

origen = "palabras_compatibles.json"
destino = "puntuacion_final.json."
    


palabras_formadas = []


tiempo_mostrar_tilde = None  
tiempo_mostrar_tilde_duracion = 500 
tiempo_mostrar_cruz = None  
tiempo_mostrar_cruz_duracion = 500 



pygame.init()


imagen_shuffle = pygame.image.load("Recursos\shuffle.jpg")
imagen_shuffle = pygame.transform.scale(imagen_shuffle, (100, 100))
boton_shuffle = pygame.Rect(ANCHO - 100, 0, 100, 100)


imagen_borrar = pygame.image.load("Recursos\sborrar.png")
imagen_borrar = pygame.transform.scale(imagen_borrar, (100, 100))
boton_borrar = pygame.Rect(ANCHO - 100, 150, 100, 100)  # Ajusta las coordenadas aquí

imagen_ingresar = pygame.image.load("Recursos\ingresar.png")
imagen_ingresar = pygame.transform.scale(imagen_ingresar, (300, 100))
boton_ingresar = pygame.Rect((ANCHO) / 2, (ALTO / 2) ,300,100)

imagen_tilde = pygame.image.load("Recursos\stilde.png")
imagen_tilde = pygame.transform.scale(imagen_tilde, (100, 100))
boton_tilde = pygame.Rect((ANCHO) / 2, (ALTO -150) ,0,500)

imagen_cruz = pygame.image.load("Recursos\cruz.png")
imagen_cruz = pygame.transform.scale(imagen_cruz, (100, 100))
boton_cruz = pygame.Rect((ANCHO) / 2, (ALTO -150) ,50,500)

imagen_tilde2 = pygame.image.load("Recursos\stilde.png")
imagen_tilde2 = pygame.transform.scale(imagen_tilde2, (100, 100))
boton_tilde2 = pygame.Rect((ANCHO) / 2, (ALTO / 2) ,0,500)

imagen_cruz2 = pygame.image.load("Recursos\cruz.png")
imagen_cruz2 = pygame.transform.scale(imagen_cruz2, (100, 100))
boton_cruz2 = pygame.Rect((ANCHO) / 2, (ALTO -150) ,50,500)

sonido_borrar2 = pygame.mixer.Sound("Recursos\eborrar.mp3")





puntaje = False
