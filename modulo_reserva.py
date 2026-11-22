from datetime import datetime, date
import logging

try:
    from modulo_excepciones import ReservaInvalidaError, ParametroInvalidoError, logger
    from modulo_cliente import Cliente
    from modulo_servicio import Servicio
except ImportError:
    try:
        from excepciones import ReservaInvalidaError, ParametroInvalidoError, logger
        from cliente import Cliente
        from servicio import Servicio
    except ImportError:
        logger = logging.getLogger("SoftwareFJ")
        class ReservaInvalidaError(Exception): pass
        class ParametroInvalidoError(Exception): pass


class Reserva:
    """
    Clase que gestiona la Reserva integrando Cliente, Servicio, fecha, duración y estado.
    Aplica bloques try/except/else/finally para operaciones críticas.
    """

    ESTADOS_PERMITIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, fecha_reserva: str, parametro_duracion: float):
        if not isinstance(cliente, Cliente):
            raise ParametroInvalidoError("El parámetro cliente debe ser una instancia de la clase Cliente.")
        if not isinstance(servicio, Servicio):
            raise ParametroInvalidoError("El parámetro servicio debe ser una instancia de la jerarquía Servicio.")
        if parametro_duracion <= 0:
            raise ParametroInvalidoError(f"La duración/cantidad debe ser mayor a cero ({parametro_duracion}).")

        self.id_reserva = str(id_reserva).strip().upper()
        self.cliente = cliente
        self.servicio = servicio
        self.parametro_duracion = float(parametro_duracion)
        self.__estado = "PENDIENTE"

        try:
            self.fecha = datetime.strptime(fecha_reserva, "%Y-%m-%d").date()
        except ValueError as e:
            msg = f"Formato de fecha inválido '{fecha_reserva}'. Use AAAA-MM-DD."
            logger.error(f"[ERR_RESERVA_INVALIDA] {msg}")
            raise ReservaInvalidaError(msg) from e

        # Cálculo inicial del costo llamando al método polimórfico del servicio
        self.costo_total = self.servicio.calcular_costo(self.parametro_duracion)
        logger.info(f"Reserva creada [{self.id_reserva}] | Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre}")

    @property
    def estado(self) -> str:
        return self.__estado

    def confirmar_reserva(self) -> bool:
        """
        Confirma la reserva pasando del estado PENDIENTE a CONFIRMADA.
        Estructura con bloques try/except/else/finally.
        """
        logger.info(f"Iniciando confirmación de reserva [{self.id_reserva}]...")
        try:
            if self.__estado != "PENDIENTE":
                raise ReservaInvalidaError(f"No se puede confirmar la reserva [{self.id_reserva}] porque su estado actual es '{self.__estado}'.")
        except ReservaInvalidaError as err:
            logger.error(f"Fallo al confirmar reserva [{self.id_reserva}]: {err}")
            raise
        else:
            self.__estado = "CONFIRMADA"
            logger.info(f"Reserva [{self.id_reserva}] confirmada con éxito.")
            print(f"✓ ÉXITO: Reserva [{self.id_reserva}] confirmada exitosamente.")
            return True
        finally:
            print(f"-> Estado final de la reserva [{self.id_reserva}]: '{self.__estado}'")

    def procesar_pago(self, monto_abonado: float) -> bool:
        """
        Procesa el pago y transiciona el estado a PROCESADA.
        Estructura con bloques try/except/else/finally.
        """
        logger.info(f"Iniciando procesamiento de pago de ${monto_abonado:,.2f} para la reserva [{self.id_reserva}]...")
        try:
            if self.__estado != "CONFIRMADA":
                raise ReservaInvalidaError(f"Imposible procesar pago. La reserva [{self.id_reserva}] debe estar CONFIRMADA (Estado actual: '{self.__estado}').")
            if abs(monto_abonado - self.costo_total) > 0.01:
                raise ReservaInvalidaError(f"Monto abonado (${monto_abonado:,.2f}) no coincide con el costo total (${self.costo_total:,.2f}).")
        except ReservaInvalidaError as err:
            logger.error(f"Fallo en procesamiento de pago para reserva [{self.id_reserva}]: {err}")
            raise
        else:
            self.__estado = "PROCESADA"
            logger.info(f"Pago procesado para reserva [{self.id_reserva}]. Total: ${self.costo_total:,.2f}")
            print(f"✓ ÉXITO: Pago de ${monto_abonado:,.2f} registrado. Reserva completada.")
            return True
        finally:
            print(f"-> Transacción finalizada para reserva [{self.id_reserva}]. Estado: '{self.__estado}'")

    def cancelar_reserva(self, motivo: str = "Solicitado por el cliente") -> bool:
        """
        Cancela una reserva si no ha sido procesada previamente.
        Estructura con bloques try/except/else/finally.
        """
        logger.info(f"Evaluando solicitud de cancelación para reserva [{self.id_reserva}]...")
        try:
            if self.__estado == "PROCESADA":
                raise ReservaInvalidaError(f"No es posible cancelar la reserva [{self.id_reserva}] porque ya fue PROCESADA y pagada.")
            if self.__estado == "CANCELADA":
                raise ReservaInvalidaError(f"La reserva [{self.id_reserva}] ya se encontraba CANCELADA.")
        except ReservaInvalidaError as err:
            logger.error(f"Error en solicitud de cancelación para reserva [{self.id_reserva}]: {err}")
            raise
        else:
            self.__estado = "CANCELADA"
            logger.info(f"Reserva [{self.id_reserva}] cancelada. Motivo: {motivo}")
            print(f"✓ ÉXITO: Reserva [{self.id_reserva}] cancelada. Motivo: {motivo}")
            return True
        finally:
            print(f"-> Verificación de cancelación terminada. Estado actual: '{self.__estado}'")

    def resumen(self) -> str:
        return (
            f"RESERVA [{self.id_reserva}] - Estado: {self.__estado}\n"
            f"  Cliente  : {self.cliente.nombre} (Doc: {self.cliente.cedula})\n"
            f"  Servicio : {self.servicio.obtener_descripcion()} | Total: ${self.costo_total:,.2f}\n"
            f"  Fecha    : {self.fecha}\n"
            f"  Total    : ${self.costo_total:,.2f}"
        )

    def __str__(self) -> str:
        return f"Reserva[{self.id_reserva} | Cliente: {self.cliente.nombre} | Estado: {self.__estado} | Total: ${self.costo_total:,.2f}]"


if __name__ == "__main__":
    from modulo_servicio import ServicioSala
    print("="*65)
    print("      PRUEBA INTEGRADA MÓDULO 4: CLASE RESERVA (SOFTWARE FJ)     ")
    print("="*65)
    
    cli = Cliente("1012345678", "William Sanchez", "william.sanchez@ejemplo.com", "3001234567")
    ser = ServicioSala("SALA-02", "Auditorio Central", 50000.0, 80, True)
    res = Reserva("RES-001", cli, ser, "2026-12-20", 4.0)

    print("\n--- RESUMEN INICIAL DE LA RESERVA ---")
    print(res.resumen())

    print("\n[PROCESANDO CONFIRMACIÓN DE RESERVA RES-001]...")
    res.confirmar_reserva()

    print("\n[PROCESANDO PAGO DE RESERVA RES-001]...")
    res.procesar_pago(res.costo_total)

    print("\n[PROCESANDO CANCELACIÓN DE RESERVA RES-001]...")
    try:
        res.cancelar_reserva()
    except ReservaInvalidaError as e:
        print(f"\n✓ Excepción capturada correctamente al cancelar reserva procesada:\n  {e}")
    print("="*65)
