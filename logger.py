# =====================================================================
# Módulo de Excepciones Personalizadas - Sistema Software FJ
# Desarrollado por: Integrante 1
# Descripción: Jerarquía de clases de excepción para controlar fallos
# en clientes, servicios, reservas y cálculos del sistema.
# =====================================================================

class SoftwareFJError(Exception):
    """Clase base abstracta para todas las excepciones del sistema Software FJ."""
    def __init__(self, mensaje: str, codigo_error: int = 500):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo_error = codigo_error

    def __str__(self):
        return f"[ERROR {self.codigo_error}]: {self.mensaje}"


class ClienteInvalidoError(SoftwareFJError):
    """Se dispara cuando los datos del cliente no cumplen con las validaciones."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error=401)


class ServicioNoDisponibleError(SoftwareFJError):
    """Se dispara cuando un servicio solicitado no se encuentra activo o no existe."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error=404)


class ReservaInvalidaError(SoftwareFJError):
    """Se dispara cuando la duración, estado o parámetros de una reserva son incorrectos."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error=400)


class CalculoInconsistenteError(SoftwareFJError):
    """Se dispara ante inconsistencias numéricas en costos, descuentos o impuestos."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error=422)
Haz clic en "Commit changes...", escribe en el mensaje feat: implementacion de excepciones personalizadas en excepciones.py y guarda
.
Paso 5: Crear el módulo de registro de logs en logger.py (Commit 4)
En la pestaña Code, haz clic en "Add file" -> "Create new file"
.
Nombra el archivo: logger.py.
Pega el siguiente código Python, el cual implementa las funciones de registro de eventos e incluye bloques try/except, try/except/else, try/except/finally y encadenamiento de excepciones (raise ... from ...)
:
# =====================================================================
# Módulo de Logging y Gestión de Eventos - Sistema Software FJ
# Desarrollado por: Integrante 1
# Descripción: Manejo seguro de archivos de texto para auditar eventos
# y capturar excepciones sin detener la ejecución de la aplicación.
# =====================================================================

from datetime import datetime
from excepciones import SoftwareFJError


def registrar_evento(log_type: str, mensaje: str, ruta_archivo: str = "logs.txt") -> bool:
    """
    Registra un evento o error en el archivo de logs del sistema.
    Usa bloques try/except/else/finally para garantizar la captura segura del fallo.
    """
    archivo = None
    exito = False
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea_log = f"[{timestamp}] [{log_type.upper()}]: {mensaje}\n"

    try:
        # Abrir el archivo en modo append (agregar al final)
        archivo = open(ruta_archivo, "a", encoding="utf-8")
        archivo.write(linea_log)
    except IOError as err:
        # Si ocurre un error al escribir el archivo, se usa encadenamiento de excepciones
        print(f"Fallo crítico al escribir en el log: {err}")
        raise SoftwareFJError("No se pudo escribir en el archivo de auditoría.") from err
    else:
        # Se ejecuta únicamente si la apertura y escritura fueron exitosas
        exito = True
        print(f"Evento registrado correctamente: {log_type.upper()}")
    finally:
        # Garantiza el cierre del recurso independientemente de si hubo error o no
        if archivo and not archivo.closed:
            archivo.close()

    return exito


def procesar_operacion_segura(operacion_func, *args, **kwargs):
    """
    Función de envoltura para ejecutar operaciones complejas del sistema de forma segura.
    Captura excepciones personalizadas, las registra en el log y evita el colapso del programa.
    """
    try:
        resultado = operacion_func(*args, **kwargs)
        registrar_evento("INFO", f"Operación {operacion_func.__name__} ejecutada con éxito.")
        return resultado
    except SoftwareFJError as error:
        # Captura de excepciones personalizadas del dominio Software FJ
        registrar_evento("ERROR_NEGOCIO", str(error))
        print(f"Excepción controlada capturada: {error}")
        return None
    except Exception as error_inesperado:
        # Encadenamiento de excepciones inesperadas
        registrar_evento("CRITICAL", f"Error insospechado: {error_inesperado}")
        print(f"Se ha producido un error inesperado en el sistema: {error_inesperado}")
        return None
