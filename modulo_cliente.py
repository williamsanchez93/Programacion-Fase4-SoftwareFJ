import re
import logging

try:
    from modulo_excepciones import ClienteInvalidoError, logger
except ImportError:
    try:
        from excepciones import ClienteInvalidoError, logger
    except ImportError:
        logger = logging.getLogger("SoftwareFJ")
        class ClienteInvalidoError(Exception):
            pass


class Cliente:
    """
    Clase que representa un Cliente en la solución Software FJ.
    Aplica encapsulación de datos personales y validaciones strictly en setters.
    """

    def __init__(self, cedula: str, nombre: str, correo: str, telefono: str):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        
        logger.info(f"Cliente registrado exitosamente: {self.__nombre} (Doc: {self.__cedula})")

    @property
    def cedula(self) -> str:
        return self.__cedula

    @cedula.setter
    def cedula(self, valor: str):
        valor_str = str(valor).strip()
        if not valor_str.isdigit() or len(valor_str) < 6 or len(valor_str) > 12:
            error_msg = f"Cédula inválida '{valor}'. Debe ser numérica y tener entre 6 y 12 dígitos."
            logger.error(f"[ERR_CLIENTE_INVALIDO] {error_msg}")
            raise ClienteInvalidoError(error_msg)
        self.__cedula = valor_str

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        valor_str = str(valor).strip()
        if not valor_str or len(valor_str) < 2:
            error_msg = f"Nombre inválido '{valor}'. Debe tener al menos 2 caracteres."
            logger.error(f"[ERR_CLIENTE_INVALIDO] {error_msg}")
            raise ClienteInvalidoError(error_msg)
        self.__nombre = valor_str.title()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        valor_str = str(valor).strip()
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, valor_str):
            error_msg = f"Formato de correo electrónico inválido '{valor}'."
            logger.error(f"[ERR_CLIENTE_INVALIDO] {error_msg}")
            raise ClienteInvalidoError(error_msg)
        self.__correo = valor_str.lower()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        valor_str = str(valor).strip()
        if not valor_str.isdigit() or len(valor_str) < 7 or len(valor_str) > 10:
            error_msg = f"Teléfono inválido '{valor}'. Debe contener entre 7 y 10 dígitos numéricos."
            logger.error(f"[ERR_CLIENTE_INVALIDO] {error_msg}")
            raise ClienteInvalidoError(error_msg)
        self.__telefono = valor_str

    def to_dict(self) -> dict:
        return {
            "cedula": self.__cedula,
            "nombre": self.__nombre,
            "correo": self.__correo,
            "telefono": self.__telefono
        }

    def __str__(self) -> str:
        return f"Cliente(Cédula='{self.__cedula}', Nombre='{self.__nombre}', Correo='{self.__correo}', Tel='{self.__telefono}')"

    def __repr__(self) -> str:
        return self.__str__()


if __name__ == "__main__":
    print("="*65)
    print("     PRUEBA INTEGRADA MÓDULO 2: CLASE CLIENTE (SOFTWARE FJ)      ")
    print("="*65)
    
    try:
        c1 = Cliente("1012345678", "william sanchez", "william.sanchez@ejemplo.com", "3001234567")
        print(f"✓ Cliente válido creado: {c1}")
    except ClienteInvalidoError as e:
        print(f"Error inesperado: {e}")

    try:
        c_err = Cliente("123", "Ana", "ana@correo.com", "3000000000")
    except ClienteInvalidoError as e:
        print(f"✓ Excepción capturada correctamente: {e}")
    print("="*65)
