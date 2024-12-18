"""
Definicion de los modelos de la base de datos (tablas)
"""
import hashlib
from logger_base import log
from conexion import Conexion

# Clases de los modelos ================================================================================================
class ProveedorDAO:
    # Sentencias SQL ===================================================================================================
    _SELECT = "SELECT * FROM proveedores"
    _INSERT = "INSERT INTO proveedores(nombre, telefono, correo, direccion) VALUES(%s, %s, %s, %s)"
    _UPDATE = "UPDATE proveedores SET nombre=%s, telefono=%s, correo=%s, direccion=%s WHERE id=%s"
    _DELETE = "DELETE FROM proveedores WHERE id=%s"

    @staticmethod
    def aumentar_id():
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT MAX(id) FROM proveedores")
                id = cursor.fetchone()[0]
                return id + 1

    # Constructor ======================================================================================================
    def __init__(self, nombre:str=None, telefono:str=None, correo:str=None, direccion:str=None):
        self.id_proveedor = self.aumentar_id()
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion

    # Setters y Getters ================================================================================================
    @property
    def id_proveedor(self):
        log.debug(f'Obteniendo id: {self._id_proveedor}')
        return self._id_proveedor

    @id_proveedor.setter
    def id_proveedor(self, id):
        self._id_proveedor = id
        log.debug(f'Asignando id: {self._id_proveedor}')

    @property
    def nombre(self):
        log.debug(f'Obteniendo nombre: {self._nombre}')
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        if not isinstance(nombre, str):
            log.debug(f'Nombre debe ser de tipo str')
            raise ValueError('Nombre debe ser de tipo str')
        log.debug(f'Asignando nombre: {nombre}')
        self._nombre = nombre

    @property
    def telefono(self):
        log.debug(f'Obteniendo telefono: {self._telefono}')
        return self._telefono

    @telefono.setter
    def telefono(self, telefono):
        if not isinstance(telefono, str):
            log.debug(f'Telefono debe ser de tipo str')
            raise ValueError('Telefono debe ser de tipo str')
        log.debug(f'Asignando telefono: {telefono}')
        self._telefono = telefono

    @property
    def correo(self):
        log.debug(f'Obteniendo correo: {self._correo}')
        return self._correo

    @correo.setter
    def correo(self, correo):
        if not isinstance(correo, str):
            log.debug(f'Correo debe ser de tipo str')
            raise ValueError('Correo debe ser de tipo str')
        log.debug(f'Asignando correo: {correo}')
        self._correo = correo

    @property
    def direccion(self):
        log.debug(f'Obteniendo direccion: {self._direccion}')
        return self._direccion

    @direccion.setter
    def direccion(self, direccion):
        if not isinstance(direccion, str):
            log.debug(f'Direccion debe ser de tipo str')
            raise ValueError('Direccion debe ser de tipo str')
        log.debug(f'Asignando direccion: {direccion}')
        self._direccion = direccion

    # Metodos especiales ================================================================================================
    def __str__(self):
        log.debug(f'Obteniendo representacion en cadena')
        return f'Proveedor: {self.id_proveedor} {self.nombre} {self.telefono} {self.correo} {self.direccion}'

    # Metodos estaticos ================================================================================================
    @classmethod
    def seleccionar(cls):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(cls._SELECT)
                registros = cursor.fetchall()
                log.debug(f'Metodo seleccionar proveedores')
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


class UsuarioDAO:
    # Metodo estatico para aumentar el id
    @staticmethod
    def aumentar_id():
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT MAX(id) FROM usuarios")
                id = cursor.fetchone()[0]
                if id is None:
                    return 1
                return id + 1

    # Sentencias SQL ===================================================================================================
    _SELECT = "SELECT * FROM usuarios"
    _INSERT = "INSERT INTO usuarios(nombre, apellido, correo, contrasena, rol, telefono) VALUES(%s, %s, %s, %s, %s, %s)"
    _UPDATE = "UPDATE usuarios SET nombre=%s, apellido=%s, correo=%s, contrasena=%s, rol=%s, telefono=%s WHERE id=%s"
    _DELETE = "DELETE FROM usuarios WHERE id=%s"

    # Constructor ======================================================================================================
    def __init__(self, nombre:str, apellido:str, correo:str, contrasena:str, rol:str, telefono:str):
        self.id_usuario = self.aumentar_id()
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol
        self.telefono = telefono

    # Setters y Getters ================================================================================================
    @property
    def id_usuario(self):
        log.debug(f'Obteniendo id: {self._id_usuario}')
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, id):
        self._id_usuario = id
        log.debug(f'Asignando id: {self._id_usuario}')

    @property
    def nombre(self):
        log.debug(f'Obteniendo nombre: {self._nombre}')
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        if not isinstance(nombre, str):
            raise ValueError('Nombre debe ser de tipo str')
        self._nombre = nombre
        log.debug(f'Asignando nombre: {self._nombre}')

    @property
    def apellido(self):
        log.debug(f'Obteniendo apellido: {self._apellido}')
        return self._apellido

    @apellido.setter
    def apellido(self, apellido):
        if not isinstance(apellido, str):
            raise ValueError('Apellido debe ser de tipo str')
        self._apellido = apellido
        log.debug(f'Asignando apellido: {self._apellido}')

    @property
    def correo(self):
        log.debug(f'Obteniendo correo: {self._correo}')
        return self._correo

    @correo.setter
    def correo(self, correo):
        if not isinstance(correo, str):
            raise ValueError('Correo debe ser de tipo str')
        self._correo = correo
        log.debug(f'Asignando correo: {self._correo}')

    @property
    def contrasena(self):
        log.debug(f'Obteniendo contraseña')
        return self._contrasena

    @contrasena.setter
    def contrasena(self, contrasena):
        if not isinstance(contrasena, str):
            raise ValueError('Contraseña debe ser de tipo str')
        # Encriptar la contrasena
        self._contrasena = encriptar_contrasena(contrasena)
        log.debug(f'Asignando contraseña')

    @property
    def rol(self):
        log.debug(f'Obteniendo rol: {self._rol}')
        return self._rol

    @rol.setter
    def rol(self, rol):
        if not isinstance(rol, str):
            raise ValueError('Rol debe ser de tipo str')
        self._rol = rol
        log.debug(f'Asignando rol: {self._rol}')

    @property
    def telefono(self):
        log.debug(f'Obteniendo telefono: {self._telefono}')
        return self._telefono

    @telefono.setter
    def telefono(self, telefono):
        if not isinstance(telefono, str):
            raise ValueError('Telefono debe ser de tipo str')
        self._telefono = telefono
        log.debug(f'Asignando telefono: {self._telefono}')

    # Métodos especiales ===============================================================================================
    def __str__(self):
        log.debug(f'Obteniendo representacion en cadena')
        return f'''Usuario: {self.id_usuario} {self.nombre} {self.apellido} {self.correo} {self.rol} {self.telefono}
                    Contraseña: {self.contrasena}'''

    # Métodos estáticos ================================================================================================
    @classmethod
    def seleccionar(cls):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(cls._SELECT)
                registros = cursor.fetchall()
                log.debug(f'Metodo seleccionar usuarios')
                return registros

    @classmethod
    def insertar(cls, usuario):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                valores = (usuario.nombre, usuario.apellido, usuario.correo, usuario.contrasena, usuario.rol, usuario.telefono)
                cursor.execute(cls._INSERT, valores)
                log.debug(f'Usuario insertado: {usuario}')
                return cursor.rowcount

    @classmethod
    def actualizar(cls, usuario):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                valores = (usuario.nombre, usuario.apellido, usuario.correo, usuario.contrasena, usuario.rol, usuario.telefono, usuario.id_usuario)
                cursor.execute(cls._UPDATE, valores)
                log.debug(f'Usuario actualizado: {usuario}')
                return cursor.rowcount

    @classmethod
    def eliminar(cls, usuario):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                valores = (usuario.id_usuario,)
                cursor.execute(cls._DELETE, valores)
                log.debug(f'Usuario eliminado: {usuario}')
                return cursor.rowcount

    @classmethod
    def buscar_por_correo(cls, correo):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(f"SELECT * FROM usuarios WHERE correo = '{correo}'")
                usuario = cursor.fetchone()
                log.debug(f'Usuario encontrado: {usuario}')
                return usuario


# Funciones de prueba ==================================================================================================
def encriptar_contrasena(contrasena: str):
    hashed_password = hashlib.sha256(contrasena.encode()).hexdigest()
    log.debug('Contraseña encriptada')
    return hashed_password


if __name__ == '__main__':
    """
    PRUEBAS DE LOS MODELOS DE LA BASE DE DATOS PROVEEDOR
    
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
    log.debug(f'Proveedor eliminado: {proveedor}')"""

    """
    PRUEBA DE LOS MODELOS DE LA BASE DE DATOS USUARIO
    # Creacion de un usuario y prueba de contrasena encriptada
    usuario = UsuarioDAO(nombre='Carlos', apellido='Monroy', correo='monroyC98@gmail.com', contrasena='Hola123', rol='Administrador', telefono='1234567890')
    print(usuario)"""

    """# Prueba del insertar usuario como administrador
    usuario = UsuarioDAO(nombre='admin', apellido='admin', correo='admin@admin.com', contrasena='admin', rol='Administrador', telefono='1234567890')
    UsuarioDAO.insertar(usuario)
    # Mostrar usuarios
    usuarios = UsuarioDAO.seleccionar()
    for usuario in usuarios:
        print(usuario)"""
    