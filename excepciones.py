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
