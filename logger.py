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
        archivo = open(ruta_archivo, "a", encoding="utf-8")
        archivo.write(linea_log)
    except IOError as err:
        print(f"Fallo crítico al escribir en el log: {err}")
        raise SoftwareFJError("No se pudo escribir en el archivo de auditoría.") from err
    else:
        exito = True
        print(f"Evento registrado correctamente: {log_type.upper()}")
    finally:
        if archivo is not None and not archivo.closed:
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
        registrar_evento("ERROR_NEGOCIO", str(error))
        print(f"Excepción controlada capturada: {error}")
        return None
    except Exception as error_inesperado:
        registrar_evento("CRITICAL", f"Error insospechado: {error_inesperado}")
        print(f"Se ha producido un error inesperado en el sistema: {error_inesperado}")
        return None
