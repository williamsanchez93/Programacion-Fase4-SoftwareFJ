import logging
import os

# Configuración centralizada del logger
LOG_FILENAME = "software_fj.log"

logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)

# Evitar duplicación de handlers si se importa varias veces
if not logger.handlers:
    # Handler para archivo
    file_handler = logging.FileHandler(LOG_FILENAME, encoding="utf-8")
    file_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("[%(levelname)s]: %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)


class SoftwareFJException(Exception):
    """Excepción base del sistema Software FJ."""
    def __init__(self, mensaje: str, codigo_error: str = "ERR_BASE"):
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        super().__init__(f"[{self.codigo_error}] {self.mensaje}")


class ClienteInvalidoError(SoftwareFJException):
    """Excepción para errores en datos de clientes."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_CLIENTE_INVALIDO")


class ServicioNoDisponibleError(SoftwareFJException):
    """Excepción para inconsistencias o falta de disponibilidad en servicios."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_SERVICIO_NO_DISPONIBLE")


class ReservaInvalidaError(SoftwareFJException):
    """Excepción para errores de negocio o estado en reservas."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_RESERVA_INVALIDA")


class ParametroInvalidoError(SoftwareFJException):
    """Excepción para parámetros de entrada fuera de rango o tipo incorrecto."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_PARAMETRO_INVALIDO")


if __name__ == "__main__":
    logger.info("Inicio de pruebas del Módulo de Excepciones y Logging.")
    print("="*65)
    print("      PRUEBA DEL MÓDULO 1: EXCEPCIONES Y LOGGING (SOFTWARE FJ)     ")
    print("="*65)
    
    try:
        raise ClienteInvalidoError("Prueba: Documento de cliente inválido.")
    except ClienteInvalidoError as e:
        logger.error(str(e))
        print(f"✓ Excepción capturada exitosamente: {e}")

    try:
        raise ServicioNoDisponibleError("Prueba: Sala sin aforo disponible.")
    except ServicioNoDisponibleError as e:
        logger.error(str(e))
        print(f"✓ Excepción capturada exitosamente: {e}")

    try:
        raise ReservaInvalidaError("Prueba: Intento de cancelar reserva procesada.")
    except ReservaInvalidaError as e:
        logger.error(str(e))
        print(f"✓ Excepción capturada exitosamente: {e}")

    print("-"*65)
    print("Verifica el archivo 'software_fj.log' en tu directorio de trabajo.")
    print("="*65)
