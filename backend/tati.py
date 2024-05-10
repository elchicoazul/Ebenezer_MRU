import random

# Nombre del archivo de texto
archivo_detalle_venta = 'detalle_ventas_inserts.txt'

# Abrir el archivo para escritura
with open(archivo_detalle_venta, 'w') as f:
    # Generar detalles de venta para cada venta
    for id_venta in range(1, 5001):
        # Generar un número aleatorio de productos comprados entre 1 y 5
        num_productos = random.randint(1, 5)
        # Generar detalles de venta para cada producto
        for id_detalle in range(1, num_productos + 1):
            # Generar ID de producto aleatorio entre PRD001 y PRD050
            id_producto = 'PRD' + str(random.randint(1, 50)).zfill(3)
            # Generar cantidad aleatoria entre 1 y 24
            cantidad = random.randint(1, 24)
            f.write(f"INSERT INTO detalle_ventas (ID_Detalle_Venta, ID_Ventas, ID_Producto, cantidad) VALUES "
                    f"(DEFAULT, 'VTN{id_venta:04}', '{id_producto}', {cantidad});\n")

print(f"Archivo de detalles de venta creado: {archivo_detalle_venta}")
