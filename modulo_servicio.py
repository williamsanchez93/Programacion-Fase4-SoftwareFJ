from abc import ABC, abstractmethod
import logging

try:
    from modulo_excepciones import ServicioNoDisponibleError, ParametroInvalidoError, logger
except ImportError:
    try:
        from excepciones import ServicioNoDisponibleError, ParametroInvalidoError, logger
    except ImportError:
        logger = logging.getLogger("SoftwareFJ")
        class ServicioNoDisponibleError(Exception): pass
        class ParametroInvalidoError(Exception): pass


class Servicio(ABC):
    """
    Clase Abstracta base para la jerarquía de Servicios en Software FJ.
    """

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float):
        if not id_servicio or not str(id_servicio).strip():
            raise ParametroInvalidoError("El ID del servicio no puede estar vacío.")
        if tarifa_base <= 0:
            raise ParametroInvalidoError(f"La tarifa base debe ser un valor positivo ({tarifa_base}).")
        
        self._id_servicio = str(id_servicio).strip()
        self._nombre = str(nombre).strip().title()
        self._tarifa_base = float(tarifa_base)

    @property
    def id_servicio(self) -> str:
        return self._id_servicio

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Método abstracto para el cálculo polimórfico del costo del servicio."""
        pass

    @abstractmethod
    def obtener_descripcion(self) -> str:
        """Método abstracto que retorna un resumen descriptivo del servicio."""
        pass

    def __str__(self) -> str:
        return f"{self._nombre} (ID: {self._id_servicio}) - Tarifa Base: ${self._tarifa_base:,.2f}"


class ServicioSala(Servicio):
    """
    Subclase para el alquiler de salas de conferencias / eventos.
    """

    def __init__(self, id_servicio: str, nombre: str, tarifa_por_hora: float, capacidad_aforo: int, incluye_audiovisuales: bool = True):
        super().__init__(id_servicio, nombre, tarifa_por_hora)
        if capacidad_aforo < 5 or capacidad_aforo > 500:
            msg = f"Aforo no disponible ({capacidad_aforo} personas). Capacidad permitida entre 5 y 500."
            logger.error(f"[ERR_SERVICIO_NO_DISPONIBLE] {msg}")
            raise ServicioNoDisponibleError(msg)
        self.capacidad_aforo = capacidad_aforo
        self.incluye_audiovisuales = incluye_audiovisuales
        logger.info(f"Servicio de Sala registrado: {self._nombre} (Aforo: {self.capacidad_aforo})")

    def calcular_costo(self, horas: float, porcentaje_descuento: float = 0.0) -> float:
        if horas <= 0 or horas > 24:
            msg = f"Duración de sala inválida '{horas}'. Debe ser entre 1 y 24 horas."
            logger.error(f"[ERR_SERVICIO_NO_DISPONIBLE] {msg}")
            raise ServicioNoDisponibleError(msg)
        
        subtotal = self._tarifa_base * horas
        if self.incluye_audiovisuales:
            subtotal += 50000.0  # Recargo fijo de equipos audiovisuales
            
        descuento = subtotal * (porcentaje_descuento / 100.0)
        total = (subtotal - descuento) * 1.15  # 15% IVA
        return round(total, 2)

    def obtener_descripcion(self) -> str:
        equipo_str = "Con Audiovisuales" if self.incluye_audiovisuales else "Sin Audiovisuales"
        return f"Sala: {self._nombre} | Aforo: {self.capacidad_aforo} personas | {equipo_str}"


class ServicioEquipo(Servicio):
    """
    Subclase para el alquiler de equipos tecnológicos / cómputo.
    """

    def __init__(self, id_servicio: str, nombre: str, tarifa_diaria: float, es_alta_gama: bool = False, garantia_base: float = 100000.0):
        super().__init__(id_servicio, nombre, tarifa_diaria)
        self.es_alta_gama = es_alta_gama
        self.garantia_base = garantia_base
        logger.info(f"Servicio de Equipo registrado: {self._nombre}")

    def calcular_costo(self, dias: int, con_seguro: bool = True) -> float:
        if dias <= 0 or dias > 90:
            msg = f"Días de alquiler de equipo inválidos '{dias}'. Debe ser entre 1 y 90 días."
            logger.error(f"[ERR_SERVICIO_NO_DISPONIBLE] {msg}")
            raise ServicioNoDisponibleError(msg)
            
        subtotal = self._tarifa_base * dias
        if self.es_alta_gama:
            subtotal *= 1.20  # 20% adicional por equipo alta gama
            
        if con_seguro:
            subtotal += 20000.0 * dias  # Seguro por día
            
        return round(subtotal, 2)

    def obtener_descripcion(self) -> str:
        gama_str = "Alta Gama" if self.es_alta_gama else "Estándar"
        return f"Equipo: {self._nombre} [{gama_str}] | Garantía: ${self.garantia_base:,.2f}"


class ServicioAsesoria(Servicio):
    """
    Subclase para servicios de consultoría y asesoría técnica.
    """

    NIVELES_PERMITIDOS = {"JUNIOR": 1.0, "SENIOR": 1.5, "MASTER": 2.2}

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora_consultor: float, nivel_consultor: str = "SENIOR"):
        super().__init__(id_servicio, nombre, tarifa_hora_consultor)
        nivel_upper = str(nivel_consultor).upper().strip()
        if nivel_upper not in self.NIVELES_PERMITIDOS:
            msg = f"Nivel de consultor inválido '{nivel_consultor}'. Permitidos: {list(self.NIVELES_PERMITIDOS.keys())}"
            logger.error(f"[ERR_SERVICIO_NO_DISPONIBLE] {msg}")
            raise ServicioNoDisponibleError(msg)
        self.nivel_consultor = nivel_upper
        logger.info(f"Servicio de Asesoría registrado: {self._nombre} (Nivel: {self.nivel_consultor})")

    def calcular_costo(self, horas: float) -> float:
        if horas <= 0 or horas > 100:
            msg = f"Horas de asesoría inválidas '{horas}'. Debe ser entre 1 y 100 horas."
            logger.error(f"[ERR_SERVICIO_NO_DISPONIBLE] {msg}")
            raise ServicioNoDisponibleError(msg)
            
        multiplicador = self.NIVELES_PERMITIDOS[self.nivel_consultor]
        total = (self._tarifa_base * horas) * multiplicador
        return round(total, 2)

    def obtener_descripcion(self) -> str:
        return f"Asesoría: {self._nombre} | Consultor {self.nivel_consultor}"


if __name__ == "__main__":
    print("="*65)
    print("     PRUEBA INTEGRADA MÓDULO 3: JERARQUÍA DE SERVICIOS (POO)     ")
    print("="*65)
    
    sala = ServicioSala("SALA-01", "Auditorio Principal", 60000.0, 150, True)
    costo_sala = sala.calcular_costo(horas=6, porcentaje_descuento=10)
    print(f"✓ {sala.obtener_descripcion()} | Total: ${costo_sala:,.2f}")

    equipo = ServicioEquipo("EQ-01", "Macbook Pro M3 Max", 100000.0, es_alta_gama=True)
    costo_equipo = equipo.calcular_costo(dias=3, con_seguro=True)
    print(f"✓ {equipo.obtener_descripcion()} | Total Alquiler: ${costo_equipo:,.2f}")

    asesoria = ServicioAsesoria("ASE-01", "Arquitectura De Software Poo", 80000.0, "MASTER")
    costo_asesoria = asesoria.calcular_costo(horas=4.5)
    print(f"✓ {asesoria.obtener_descripcion()} | Total: ${costo_asesoria:,.2f}")
    print("="*65)
