"""
Definicion de los modelos de la base de datos (tablas)
"""
from logger_base import log
from conexion import Conexion

class ProveedorDAO:
    # Sentencias SQL ===================================================================================================
    _SELECT = "SELECT * FROM proveedores"
    _INSERT = "INSERT INTO proveedores(nombre, telefono, correo, direccion) VALUES(%s, %s, %s, %s)"
    _UPDATE = "UPDATE proveedores SET nombre=%s, telefono=%s, correo=%s, direccion=%s WHERE id=%s"
    _DELETE = "DELETE FROM proveedores WHERE id=%s"

    # Constructor ======================================================================================================
    def __init__(self, id=None, nombre=None, telefono=None, correo=None, direccion=None):
        self._id_proveedor = id
        self._nombre = nombre
        self._telefono = telefono
        self._correo = correo
        self._direccion = direccion

    # Setters y Getters ================================================================================================
    @property
    def id_proveedor(self):
        return self._id_proveedor

    @id_proveedor.setter
    def id_proveedor(self, id):
        self._id_proveedor = id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, telefono):
        self._telefono = telefono

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, correo):
        self._correo = correo

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, direccion):
        self._direccion = direccion

    # Metodos especiales ================================================================================================
    def __str__(self):
        return f'Proveedor: {self.id_proveedor} {self.nombre} {self.telefono} {self.correo} {self.direccion}'

    # Metodos estaticos ================================================================================================
    @classmethod
    def seleccionar(cls):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(cls._SELECT)
                registros = cursor.fetchall()
                return registros

    @classmethod
    def insertar(cls, proveedor):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                valores = (proveedor.nombre, proveedor.telefono, proveedor.correo, proveedor.direccion)
                cursor.execute(cls._INSERT, valores)
                log.debug(f'Proveedor insertado: {proveedor}')
                return cursor.rowcount

    @classmethod
    def actualizar(cls, proveedor):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                valores = (proveedor.nombre, proveedor.telefono, proveedor.correo, proveedor.direccion, proveedor.id_proveedor)
                cursor.execute(cls._UPDATE, valores)
                log.debug(f'Proveedor actualizado: {proveedor}')
                return cursor.rowcount

    @classmethod
    def eliminar(cls, proveedor):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                valores = (proveedor.id_proveedor,)
                cursor.execute(cls._DELETE, valores)
                log.debug(f'Proveedor eliminado: {proveedor}')
                return cursor.rowcount

if __name__ == '__main__':
    # Insertar un registro
    proveedor = ProveedorDAO(nombre='Juan', telefono='1234567890', correo='juan@example.com', direccion='Calle Falsa 123')
    ProveedorDAO.insertar(proveedor)
    log.debug(f'Proveedor insertado: {proveedor}')

    # Seleccionar registros
    proveedores = ProveedorDAO.seleccionar()
    for proveedor in proveedores:
        log.debug(proveedor)

    # Actualizar un registro
    proveedor = ProveedorDAO(id=1, nombre='Juan Actualizado', telefono='0987654321', correo='juan_actualizado@example.com', direccion='Calle Verdadera 456')
    ProveedorDAO.actualizar(proveedor)
    log.debug(f'Proveedor actualizado: {proveedor}')

    # Eliminar un registro
    proveedor = ProveedorDAO(id=1)
    ProveedorDAO.eliminar(proveedor)
    log.debug(f'Proveedor eliminado: {proveedor}')