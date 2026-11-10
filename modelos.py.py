import logging
from abc import ABC, abstractmethod

# Configuración básica del archivo de logs
logging.basicConfig(
    filename='sistema_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- EXCEPCIONES PERSONALIZADAS ---
class ErrorSistemaFJ(Exception):
    pass

class ClienteNoValidoError(ErrorSistemaFJ):
    pass

class ServicioNoDisponibleError(ErrorSistemaFJ):
    pass

class ReservaInvalidaError(ErrorSistemaFJ):
    pass


# --- CLASE ABSTRACTA GENERAL ---
class EntidadBase(ABC):
    @abstractmethod
    def obtener_detalles(self):
        pass


# --- CLASE CLIENTE ---
class Cliente(EntidadBase):
    def __init__(self, identificacion: str, nombre: str, correo: str):
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    @property
    def identificacion(self):
        return self.__identificacion

    @identificacion.setter
    def identificacion(self, valor):
        if not valor or len(valor.strip()) == 0:
            logging.error("Intento de registrar cliente con identificación vacía.")
            raise ClienteNoValidoError("La identificación del cliente no puede estar vacía.")
        self.__identificacion = valor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) == 0:
            logging.error("Intento de registrar cliente con nombre vacío.")
            raise ClienteNoValidoError("El nombre del cliente no puede estar vacío.")
        self.__nombre = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if "@" not in valor:
            logging.error(f"Intento de registrar correo inválido: {valor}")
            raise ClienteNoValidoError("El correo electrónico no es válido.")
        self.__correo = valor

    def obtener_detalles(self) -> str:
        return f"Cliente: {self.nombre} (ID: {self.identificacion}, Correo: {self.correo})"


# --- CLASE ABSTRACTA SERVICIO ---
class Servicio(EntidadBase, ABC):
    def __init__(self, codigo: str, descripcion: str, costo_base: float):
        self.codigo = codigo
        self.descripcion = descripcion
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self) -> float:
        pass

    def calcular_costo_con_opciones(self, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        costo_parcial = self.calcular_costo() * (1 - descuento)
        return costo_parcial * (1 + impuesto)

    def obtener_detalles(self) -> str:
        return f"Servicio [{self.codigo}]: {self.descripcion} - Costo Base: ${self.costo_base}"


# --- SERVICIOS ESPECIALIZADOS ---
class ReservaSala(Servicio):
    def __init__(self, codigo: str, descripcion: str, costo_base: float, capacidad: int):
        super().__init__(codigo, descripcion, costo_base)
        self.capacidad = capacidad

    def calcular_costo(self) -> float:
        return self.costo_base


class AlquilerEquipo(Servicio):
    def __init__(self, codigo: str, descripcion: str, costo_base: float, horas: int):
        super().__init__(codigo, descripcion, costo_base)
        self.horas = horas

    def calcular_costo(self) -> float:
        return self.costo_base * self.horas


class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo: str, descripcion: str, costo_base: float, nivel_experticia: str):
        super().__init__(codigo, descripcion, costo_base)
        self.nivel_experticia = nivel_experticia

    def calcular_costo(self) -> float:
        multiplicador = 1.5 if self.nivel_experticia.lower() == "senior" else 1.0
        return self.costo_base * multiplicador


# --- CLASE RESERVA ---
class Reserva:
    def __init__(self, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.estado = "Pendiente"

    def confirmar_reserva(self):
        try:
            if self.duracion_horas <= 0:
                raise ReservaInvalidaError("La duración de la reserva debe ser mayor a 0 horas.")
            self.estado = "Confirmada"
            logging.info(f"Reserva confirmada exitosamente para {self.cliente.nombre}.")
        except Exception as e:
            logging.error(f"Error al confirmar la reserva: {e}")
            self.estado = "Fallida"
            raise
        finally:
            print(f"Estado final del proceso de reserva: {self.estado}")

    def cancelar_reserva(self):
        self.estado = "Cancelada"
        logging.info(f"Reserva cancelada para el cliente {self.cliente.nombre}.")