from logger_base import log
from functools import wraps
from app.conexion import Conexion

# Decorador para gestionar la conexión y el cursor =====================================================================
def gestionar_conexion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conexion = None
        cursor = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            log.debug(f"Conexion y cursor obtenidos: {conexion}, {cursor}")
            result = func(*args, conexion=conexion, cursor=cursor, **kwargs)
            return result
        finally:
            if cursor:
                cursor.close()
            if conexion:
                Conexion.liberar_conexion(conexion)
    return wrapper

# Función para obtener la conexión y el cursor =========================================================================
@gestionar_conexion
def obtener_conexion_y_cursor(conexion, cursor):
    """
    Función para obtener la conexión y el cursor
    :param conexion:
    :param cursor:
    :return: conexion, cursor
    """
    return conexion, cursor


# Clase de modelo DAO===================================================================================================
class ProveedorDAO:
    """
    Clase para gestionar la tabla proveedores de la base de datos
    """
    # Sentencias SQL ===================================================================================================
    _SELECT = "SELECT * FROM proveedores"
    _INSERT = "INSERT INTO proveedores(nombre, telefono, correo, direccion) VALUES(%s, %s, %s, %s)"
    _UPDATE = "UPDATE proveedores SET nombre=%s, telefono=%s, correo=%s, direccion=%s WHERE id=%s"
    _DELETE = "DELETE FROM proveedores WHERE id=%s"

    @staticmethod
    @gestionar_conexion
    def aumentar_id(conexion, cursor):
        cursor.execute("SELECT MAX(id) FROM proveedores")
        id = cursor.fetchone()[0]
        return id + 1

    # Métodos estáticos ================================================================================================
    @classmethod
    @gestionar_conexion
    def seleccionar(cls, conexion, cursor):
        cursor.execute(cls._SELECT)
        registros = cursor.fetchall()
        log.debug(f'Método seleccionar proveedores')
        return registros

    @classmethod
    @gestionar_conexion
    def insertar(cls, conexion, cursor, proveedor):
        valores = (proveedor.nombre, proveedor.telefono, proveedor.correo, proveedor.direccion)
        cursor.execute(cls._INSERT, valores)
        conexion.commit()
        log.debug(f'Proveedor insertado: {proveedor}')
        return cursor.rowcount

    @classmethod
    @gestionar_conexion
    def actualizar(cls, conexion, cursor, proveedor):
        valores = (proveedor.nombre, proveedor.telefono, proveedor.correo, proveedor.direccion, proveedor.id)
        cursor.execute(cls._UPDATE, valores)
        conexion.commit()
        log.debug(f'Proveedor actualizado: {proveedor}')
        return cursor.rowcount

    @classmethod
    @gestionar_conexion
    def eliminar(cls, conexion, cursor, proveedor):
        valores = (proveedor.id,)
        cursor.execute(cls._DELETE, valores)
        conexion.commit()
        log.debug(f'Proveedor eliminado: {proveedor}')
        return cursor.rowcount
    # Fin de la clase ProveedorDAO =====================================================================================


class UsuarioDAO:
    """
    Clase para gestionar la tabla usuarios de la base de datos
    """
    # Metodo estatico para aumentar el id
    @staticmethod
    @gestionar_conexion
    def aumentar_id(conexion, cursor):
        cursor.execute("SELECT MAX(id) FROM usuarios")
        id = cursor.fetchone()[0]
        if id is None:
            return 1
        return id + 1

    # Sentencias SQL ===================================================================================================
    _SELECT = "SELECT * FROM usuarios ORDER BY id ASC"
    _INSERT = "INSERT INTO usuarios(id, nombre, apellido, correo, contrasena, rol, telefono) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    _UPDATE = "UPDATE usuarios SET nombre=%s, apellido=%s, correo=%s, contrasena=%s, rol=%s, telefono=%s WHERE id=%s"
    _DELETE = "DELETE FROM usuarios WHERE id=%s"

    # Métodos estáticos ================================================================================================
    @classmethod
    @gestionar_conexion
    def seleccionar(cls, conexion, cursor):
        cursor.execute(cls._SELECT)
        registros = cursor.fetchall()
        log.debug(f'Metodo seleccionar usuarios')
        return registros

    @classmethod
    @gestionar_conexion
    def insertar(cls, usuario, conexion=None, cursor=None):
        valores = (usuario.id_usuario, usuario.nombre, usuario.apellido, usuario.correo, usuario.contrasena, usuario.rol, usuario.telefono)
        cursor.execute(cls._INSERT, valores)
        conexion.commit()
        log.debug(f'Usuario insertado: {usuario}')
        return cursor.rowcount

    @classmethod
    @gestionar_conexion
    def actualizar(cls, nombre, apellido, correo, contrasena, rol, telefono, id_usuario, conexion=None, cursor=None):
        valores = (nombre, apellido, correo, contrasena, rol, telefono, id_usuario)
        cursor.execute(cls._UPDATE, valores)
        conexion.commit()
        log.debug(f'Usuario actualizado: {id_usuario}')
        return cursor.rowcount

    @classmethod
    @gestionar_conexion
    def eliminar(cls, conexion, cursor, id_usuario):
        valores = (id_usuario,)
        cursor.execute(cls._DELETE, valores)
        conexion.commit()
        log.debug(f'Usuario eliminado: {id_usuario}')
        return cursor.rowcount

    @classmethod
    @gestionar_conexion
    def seleccionar_por_id(cls, conexion, cursor, id_usuario):
        log.debug(f"Ejecutando seleccionar_por_id con id_usuario: {id_usuario}")
        cursor.execute(f"SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
        usuario = cursor.fetchone()
        log.debug(f'Usuario encontrado: {usuario}')
        return usuario

    # Métodos de busqueda ==============================================================================================
    @classmethod
    @gestionar_conexion
    def mostrar_usuarios_administradores(cls, conexion, cursor):
        cursor.execute(f"SELECT * FROM usuarios WHERE rol = 'Administrador'")
        usuarios = cursor.fetchall()
        log.debug(f'Usuarios encontrados: {usuarios}')
        return usuarios

    @classmethod
    @gestionar_conexion
    def seleccionar_por_id(cls, conexion, cursor, id_usuario):
        log.debug(f"Ejecutando seleccionar_por_id con id_usuario: {id_usuario}")
        cursor.execute(f"SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
        usuario = cursor.fetchone()
        log.debug(f'Usuario encontrado: {usuario}')
        return usuario