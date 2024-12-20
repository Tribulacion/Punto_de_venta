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

    # Métodos de busqueda ==============================================================================================
    @classmethod
    def buscar_por_correo(cls, correo):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(f"SELECT * FROM usuarios WHERE correo = '{correo}'")
                usuario = cursor.fetchone()
                log.debug(f'Usuario encontrado: {usuario}')
                return usuario

    @classmethod
    def mostrar_usuarios_administradores(cls):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(f"SELECT * FROM usuarios WHERE rol = 'Administrador'")
                usuarios = cursor.fetchall()
                log.debug(f'Usuarios encontrados: {usuarios}')
                return usuarios

class ProductoDAO:
    """
    create table productos (
    id bigint primary key generated always as identity,
    nombre text not null,
    descripcion text,
    precio numeric(10, 2) not null,
    stock_actual int not null,
    stock_minimo int not null,
    codigo_barras text unique not null,
    id_proveedor bigint references proveedores (id)
    );
    """
    @staticmethod
    def aumentar_id():
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT MAX(id) FROM productos")
                id = cursor.fetchone()[0]
                if id is None:
                    log.debug('No hay productos, se asigna id 1')
                    return 1
                log.debug(f'Id aumentado: {id + 1}')
                return id + 1

    # Sentencias SQL ===================================================================================================
    _SELECT = "SELECT * FROM productos"
    _INSERT = "INSERT INTO productos(nombre, descripcion, precio, stock_actual, stock_minimo, codigo_barras, id_proveedor) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    _UPDATE = "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock_actual=%s, stock_minimo=%s, codigo_barras=%s, id_proveedor=%s WHERE id=%s"
    _DELETE = "DELETE FROM productos WHERE id=%s"

    # Constructor ======================================================================================================
    def __init__(self, nombre:str, descripcion:str, precio:float, stock_actual:int, stock_minimo:int, codigo_barras:str, id_proveedor:int):
        self.id_producto = self.aumentar_id()
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.codigo_barras = codigo_barras
        self.id_proveedor = id_proveedor

    # Setters y Getters ================================================================================================
    @property
    def id_producto(self):
        log.debug(f'Obteniendo id: {self._id_producto}')
        return self._id_producto

    @id_producto.setter
    def id_producto(self, id: int):
        self._id_producto = id
        log.debug(f'Asignando id: {self._id_producto}')

    @property
    def nombre(self):
        log.debug(f'Obteniendo nombre: {self._nombre}')
        return self._nombre

    @nombre.setter
    def nombre(self, nombre:str):
        if not isinstance(nombre, str):
            log.debug(f'Nombre debe ser de tipo str')
            raise ValueError('Nombre debe ser de tipo str')
        self._nombre = nombre
        log.debug(f'Asignando nombre: {self._nombre}')

    @property
    def descripcion(self):
        log.debug(f'Obteniendo descripcion: {self._descripcion}')
        return self._descripcion

    @descripcion.setter
    def descripcion(self, descripcion:str):
        if not isinstance(descripcion, str):
            log.debug(f'Descripcion debe ser de tipo str')
            raise ValueError('Descripcion debe ser de tipo str')
        self._descripcion = descripcion
        log.debug(f'Asignando descripcion: {self._descripcion}')

    @property
    def precio(self):
        log.debug(f'Obteniendo precio: {self._precio}')
        return self._precio

    @precio.setter
    def precio(self, precio:float):
        if not isinstance(precio, float):
            log.debug(f'Precio debe ser de tipo float')
            raise ValueError('Precio debe ser de tipo float')
        self._precio = precio
        log.debug(f'Asignando precio: {self._precio}')

    @property
    def stock_actual(self):
        log.debug(f'Obteniendo stock actual: {self._stock_actual}')
        return self._stock_actual

    @stock_actual.setter
    def stock_actual(self, stock_actual:int):
        if not isinstance(stock_actual, int):
            log.debug(f'Stock actual debe ser de tipo int')
            raise ValueError('Stock actual debe ser de tipo int')
        self._stock_actual = stock_actual
        log.debug(f'Asignando stock actual: {self._stock_actual}')

    @property
    def stock_minimo(self):
        log.debug(f'Obteniendo stock minimo: {self._stock_minimo}')
        return self._stock_minimo

    @stock_minimo.setter
    def stock_minimo(self, stock_minimo:int):
        if not isinstance(stock_minimo, int):
            log.debug(f'Stock minimo debe ser de tipo int')
            raise ValueError('Stock minimo debe ser de tipo int')
        self._stock_minimo = stock_minimo
        log.debug(f'Asignando stock minimo: {self._stock_minimo}')

    @property
    def codigo_barras(self):
        log.debug(f'Obteniendo codigo de barras: {self._codigo_barras}')
        return self._codigo_barras

    @codigo_barras.setter
    def codigo_barras(self, codigo_barras:str):
        if not isinstance(codigo_barras, str):
            log.debug(f'Codigo de barras debe ser de tipo str')
            raise ValueError('Codigo de barras debe ser de tipo str')
        self._codigo_barras = codigo_barras
        log.debug(f'Asignando codigo de barras: {self._codigo_barras}')

    @property
    def id_proveedor(self):
        log.debug(f'Obteniendo id de proveedor: {self._id_proveedor}')
        return self._id_proveedor

    @id_proveedor.setter
    def id_proveedor(self, id_proveedor:int):
        if not isinstance(id_proveedor, int):
            log.debug(f'Id de proveedor debe ser de tipo int')
            raise ValueError('Id de proveedor debe ser de tipo int')
        self._id_proveedor = id_proveedor
        log.debug(f'Asignando id de proveedor: {self._id_proveedor}')

    # Métodos especiales ===============================================================================================
    def __str__(self):
        log.debug(f'Obteniendo representacion en cadena')
        return f'Producto: {self.id_producto} {self.nombre} {self.descripcion} {self.precio} {self.stock_actual} {self.stock_minimo} {self.codigo_barras} {self.id_proveedor}'

    # Métodos estáticos ================================================================================================
    @classmethod
    def seleccionar(cls):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(cls._SELECT)
                registros = cursor.fetchall()
                log.debug(f'Metodo seleccionar productos')
                return registros

    @classmethod
    def insertar(cls, producto):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                valores = (producto.nombre, producto.descripcion, producto.precio, producto.stock_actual, producto.stock_minimo, producto.codigo_barras, producto.id_proveedor)
                cursor.execute(cls._INSERT, valores)
                log.debug(f'Producto insertado: {producto}')
                return cursor.rowcount

    @classmethod
    def actualizar(cls, producto):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                # Verificar si el producto existe
                if not cls.buscar_por_id(producto.id_producto):
                    log.debug(f'Producto con id {producto.id_producto} no existe')
                    return 0
                # Actualizar el producto
                valores = (producto.nombre, producto.descripcion, producto.precio, producto.stock_actual, producto.stock_minimo, producto.codigo_barras, producto.id_proveedor, producto.id_producto)
                cursor.execute(cls._UPDATE, valores)
                conexion.commit()
                log.debug(f'Producto actualizado: {producto}')
                return cursor.rowcount

    @classmethod
    def eliminar(cls, producto):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                valores = (producto.id_producto,)
                cursor.execute(cls._DELETE, valores)
                log.debug(f'Producto eliminado: {producto}')
                return cursor.rowcount

    # Métodos de busqueda ==============================================================================================
    @classmethod
    def buscar_por_codigo_barras(cls, codigo_barras):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(f"SELECT * FROM productos WHERE codigo_barras = '{codigo_barras}'")
                producto = cursor.fetchone()
                log.debug(f'Producto encontrado: {producto}')
                return producto

    @classmethod
    def buscar_por_nombre(cls, nombre):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(f"SELECT * FROM productos WHERE nombre = '{nombre}'")
                producto = cursor.fetchone()
                log.debug(f'Producto encontrado: {producto}')
                return producto

    @classmethod
    def buscar_por_proveedor(cls, id_proveedor):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(f"SELECT * FROM productos WHERE id_proveedor = {id_proveedor}")
                productos = cursor.fetchall()
                log.debug(f'Productos encontrados: {productos}')
                return productos

    @classmethod
    def buscar_por_id(cls, id_producto):
        with Conexion.obtener_conexion() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(f"SELECT * FROM productos WHERE id = {id_producto}")
                producto = cursor.fetchone()
                log.debug(f'Producto encontrado: {producto}')
                return producto

class VentasDAO:
    pass

class DetalleVentaDAO:
    pass

class PromocionesDAO:
    pass

class HistorialProductoDAO:
    pass

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

    # Prueba de ProductoDAO
    # # Insertar un producto
    # producto = ProductoDAO(nombre='Producto 1', descripcion='Descripcion 1', precio=100.0, stock_actual=10, stock_minimo=5, codigo_barras='1234567890', id_proveedor=2)
    # ProductoDAO.insertar(producto)
    # log.debug(f'Producto insertado: {producto}')

    # Seleccionar productos
    productos = ProductoDAO.seleccionar()
    for producto in productos:
        log.debug(producto)
    #
    # Actualizar un producto
    producto = ProductoDAO(nombre='Producto 1 Actualizado', descripcion='Descripcion 1 Actualizada', precio=200.0, stock_actual=20, stock_minimo=10, codigo_barras='1234567890', id_proveedor=2)
    ProductoDAO.actualizar(producto)
    log.debug(f'Producto actualizado: {producto}')
    #
    # # Eliminar un producto
    # producto = ProductoDAO(id_producto=1)
    # ProductoDAO.eliminar(producto)
    # log.debug(f'Producto eliminado: {producto}')
    #
    # # Buscar producto por codigo de barras
    # producto = ProductoDAO.buscar_por_codigo_barras('1234567890')
    # log.debug(f'Producto encontrado: {producto}')
    #
    # # Buscar producto por nombre
    # producto = ProductoDAO.buscar_por_nombre('Producto 1 Actualizado')
    # log.debug(f'Producto encontrado: {producto}')
    #
    # # Buscar producto por proveedor
    # productos = ProductoDAO.buscar_por_proveedor(2)
    # log.debug(f'Productos encontrados: {productos}')
    #
    # # Buscar producto por id
    # producto = ProductoDAO.buscar_por_id(1)
    # log.debug(f'Producto encontrado: {producto}')
