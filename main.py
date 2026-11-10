# =====================================================================
# Menú Principal Interactivo - Sistema Software FJ
# Desarrollado por: Integrante 5 (Juan Pablo Sánchez Ramírez)
# Descripción: Integra todos los módulos del proyecto en un menú por
# consola. Cada opción se ejecuta con procesar_operacion_segura()
# (logger.py), así ningún error detiene el programa y todo queda
# registrado en el archivo logs.txt.
# Ejecución: python main.py
# =====================================================================

import sys  # Para ajustar la codificación de la consola

from logger import procesar_operacion_segura, registrar_evento  # Registro seguro (Integrante 1)
from reserva import SistemaGestion                              # Gestor con listas internas
from servicios import IVA, formato_pesos                        # IVA por defecto y formato de pesos
from simulacion import ejecutar_simulacion                      # Simulación automática (Integrante 4)

LINEA = "-" * 60  # Separador visual del menú

MENU = """
============================================================
        SOFTWARE FJ - SISTEMA DE GESTIÓN DE RESERVAS
============================================================
  1. Registrar cliente
  2. Crear servicio (sala, equipo o asesoría)
  3. Crear y confirmar una reserva
  4. Procesar (cobrar) una reserva
  5. Cancelar una reserva
  6. Cotizar un servicio
  7. Ver clientes, servicios y reservas (reporte)
  8. Ejecutar la simulación automática de operaciones
  0. Salir
============================================================"""


# ---------------------------------------------------------------------
# Funciones de apoyo para leer datos del usuario
# ---------------------------------------------------------------------

def pedir(texto, obligatorio=True):
    """Pide un texto por consola. Si no es obligatorio y se deja vacío, devuelve None."""
    valor = input(f"  {texto}: ").strip()  # Leemos y quitamos espacios
    if valor == "" and not obligatorio:    # Campo opcional vacío
        return None
    return valor  # Si es obligatorio y vacío, la clase correspondiente lo rechazará


def a_numero(valor):
    """Convierte '3' en 3 y '2.5' en 2.5. Si no es un número, lo deja como texto
    para que la clase que lo recibe lance su propia excepción de validación."""
    if valor is None:  # Nada que convertir
        return None
    try:
        return int(valor)  # Primero intentamos entero
    except ValueError:
        try:
            return float(valor)  # Luego decimal
        except ValueError:
            return valor  # No es número: se deja tal cual


def porcentaje(valor):
    """Convierte '10' (10 %) en 0.10. Si viene vacío devuelve None (sin descuento)."""
    numero = a_numero(valor)  # Puede quedar como texto si no es número
    if isinstance(numero, (int, float)):  # Solo los números se pasan a fracción
        return numero / 100
    return numero  # None o texto inválido: el cálculo lo rechazará con su excepción


def mostrar_lista(sistema, tipo):
    """Imprime los elementos de una lista del sistema para que el usuario elija IDs."""
    elementos = sistema.listar(tipo)  # Copia de la lista interna
    if not elementos:  # Lista vacía
        print(f"  (No hay {tipo} registrados todavía)")
    for elemento in elementos:  # Polimorfismo: cada objeto se describe a sí mismo
        print("  -", elemento)


# ---------------------------------------------------------------------
# Acciones del menú: cada una pide los datos y llama al sistema
# ---------------------------------------------------------------------

def registrar_cliente(sistema):
    print("\nRegistrar cliente")
    cliente = sistema.registrar_cliente(       # Las validaciones están en la clase Cliente
        nombre=pedir("Nombre completo"),
        documento=pedir("Documento (6 a 10 dígitos)"),
        correo=pedir("Correo electrónico"),
        telefono=pedir("Celular (opcional, Enter para omitir)", obligatorio=False),
    )
    print(f"  ✔ {cliente}")  # Solo llega aquí si no hubo errores


def crear_servicio(sistema):
    print("\nCrear servicio - tipos: sala | equipo | asesoria")
    tipo = pedir("Tipo de servicio").lower()           # Tipo elegido
    datos = {"nombre": pedir("Nombre del servicio"),     # Datos comunes a todos
             "tarifa": a_numero(pedir("Tarifa en pesos (por hora o por día)"))}
    if tipo == "sala":                                   # Datos propios de cada tipo
        datos["capacidad"] = a_numero(pedir("Capacidad (personas)"))
    elif tipo == "equipo":
        datos["tipo_equipo"] = pedir("Tipo de equipo (ej. Portátil)")
        datos["unidades"] = a_numero(pedir("Unidades disponibles"))
    elif tipo == "asesoria":
        datos["area"] = pedir("Área de la asesoría")
        datos["nivel"] = pedir("Nivel (basico, avanzado, experto)")
    servicio = sistema.crear_servicio(tipo, **datos)    # Un tipo desconocido lanza ServicioInvalidoError
    print(f"  ✔ {servicio}")


def crear_reserva(sistema):
    print("\nCrear y confirmar reserva")
    mostrar_lista(sistema, "servicios")                  # Ayuda a escoger el ID
    documento = pedir("Documento del cliente")
    servicio_id = pedir("ID del servicio (ej. SRV-0001)")
    duracion = pedir("Duración (horas o días según el servicio)")  # Reserva valida que sea número
    servicio = sistema.buscar_servicio(servicio_id)     # Para saber qué datos extra pedir
    detalles = {}                                       # Datos extra según el servicio
    if type(servicio).__name__ == "ReservaSala":
        detalles["personas"] = a_numero(pedir("Número de personas"))
    elif type(servicio).__name__ == "AlquilerEquipo":
        detalles["cantidad"] = a_numero(pedir("Cantidad de unidades"))
    reserva = sistema.reservar(documento, servicio_id, duracion, **detalles)  # Crea y confirma
    print(f"  ✔ {reserva}")


def procesar_reserva(sistema):
    print("\nProcesar reserva")
    mostrar_lista(sistema, "reservas")
    reserva = sistema.buscar_reserva(pedir("ID de la reserva (ej. RES-0001)"))
    descuento = porcentaje(pedir("Descuento en % (Enter si no hay)", obligatorio=False))
    reserva.procesar(impuesto=IVA, descuento=descuento)  # Calcula con IVA y cierra la reserva
    print(f"  ✔ {reserva}")


def cancelar_reserva(sistema):
    print("\nCancelar reserva")
    mostrar_lista(sistema, "reservas")
    reserva = sistema.buscar_reserva(pedir("ID de la reserva (ej. RES-0001)"))
    motivo = pedir("Motivo (opcional)", obligatorio=False) or "sin motivo"
    reserva.cancelar(motivo)  # Una reserva procesada o ya cancelada lanza OperacionNoPermitidaError
    print(f"  ✔ {reserva}")


def cotizar(sistema):
    print("\nCotizar servicio (IVA incluido)")
    mostrar_lista(sistema, "servicios")
    servicio = sistema.buscar_servicio(pedir("ID del servicio (ej. SRV-0001)"))
    consulta = {"duracion": a_numero(pedir("Duración")), "impuesto": IVA}  # Diccionario para cotizar()
    descuento = porcentaje(pedir("Descuento en % (Enter si no hay)", obligatorio=False))
    if descuento is not None:
        consulta["descuento"] = descuento
    if type(servicio).__name__ == "ReservaSala":        # Detalles según el tipo
        consulta["personas"] = a_numero(pedir("Número de personas"))
    elif type(servicio).__name__ == "AlquilerEquipo":
        consulta["cantidad"] = a_numero(pedir("Cantidad de unidades"))
    print(f"  ✔ Valor estimado: {formato_pesos(servicio.cotizar(consulta))}")  # Sobrecarga por tipo (dict)


def ver_reporte(sistema):
    sistema.reporte()  # Listado completo con polimorfismo (cada objeto se describe)


def simulacion_automatica(sistema):
    ejecutar_simulacion(reiniciar_log=False)  # Usa su propio sistema para no mezclar datos con el menú


# Relación opción -> función (evita una larga cadena de if/elif)
ACCIONES = {
    "1": registrar_cliente,
    "2": crear_servicio,
    "3": crear_reserva,
    "4": procesar_reserva,
    "5": cancelar_reserva,
    "6": cotizar,
    "7": ver_reporte,
    "8": simulacion_automatica,
}


def main():
    """Ciclo principal del menú. Solo termina con la opción 0 (o Ctrl+C)."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Tildes y símbolos en cualquier consola
    except (AttributeError, ValueError):
        pass  # Consolas antiguas: se sigue con su codificación
    sistema = SistemaGestion()  # Listas vacías, sin base de datos
    registrar_evento("INFO", "Menú principal iniciado")
    while True:  # El menú se repite hasta que el usuario elija salir
        print(MENU)
        try:
            opcion = input("Elija una opción: ").strip()
        except (KeyboardInterrupt, EOFError):  # Ctrl+C o fin de entrada: salida ordenada
            opcion = "0"
        if opcion == "0":
            registrar_evento("INFO", "Menú principal cerrado por el usuario")
            print("\nGracias por usar Software FJ. ¡Hasta pronto!")
            break
        accion = ACCIONES.get(opcion)  # None si la opción no existe
        if accion is None:
            print("  ✘ Opción no válida. Escriba un número del 0 al 8.")
            registrar_evento("WARNING", f"Opción de menú inválida: {opcion!r}")
            continue
        try:
            # Red de seguridad del Integrante 1: atrapa y registra cualquier error
            procesar_operacion_segura(accion, sistema)
        except KeyboardInterrupt:  # Ctrl+C dentro de una opción: volvemos al menú
            print("\n  Operación cancelada por el usuario.")
        print(LINEA)


# Solo se ejecuta el menú si se corre este archivo directamente
if __name__ == "__main__":
    main()
