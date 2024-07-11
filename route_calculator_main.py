from route_c_funciones import CalculadoraRutas

# Mapa predeterminado
mapa = [[0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 1],
        [0, 1, 1, 0, 1, 1],
        [3, 3, 0, 0, 0, 2],
        [2, 2, 2, 2, 0, 2],
        [0, 0, 0, 0, 0, 0]]

tamano = len(mapa)

# Creamos una instancia de CalculadoraRutas
calculadora = CalculadoraRutas(tamano, mapa)

print("""
        BIENVENIDO A TU CALCULADOR DE RUTAS
        """)

calculadora.imprimir_mapa(calculadora.mapa)

menu = 1
while menu != 0:
    opciones = [0, 1, 2, 3, 4]
    mensaje = """
                    Elija una opcion:
                0 - Salir
                1 - Cambiar inicio y fin
                2 - Modificar obstaculos
                3 - Imprimir mapa
                4 - Encontrar camino
                -> """

    # Pedimos al usuario una opcion
    menu = calculadora._obtener_eleccion(mensaje, opciones)

    # Cambiar coordenadas de inicio y de fin
    if menu == 1:
        calculadora.definir_coordenadas()

    # Anadir obstaculos
    elif menu == 2:
        calculadora.definir_obstaculos()

    # Imprimir mapa
    elif menu == 3:
        calculadora.imprimir_mapa(calculadora.mapa)

    # Encontrar camino
    elif menu == 4:
        calculadora.encontrar_ruta_mas_corta()

print("    ")
print("Asi quedo tu ruta")
calculadora.encontrar_ruta_mas_corta()
