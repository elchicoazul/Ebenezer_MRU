import cv2
import cv2.aruco as aruco
import numpy as np



# Asegúrese de que cv2.aruco está disponible
if hasattr(cv2, 'aruco'):
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

    # Cargar la imagen del carrito
    carrito_image = cv2.imread('D:\\Laboratorio-de-fisica-con-realidad-aumentada-Eben\\backend\\car.png', cv2.IMREAD_UNCHANGED)


    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    car_width, car_height = 50, 50

    # Posiciones iniciales y finales del carrito (se inicializan como None)
    car_pos = None
    target_pos = None

    # Velocidad de movimiento del carrito (puede ajustar según necesite)
    car_speed = 2
    def overlay_image_alpha(img, img_overlay, x, y, alpha_mask):
        """Superpone img_overlay en img en la posición x, y con la máscara alpha."""
        y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
        x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

        y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
        x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

        if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
            return

        channels = img.shape[2]

        alpha = alpha_mask[y1o:y2o, x1o:x2o]
        alpha_inv = 1.0 - alpha

        for c in range(channels):
            img[y1:y2, x1:x2, c] = (alpha * img_overlay[y1o:y2o, x1o:x2o, c] +
                                     alpha_inv * img[y1:y2, x1:x2, c])
    def get_marker_center(marker_corners):
        """Obtiene el centro de un marcador dado sus esquinas."""
        center_x = int(sum([corner[0] for corner in marker_corners]) / 4)
        center_y = int(sum([corner[1] for corner in marker_corners]) / 4)
        return center_x, center_y
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detectar los marcadores en la imagen
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is not None:
            for i, corner in zip(ids.flatten(), corners):
                if i == 0:  # ID del primer marcador
                    car_pos = get_marker_center(corner[0])
                elif i == 1:  # ID del segundo marcador
                    target_pos = get_marker_center(corner[0])
        # Mover el carrito hacia el marcador ID 1
        if car_pos is not None and target_pos is not None:
            # Calcular vector de movimiento
            move_vector = np.array(target_pos) - np.array(car_pos)
            move_distance = np.linalg.norm(move_vector)
            
            if move_distance > car_speed:
                move_vector = car_speed * move_vector / move_distance
            else:
                move_vector = target_pos - car_pos
            
            # Actualizar la posición del carrito
            car_pos = np.array(car_pos) + move_vector
            car_pos = car_pos.astype(int)
            
            # Superponer la imagen del carrito en la nueva posición
            carrito_resized = cv2.resize(carrito_image, (car_width, car_height))
            overlay_image_alpha(frame, carrito_resized[:, :, 0:3], car_pos[0] - car_width // 2, car_pos[1] - car_height // 2, carrito_resized[:, :, 3] / 255.0)

        # Mostrar el frame
        cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
else:
    print("El módulo cv2.aruco no está disponible.")
