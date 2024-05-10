import random
from datetime import datetime, timedelta

# Función para generar un ID de cliente aleatorio entre C001 y C500
def generar_id_cliente():
    return 'C' + str(random.randint(1, 500)).zfill(3)

# Función para generar una fecha de venta dentro del rango especificado
def generar_fecha_venta(fecha_inicio, fecha_fin, id_venta):
    dias_totales = (fecha_fin - fecha_inicio).days
    dias_por_venta = dias_totales / 5000
    dias_a_sumar = int((id_venta - 1) * dias_por_venta)
    return fecha_inicio + timedelta(days=dias_a_sumar)

# Función para generar una hora de venta entre las 8:00 y las 20:00
def generar_hora_venta():
    hora = random.randint(8, 19)
    return f"{hora:02}:00"

# Nombre del archivo de texto
archivo = 'registro_ventas_inserts.txt'

# Configurar el inicio y fin del rango de fechas
fecha_inicio = datetime(2022, 1, 1)
fecha_fin = datetime(2024, 1, 31)

# Abrir el archivo para escritura
with open(archivo, 'w') as f:
    # Generar comandos de inserción y escribir en el archivo
    for id_venta in range(1, 5001):
        id_cliente = generar_id_cliente()
        fecha_venta = generar_fecha_venta(fecha_inicio, fecha_fin, id_venta)
        hora_venta = generar_hora_venta()
        f.write(f"INSERT INTO registro_ventas (ID_Ventas, ID_Cliente, fecha_venta, hora) VALUES "
                f"('VTN{id_venta:04}', '{id_cliente}', '{fecha_venta}', '{hora_venta}');\n")

print(f"Archivo de inserciones creado: {archivo}")
