"""
===============================================================================
MÓDULO 2: GESTIÓN DE CLIENTES - SOFTWARE FJ
Fase 4: Componente Práctico Simuladas - Curso Programación UNAD (213023)
Autor: William Sánchez (Módulo 2 - Responsable de la clase Cliente)
===============================================================================
Este módulo define la clase Cliente con encapsulación de datos personales,
validaciones estrictas mediante propiedades (getters/setters), manejo de
excepciones personalizadas y registro de eventos (logging).
"""

import re
import logging
import sys

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE EXCEPCIONES PERSONALIZADAS
# -----------------------------------------------------------------------------
try:
    from excepciones import SoftwareFJException, ClienteInvalidoError
except ImportError:
    # Definición autónoma de excepciones en caso de ejecutar la clase como módulo independiente
    class SoftwareFJException(Exception):
        """Excepción base del sistema Software FJ."""
        pass

    class ClienteInvalidoError(SoftwareFJException):
        """Excepción lanzada cuando los datos de un cliente son inválidos."""
        pass

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DEL SISTEMA DE LOGGING
# -----------------------------------------------------------------------------
logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.INFO)

# Evitar duplicación de handlers si ya existen
if not logger.handlers:
    # Handler para archivo de log requerido en la Fase 4
    file_handler = logging.FileHandler("software_fj.log", encoding="utf-8")
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - Módulo Cliente: %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter("[%(levelname)s] %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)


# -----------------------------------------------------------------------------
# CLASE CLIENTE (POO & ENCAPSULACIÓN)
# -----------------------------------------------------------------------------
class Cliente:
    """
    Clase que representa un Cliente en la solución Software FJ.
    Aplica encapsulación estricta de datos personales mediante atributos privados
    y validaciones rigurosas en setters.
    """

    def __init__(self, cedula: str, nombre: str, correo: str, telefono: str):
        """
        Inicializa un nuevo objeto Cliente pasando los datos por los setters
        para ejecutar todas las validaciones desde el momento de instanciación.
        """
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        
        logger.info(f"Cliente creado exitosamente -> Cédula: {self.__cedula} | Nombre: {self.__nombre}")

    # -------------------------------------------------------------------------
    # PROPIEDADES (GETTERS Y SETTERS) CON ENCAPSULACIÓN Y VALIDACIONES
    # -------------------------------------------------------------------------

    @property
    def cedula(self) -> str:
        """Obtiene la cédula/documento del cliente."""
        return self.__cedula

    @cedula.setter
    def cedula(self, valor: str):
        valor_str = str(valor).strip()
        # Validación: Numérico entre 6 y 12 dígitos
        if not valor_str.isdigit() or not (6 <= len(valor_str) <= 12):
            msg_error = (
                f"Cédula inválida '{valor}'. Debe ser numérica y tener entre 6 y 12 dígitos."
            )
            logger.error(f"Error de validación: {msg_error}")
            raise ClienteInvalidoError(msg_error)
        self.__cedula = valor_str

    @property
    def nombre(self) -> str:
        """Obtiene el nombre completo del cliente."""
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        valor_str = str(valor).strip()
        # Validación: No vacío y longitud mínima de 2 caracteres
        if not valor_str or len(valor_str) < 2:
            msg_error = f"Nombre inválido '{valor}'. Debe tener al menos 2 caracteres."
            logger.error(f"Error de validación: {msg_error}")
            raise ClienteInvalidoError(msg_error)
        # Se guarda formateado en formato título (Title Case)
        self.__nombre = valor_str.title()

    @property
    def correo(self) -> str:
        """Obtiene el correo electrónico del cliente."""
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        valor_str = str(valor).strip()
        # Expresión regular estándar para la validación de formato de email
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, valor_str):
            msg_error = f"Formato de correo electrónico inválido '{valor}'."
            logger.error(f"Error de validación: {msg_error}")
            raise ClienteInvalidoError(msg_error)
        self.__correo = valor_str.lower()

    @property
    def telefono(self) -> str:
        """Obtiene el número telefónico del cliente."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        valor_str = str(valor).strip()
        # Validación: Numérico entre 7 y 10 dígitos
        if not valor_str.isdigit() or not (7 <= len(valor_str) <= 10):
            msg_error = (
                f"Teléfono inválido '{valor}'. Debe contener entre 7 y 10 dígitos numéricos."
            )
            logger.error(f"Error de validación: {msg_error}")
            raise ClienteInvalidoError(msg_error)
        self.__telefono = valor_str

    # -------------------------------------------------------------------------
    # MÉTODOS DE REPRESENTACIÓN Y DICCIONARIO
    # -------------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Convierte los datos del cliente a un diccionario."""
        return {
            "cedula": self.__cedula,
            "nombre": self.__nombre,
            "correo": self.__correo,
            "telefono": self.__telefono,
        }

    def __str__(self) -> str:
        return f"Cliente(Cédula='{self.__cedula}', Nombre='{self.__nombre}', Correo='{self.__correo}', Tel='{self.__telefono}')"

    def __repr__(self) -> str:
        return self.__str__()


# -----------------------------------------------------------------------------
# EJECUCIÓN Y PRUEBAS DEL MÓDULO (VS CODE)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("=================================================================")
    print("     PRUEBAS DEL MÓDULO 2: CLASE CLIENTE (SOFTWARE FJ)           ")
    print("=================================================================\n")

    # CASO 1: Creación de clientes válidos
    print("--- 1. Pruebas de Registro de Clientes Válidos ---")
    try:
        cliente_1 = Cliente(
            cedula="1012345678",
            nombre="william sanchez",
            correo="william.sanchez@ejemplo.com",
            telefono="3001234567"
        )
        print("  ✓ Objeto creado:", cliente_1)
        
        cliente_2 = Cliente(
            cedula="987654321",
            nombre="MARIA FERNANDA RODRIGUEZ",
            correo="maria.rodriguez@correo.co",
            telefono="3159876543"
        )
        print("  ✓ Objeto creado:", cliente_2)
    except ClienteInvalidoError as e:
        print("  ❌ Error inesperado:", e)

    print("\n-----------------------------------------------------------------")
    print("--- 2. Pruebas de Captura de Excepciones (Datos Inválidos) ---")

    # CASO 2.1: Cédula con caracteres alfabéticos
    try:
        print("\nPrueba 2.1 - Cédula con letras '101234ABC':")
        cliente_error_1 = Cliente("101234ABC", "Carlos Pérez", "carlos@mail.com", "3001112233")
    except ClienteInvalidoError as e:
        print("  ✓ Excepción capturada correctamente:", e)

    # CASO 2.2: Correo electrónico sin formato correcto
    try:
        print("\nPrueba 2.2 - Correo sin '@' o dominio:")
        cliente_error_2 = Cliente("1098765432", "Ana Gómez", "correo_invalido_sin_arroba", "3001112233")
    except ClienteInvalidoError as e:
        print("  ✓ Excepción capturada correctamente:", e)

    # CASO 2.3: Teléfono con longitud incorrecta
    try:
        print("\nPrueba 2.3 - Teléfono de 4 dígitos '1234':")
        cliente_error_3 = Cliente("1098765432", "Pedro Infante", "pedro@mail.com", "1234")
    except ClienteInvalidoError as e:
        print("  ✓ Excepción capturada correctamente:", e)

    # CASO 2.4: Nombre demasiado corto
    try:
        print("\nPrueba 2.4 - Nombre vacío o de 1 letra 'A':")
        cliente_error_4 = Cliente("1098765432", "A", "a@mail.com", "3001112233")
    except ClienteInvalidoError as e:
        print("  ✓ Excepción capturada correctamente:", e)

    print("\n=================================================================")
    print("Pruebas finalizadas. Los eventos han sido registrados en 'software_fj.log'.")
    print("=================================================================")
