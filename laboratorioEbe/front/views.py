import json
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import subprocess
from django.http import JsonResponse
from django.http import StreamingHttpResponse
import cv2
import cv2.aruco as aruco
import numpy as np
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import LoginForm, SignUpForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required



car_speed = 2  # Velocidad inicial


# Create your views here.
#imprime un txto html

def menu(request):
    context = {}
    return render(request, 'front/menu.html', context)

def cuadro(request):
   
    return render(request, 'front/cuadro_formulario.html', context)



def ejecutar_ca(request):
    try:
        subprocess.run(['python', 'D:\\Laboratorio-de-fisica-con-realidad-aumentada-Eben\\backend\\vista.py'])
        context = {}
        return render(request, 'front/cuadro_formulario.html', context)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def video_stream():
    cap = cv2.VideoCapture(0)
    aruco = cv2.aruco
    global car_speed
   
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
        # Aquí agregaría su lógica de procesamiento de ArUco y superposición
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
                print(car_speed)
                move_vector = car_speed * move_vector / move_distance
                print(car_speed)
            else:
                move_vector = target_pos - car_pos
            
            # Actualizar la posición del carrito
            car_pos = np.array(car_pos) + move_vector
            car_pos = car_pos.astype(int)
            
            # Superponer la imagen del carrito en la nueva posición
            carrito_resized = cv2.resize(carrito_image, (car_width, car_height))
            overlay_image_alpha(frame, carrito_resized[:, :, 0:3], car_pos[0] - car_width // 2, car_pos[1] - car_height // 2, carrito_resized[:, :, 3] / 255.0)

        # Mostrar el frame
        #cv2.imshow('Video', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

def video_feed(request):
    return StreamingHttpResponse(video_stream(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')



@require_POST
def actualizar_velocidad(request):
    global car_speed
    try:
        data = json.loads(request.body)
        nueva_velocidad = int(data.get('velocidad', 2))  # Valor por defecto de 2
        car_speed = nueva_velocidad  # Actualizar la velocidad global
        print(f"Velocidad actualizada a: {car_speed}")  # Impresión para depuración
        return JsonResponse({'status': 'success', 'new_speed': car_speed})
    except js.on.JSONDecodeError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)



@login_required
def mPerfil(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('menu')  # Redirige a la página de inicio o a algún panel de usuario
    else:
        form = UserChangeForm(instance=request.user)
    
    context = {'form': form}
    return render(request, 'front/mPerfil.html', context)

def editarPerfil(request):
    context = {}
    return render(request, 'front/editarPerfil.html', context)
def infSimulacion(request):
    context = {}
    return render(request, 'front/infSimulacion.html', context)
def infEjecucion(request):
    context = {}
    return render(request, 'front/infEjecucion.html', context)
def herAnotacion(request):
    context = {}
    return render(request, 'front/herAnotacion.html', context)



def registro(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario en la base de datos
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)  # Autentica al usuario correctamente
            if user:
                login(request, user)  # Inicia sesión al usuario
                return redirect('menu')  # Asegúrese de que 'menu' es una vista o URL válida en su archivo urls.py
            else:
                print("Error en la autenticación")  # Agregar para depuración
        else:
            print(form.errors)  # Imprime errores para depuración
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'front/registro.html', context)

def IniciarSesion(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print("Username:", username)  # Imprime el nombre de usuario recibido
            print("Password:", password)  # Imprime la contraseña recibida

            user = authenticate(username=username, password=password)
            if user is not None:
                print("Autenticación exitosa para el usuario:", username)
                login(request, user)
                return redirect('menu')  # Redirige a la página de inicio después del login
            else:
                print("Error en la autenticación, usuario no encontrado o contraseña incorrecta.")
        else:
            print("Formulario no válido, errores:", form.errors)
    else:
        form = LoginForm()

    return render(request, 'front/login.html', {'form': form})
