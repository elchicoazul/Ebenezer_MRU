import cv2
import numpy as np
import pygame
import sys

# Inicializar Pygame
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MRU Simulation")

# Cargar la imagen del carrito en Pygame
carrito_image = pygame.image.load('D:\\Laboratorio-de-fisica-con-realidad-aumentada-Eben\\backend\\car.png')  # Asegúrate de poner la ruta correcta de la imagen
carrito_image = pygame.transform.scale(carrito_image, (50, 50))

# Configuración de OpenCV
cap = cv2.VideoCapture(0)
aruco = cv2.aruco

    # Cargar el diccionario ArUco que corresponde con el marcador que se usará
    # Nota: En algunas versiones puede ser necesario acceder al diccionario de esta manera
   # Cargar el diccionario ArUco que corresponde con el marcador que se usará
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_7X7_100)

    # Intentar crear una instancia de DetectorParameters
try:
    parameters = aruco.DetectorParameters_create()
except AttributeError:
        # Si la función no está disponible, use la clase directamente
    parameters = aruco.DetectorParameters()

car_speed = 20  # Velocidad del carrito

# Lista de marcadores virtuales
virtual_markers = []

# Función para convertir imagen de OpenCV a Pygame
def cvimage_to_pygame(image):
    """Convertir imagen de OpenCV a imagen de Pygame."""
    return pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], "RGB")

# Variables de control
car_pos = None
target_pos = None

running = True
while running:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir a RGB para Pygame
    pygame_frame = cvimage_to_pygame(frame)
    screen.blit(pygame_frame, (0, 0))

    # Convertir frame a escala de grises y detectar marcadores
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        print("Marcadores detectados:", ids)
        for i, corner in zip(ids.flatten(), corners):
            if i == 0:  # ID del primer marcador
                car_pos = np.mean(corner[0], axis=0).astype(int)
                print("Posición del carrito:", car_pos)
            elif i == 1:  # ID del segundo marcador
                target_pos = np.mean(corner[0], axis=0).astype(int)
                print("Posición del objetivo:", target_pos)
    else:
        print("No se detectaron marcadores")

    # Añadir marcadores virtuales al hacer clic con el mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Añadir un marcador virtual en la posición del clic
            x, y = pygame.mouse.get_pos()
            virtual_markers.append((x, y))
            print("Marcador virtual añadido en:", x, y)

    # Dibujar todos los marcadores virtuales
    for marker in virtual_markers:
        pygame.draw.circle(screen, (255, 0, 0), marker, 10)  # Dibuja un círculo rojo para cada marcador virtual

    # Mover el carrito hacia el marcador ID 1
    if car_pos is not None and target_pos is not None:
        move_vector = np.array(target_pos) - np.array(car_pos)
        move_distance = np.linalg.norm(move_vector)

        if move_distance > car_speed:
            move_vector = (car_speed * move_vector / move_distance).astype(int)
        car_pos += move_vector

        # Superponer la imagen del carrito en la nueva posición
        car_rect = carrito_image.get_rect(center=(car_pos[0], car_pos[1]))
        screen.blit(carrito_image, car_rect)

    # Actualizar la pantalla
    pygame.display.flip()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Limpieza
cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()

