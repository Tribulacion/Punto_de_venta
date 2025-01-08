"""
Definición de las ventanas de la aplicación
"""
import tkinter as tk
from tkinter import ttk, messagebox
from app.modelos_dao import UsuarioDAO
from app.modelos import Usuario, encriptar_contrasena
from logger_base import log

COLOR_FONDO = '#1A3E66'                 # Azul Oscuro
COLOR_CREMA = '#D6D3BD'                 # Crema
COLOR_PRUEBA = '#AA870C'                # Dorado
COLOR_SELECCION_REGISTRO = '#1F446E'    # Azul Claro


def centrar_ventana(root, width, height):
    ancho = root.winfo_screenwidth()
    alto = root.winfo_screenheight()
    x = (ancho / 2) - (width / 2)
    y = (alto / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    log.debug(f"Ventana centrada en x={x}, y={y}")

def definir_pantalla_completa(root):
    # Funcion para que la ventana sea de los pixeles de la pantalla
    root.state('zoomed')  # Maximizar la ventana
    log.debug(f"Ventana maximizada")

class App(tk.Tk):
    # Variables globales ===============================================================================================
    COLOR_FONDO = '#1A3E66'                 # Azul Oscuro
    COLOR_CREMA = '#D6D3BD'                 # Crema
    COLOR_PRUEBA = '#AA870C'                # Dorado
    COLOR_SELECCION_REGISTRO = '#1F446E'    # Azul Claro

    ANCHO = 400
    ALTO = 250

    # Constructor ======================================================================================================
    def __init__(self):
        log.debug("Iniciando aplicación: Login")
        super().__init__()
        self.id_cliente = None
        self.cargar_estilos()
        self.configurar_ventana()
        self.configurar_grid()
        self.crear_widgets()

        log.debug("Aplicación iniciada exitosamente")

    # Estilos ==========================================================================================================
    def cargar_estilos(self):
        log.debug("Cargando estilos")

        # Estilos de la tabla
        self.estilos = ttk.Style()
        self.estilos.configure('Treeview',
                                background=self.COLOR_PRUEBA, # Cambiar a COLOR_SELECCION_REGISTRO
                                foreground='white',
                                fieldbackground=self.COLOR_SELECCION_REGISTRO,  # Cambiar a COLOR_SELECCION_REGISTRO
                                rowheight=30
                                )

    # Creacion de la ventana de login ==================================================================================
    def configurar_ventana(self):
        log.debug("Configurando ventana")
        self.geometry(f'{self.ANCHO}x{self.ALTO}')
        self.title('Login')
        self.configure(background=self.COLOR_FONDO)
        self.resizable(width=False, height=False)
        centrar_ventana(self, self.ANCHO, self.ALTO)

    def configurar_grid(self):
        log.debug("Configurando grid")
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

    def crear_widgets(self):
        log.debug("Creando widgets")
        """
        los widgets son los elementos que conforman la interfaz gráfica de usuario
        - Frame con titulo
        - Frame para tabla, formularios de registro y botones
        """
        self.mostrar_titulo()

        self.mostrar_tabla()
        self.mostrar_formulario()
        self.mostrar_botones()

    def mostrar_titulo(self):
        log.debug("Mostrando título")
        frame_titulo = tk.Frame(self, bg=self.COLOR_FONDO)

        lbl_titulo = tk.Label(frame_titulo,
                                text='Login',
                                bg=self.COLOR_FONDO,  # Cambiar a COLOR_FONDO
                                fg='white',
                                font=('Arial', 20),
                                padx=10,
                                pady=10,
                                anchor=tk.CENTER)
        lbl_titulo.pack(expand=True, fill='both')

        frame_titulo.grid(row=0, column=0, columnspan=2, sticky='nsew')

    def mostrar_tabla(self):
        log.debug("Mostrando tabla")
        # Crear un frame para la tabla con tamaño ajustado
        self.frame_tabla = tk.Frame(self,
                                    bg=self.COLOR_FONDO,  # Cambiar a COLOR_FONDO
                                    bd=1,
                                    height=200,  # Ajustar la altura
                                    width=50,   # Ajustar el ancho
                                    relief='raised')
        self.frame_tabla.columnconfigure(0, weight=1)

        # Configurar la tabla y cargar los registros
        self.configurar_tabla()
        self.cargar_registros_en_tabla()

        self.frame_tabla.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)  # Ajustar el padding

    def mostrar_formulario(self):
        log.debug("Mostrando formulario")
        self.configurar_formulario()
        self.labels_cajas_texto_formulario()

    def mostrar_botones(self):
        log.debug("Mostrando botones")
        # Crear un frame para los botones
        self.configurar_frame_botones()
        self.crear_botones()

    # Eventos ==========================================================================================================
    def _salir(self):
        log.debug("Saliendo de la aplicación")
        self.quit()
        log.debug("Aplicación finalizada exitosamente")

    def _login(self, event=None):
        log.debug("Iniciando login")

        if self.validar_campos():
            usuario = self.usuario.get()
            password = encriptar_contrasena(self.password.get())

            # Verificar los usuarios cargados en la base de datos
            for registro in self._registros:
                if registro[1] == usuario and registro[4] == password:
                    messagebox.showinfo(title='Login exitoso', message='Bienvenido!')
                    self.limpiar_formulario()
                    self.llamar_ventana_principal()
                    log.debug("Login finalizado")
                    self.destroy()
                    return

        messagebox.showerror(title='Login fallido', message='Usuario o contraseña incorrectos')
        self.limpiar_formulario()
        log.debug("Login fallido")

    def validar_campos(self):
        log.debug("Validando campos")
        """
        Validar que los campos no estén vacíos
        """
        if not self.usuario.get():
            messagebox.showwarning(title='Campo vacío', message='Por favor seleccione un usuario')
            self.txt_usuario.focus()
            return False
        if not self.password.get():
            messagebox.showwarning(title='Campo vacío', message='Por favor llene el campo de contraseña')
            self.txt_password.focus()
            return False
        return True

    def llamar_ventana_principal(self):
        log.debug("Llamando a la ventana principal")
        # Implementar la lógica para llamar a la ventana principal
        VentanaPrincipal()

    # Metodos tabla ====================================================================================================
    def configurar_tabla(self):
        log.debug("Configurando tabla")

        # Definir las columnas de la tabla
        columnas = ('Nombre')

        # Crear la tabla
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show='headings')
        # Agregar los encabezados de la tabla
        self.tabla.heading('Nombre', text='Nombre', anchor=tk.CENTER)
        # Definir las columnas de la tabla
        self.tabla.column('Nombre', width=100, anchor=tk.CENTER)
        # Agregamos barra de scroll
        scroll = ttk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        scroll.grid(row=0, column=1, sticky='ns')
        self.tabla.configure(yscrollcommand=scroll.set)


        self.tabla.grid(row=0, column=0, sticky='nsew')

    def cargar_registros_en_tabla(self):
        log.debug("Cargando registros en tabla")

        # Caragamos los registros de la base de datos
        self._registros = UsuarioDAO.seleccionar()
        for registro in self._registros:
            self.tabla.insert(parent='', index=tk.END, values=(registro[1]))

        # Asociar el evento SELECT a la tabla
        self.tabla.bind('<<TreeviewSelect>>', self.cargar_registro_en_formulario)

    # Metodos formulario ===============================================================================================
    def configurar_formulario(self):
        log.debug("Configurando formulario")
        """
        Configurar los campos del formulario
        """
        self.frame_fomulario_botones = tk.Frame(self, bg=self.COLOR_FONDO, bd=1, relief='raised')
        self.frame_fomulario_botones.columnconfigure(0, weight=1)

        self.frame_fomulario_botones.rowconfigure(0, weight=0)
        self.frame_fomulario_botones.rowconfigure(1, weight=0)
        self.frame_fomulario_botones.rowconfigure(2, weight=1)  # Para el frame de los botones

        self.frame_fomulario_botones.grid(row=1, column=1, sticky='nsew')

    def labels_cajas_texto_formulario(self):
        log.debug("Creando campos del formulario")
        color_letra = 'white'

        # Crear los campos del formulario
        # Nombre
        lbl_usuario = tk.Label(self.frame_fomulario_botones,    # Frame donde se encuentra el label
                                text='Usuario',                 # Texto del label
                                bg=self.COLOR_FONDO,            # Color de fondo del label
                                fg=color_letra)                     # Color de la letra del label
        lbl_usuario.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=10)
        self.usuario = tk.StringVar()
        self.txt_usuario = tk.Entry(self.frame_fomulario_botones, textvariable=self.usuario)
        self.txt_usuario.grid(row=0, column=1, sticky=tk.EW, padx=10, pady=10)

        # Contraseña
        lbl_password = tk.Label(self.frame_fomulario_botones,
                                text='Contraseña',
                                bg=self.COLOR_FONDO,
                                fg=color_letra)
        lbl_password.grid(row=1, column=0, sticky=tk.EW, padx=10, pady=10)
        self.password = tk.StringVar()
        self.txt_password = tk.Entry(self.frame_fomulario_botones, textvariable=self.password, show='*')
        self.txt_password.grid(row=1, column=1, sticky=tk.EW, padx=10, pady=10)

        # que al iniciar la aplicacion el focus este en la caja de contraseña
        self.txt_password.focus()

        # Eventos bind
        self.txt_password.bind('<Return>', self._login)

    def limpiar_formulario(self):
        log.debug("Limpiando formulario")
        """
        Limpiar los campos del formulario
        """
        self.id_cliente = None
        self.txt_usuario.delete(0, tk.END)
        self.txt_password.delete(0, tk.END)
        self.txt_password.focus()

    def cargar_registro_en_formulario(self, event):
        log.debug("Cargando registro en formulario")
        """
        Cargar los datos del registro en el formulario
        """
        self.limpiar_formulario()

        # Obtener el id del registro seleccionado y cargar el nombre el formulario
        seleccion = self.tabla.selection()
        id_cliente = self.tabla.item(seleccion)['values'][0]
        self.id_cliente = id_cliente

        # Mostar el nombre en el formulario
        self.txt_usuario.delete(0, tk.END)
        self.txt_usuario.insert(0, id_cliente)

    # Metodos botones ==================================================================================================
    def configurar_frame_botones(self):
        log.debug("Configurando frame de botones")
        self.frame_botones = tk.Frame(self.frame_fomulario_botones, bg=self.COLOR_FONDO)

        self.frame_botones.columnconfigure(0, weight=1)
        self.frame_botones.columnconfigure(1, weight=1)

        self.frame_botones.grid(row=2, column=0, columnspan=2, sticky='nsew')

    def crear_botones(self):
        log.debug("Creando botones")
        color = 'white'

        # Boton de login
        btn_login = tk.Button(self.frame_botones,
                                text='Iniciar Sesión',
                                # bg=self.COLOR_CREMA,
                                # fg=color,
                                command=self._login)
        btn_login.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Boton de salir
        btn_salir = tk.Button(self.frame_botones,
                                text='Salir',
                                # bg=self.COLOR_CREMA,
                                # fg=color,
                                command=self._salir)
        btn_salir.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
    # Fin de la clase App //////////////////////////////////////////////////////////////////////////////////////////////


class VentanaPrincipal(tk.Tk):
    # Variables globales ===============================================================================================
    ANCHO_MINIMO = 1000
    ALTO_MINIMO = 700

    # Constructor ======================================================================================================
    def __init__(self):
        log.debug("Iniciando aplicación: Ventana Principal")
        super().__init__()
        self.configurar_ventana_principal()
        self.crear_componentes()
        self.imagen_foto = None

        log.debug("Aplicación iniciada exitosamente")

    # Estilos ==========================================================================================================


    # Creacion de la ventana de login ==================================================================================
    def crear_componentes(self):
        log.debug("Creando componentes")
        self.crear_barra_navegacion_ventana_principal()
        self.botones_superiores_ventana_principal()

    def configurar_ventana_principal(self):
        log.debug("Configurando ventana")
        self.title('Ventana Principal')
        definir_pantalla_completa(self)
        self.minsize(width=self.ANCHO_MINIMO, height=self.ALTO_MINIMO)
        self.configure(background=COLOR_FONDO)
        self.frame_principal = tk.Frame(self, bg=COLOR_FONDO)
        self.frame_principal.pack(fill='both', expand=True)

    def crear_barra_navegacion_ventana_principal(self):
        log.debug("Creando barra de navegación")
        self.barra_menu = tk.Menu(self)
        self.config(menu=self.barra_menu)

        """                                    Menu                                                """
        menu_archivo = tk.Menu(self.barra_menu, tearoff=0)  # tearoff=0: No se puede separar del menu
        self.barra_menu.add_cascade(label="Acerca de.", menu=menu_archivo)

        menu_archivo.add_command(label="Nosotros", command=lambda: print("Nosotros"))

    def botones_superiores_ventana_principal(self):
        log.debug("Creando botones superiores")
        self.frame_botones = tk.Frame(self.frame_principal, bg=COLOR_PRUEBA)

        self.btn_abrir_turno = tk.Button(self.frame_botones,
                                    text='Abrir Turno',
                                    command=self.abrir_turno)
        self.btn_abrir_turno.pack(side='left', padx=10, pady=10)

        self.btn_cerrar_turno = tk.Button(self.frame_botones,
                                    text='Cerrar Turno',
                                    command=self.cerrar_turno,
                                    state='disabled')
        self.btn_cerrar_turno.pack(side='left', padx=10, pady=10)

        self.btn_alta_usuarios = tk.Button(self.frame_botones,
                                            text='Mostrar Usuarios',
                                            command=self.mostrar_usuarios)
        self.btn_alta_usuarios.pack(side='left', padx=10, pady=10)

        self.frame_botones.pack(fill='x')

    # Eventos ==========================================================================================================
    def abrir_turno(self):
        log.debug("Abriendo turno")
        # Implementar la lógica para abrir turno
        self.btn_abrir_turno.config(state='disabled')
        self.btn_cerrar_turno.config(state='normal')

    def cerrar_turno(self):
        log.debug("Cerrando turno")
        # Implementar la lógica para cerrar turno
        self.btn_abrir_turno.config(state='normal')
        self.btn_cerrar_turno.config(state='disabled')

    def mostrar_usuarios(self):
        log.debug("Creando ventana para mostrar usuarios")
        # Crear ventana para mostrar los usuarios
        self.crear_ventana_mostrar_usuarios()
        self.configurar_grid_ventana_usuarios()
        self.crear_frames_mostrar_usuarios()
        self.mostrar_contenido_ventana_usuarios()

    # Ventana de usuarios ==============================================================================================
    """
    Funciones de configuración: Funciones que configuran la ventana y los elementos de la interfaz.
    Funciones de creación de elementos: Funciones que crean los diferentes elementos de la interfaz.
    Funciones de manejo de eventos: Funciones que manejan los eventos de los botones y otros elementos interactivos.
    Funciones de validación: Funciones que validan los datos ingresados por el usuario.
    Funciones de utilidad: Funciones auxiliares que no encajan en las otras categorías.
    """
    def crear_ventana_mostrar_usuarios(self):
        log.debug("Creando ventana de usuarios")
        self.ventana_usuarios = tk.Toplevel(self)
        self.ventana_usuarios.title('Usuarios')
        self.ventana_usuarios.geometry('800x300')
        self.ventana_usuarios.minsize(width=800, height=300)
        self.ventana_usuarios.resizable(width=False, height=False)
        centrar_ventana(self.ventana_usuarios, 800, 300)

    def configurar_grid_ventana_usuarios(self):
        log.debug("Configurando grid de la ventana de usuarios")
        self.frame_principal_usuarios = tk.Frame(self.ventana_usuarios)

        self.frame_principal_usuarios.columnconfigure(0, weight=0)
        self.frame_principal_usuarios.columnconfigure(1, weight=1)
        self.frame_principal_usuarios.columnconfigure(2, weight=1)

        self.frame_principal_usuarios.rowconfigure(0, weight=0)
        self.frame_principal_usuarios.rowconfigure(1, weight=1)

        self.frame_principal_usuarios.pack(fill='both', expand=True)

    def crear_frames_mostrar_usuarios(self):
        log.debug("Creando frames de la ventana de usuarios")
        # Frame para el filtro
        self.frame_usuarios_filtro = tk.Frame(self.frame_principal_usuarios, bg=COLOR_FONDO, bd=1, relief='raised')
        self.frame_usuarios_filtro.grid(row=0, column=0, sticky='nsew')

        # Frame para los botones
        self.frame_usuarios_botones = tk.Frame(self.frame_principal_usuarios, bg=COLOR_FONDO, bd=1, relief='raised')
        self.frame_usuarios_botones.grid(row=0, column=1, sticky='nsew', columnspan=2)

        # Frame para la tabla
        self.frame_usuarios_tabla = tk.Frame(self.frame_principal_usuarios, bg=COLOR_FONDO, bd=1, relief='raised')
        self.frame_usuarios_tabla.grid(row=1, column=0, sticky='nsew')

        # Frame para el formulario
        self.frame_usuarios_formulario = tk.Frame(self.frame_principal_usuarios, bg=COLOR_FONDO, bd=1, relief='raised')
        self.frame_usuarios_formulario.grid(row=1, column=1, sticky='nsew', columnspan=2)

    def mostrar_contenido_ventana_usuarios(self):
        log.debug("Mostrando contenido de la ventana de usuarios")
        self.mostrar_filtro_usuarios()
        self.mostrar_botones_usuarios()
        self.mostrar_tabla_usuarios()
        self.mostrar_formulario_usuarios()

    def mostrar_filtro_usuarios(self):
        log.debug("Mostrando filtro de usuarios")
        lbl_filtro = tk.Label(self.frame_usuarios_filtro,
                                text='Filtrar por tipo:',
                                bg=COLOR_FONDO,
                                fg='white')
        lbl_filtro.grid(row=0, column=0, padx=10, pady=10)

        filtros = ['Todos', 'Administrador', 'Cajero']

        self.combobox = ttk.Combobox(self.frame_usuarios_filtro, values=filtros)
        self.combobox.grid(row=0, column=1, padx=10, pady=10)

        # Seleccionamos un elemento por default a mostrar
        self.combobox.current(0)

        # Asociar el evento de selección al combobox
        self.combobox.bind("<<ComboboxSelected>>", self.filtrar_usuarios)

    def filtrar_usuarios(self, event):
        filtro = self.combobox.get()
        log.debug(f"Filtrando usuarios por tipo: {filtro}")

        # Limpiar la tabla
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)

        # Cargar los registros filtrados
        if filtro == 'Todos':
            usuarios = UsuarioDAO.seleccionar()
        else:
            usuarios = [usuario for usuario in UsuarioDAO.seleccionar() if usuario[5] == filtro]

        for usuario in usuarios:
            self.tabla_usuarios.insert(parent='', index=tk.END, values=(usuario[0], f'{usuario[1]} {usuario[2]}', usuario[5]))

    def mostrar_botones_usuarios(self):
        log.debug("Mostrando botones de usuarios")

        btn_nuevo = ttk.Button(self.frame_usuarios_botones,
                                text='Nuevo',
                                command=self.agregar_usuario)  # implementando funcion de agregar usuario
        btn_nuevo.grid(row=0, column=0, pady=10, padx=5)

        btn_guardar = ttk.Button(self.frame_usuarios_botones,
                                text='Guardar',
                                command=self.guardar_cambios_mostrar_usuario)  # implementando funcion de guardar usuario
        btn_guardar.grid(row=0, column=1, pady=10, padx=5)

        btn_deshacer = ttk.Button(self.frame_usuarios_botones,
                                text='Deshacer',
                                command=lambda: print('Deshacer'))
        btn_deshacer.grid(row=0, column=2, pady=10, padx=5)

        btn_editar = ttk.Button(self.frame_usuarios_botones,
                                text='Editar',
                                command=self.editar_usuario)  # implementando funcion de editar usuario
        btn_editar.grid(row=0, column=3, pady=10, padx=5)

        btn_buscar = ttk.Button(self.frame_usuarios_botones,
                                text='Buscar',
                                command=lambda: print('Buscar'))
        btn_buscar.grid(row=0, column=4, pady=10, padx=5)

        btn_eliminar = ttk.Button(self.frame_usuarios_botones,
                                text='Eliminar',
                                command=lambda: print('Eliminar'))
        btn_eliminar.grid(row=0, column=5, pady=10, padx=5)

    def agregar_usuario(self):
        log.debug("Agregando usuario")
        self.limpiar_formulario_usuarios()
        self.habilitar_todos_los_campos_formulario_usuarios()

        nuevo_id = UsuarioDAO.aumentar_id()
        self.txt_id_usuario.config(state='normal')
        self.txt_id_usuario.delete(0, tk.END)
        self.txt_id_usuario.insert(0, nuevo_id)
        self.txt_id_usuario.config(state='disabled')
        self.txt_nombre_usuario.focus()

    def editar_usuario(self):
        log.debug("Editando usuario")
        self.habilitar_todos_los_campos_formulario_usuarios()
        self.txt_id_usuario.config(state='disabled')

    def guardar_cambios_mostrar_usuario(self):
        log.debug("Guardando cambios en usuario")
        if not self.validar_todos_campos_formulario_usuarios():
            log.debug("Campos del formulario de usuarios no válidos")
            return

        id_usuario = int(self.txt_id_usuario.get())
        nombre_completo = self.txt_nombre_usuario.get()
        nombre = nombre_completo.split(' ')[0]
        apellido = nombre_completo.split(' ')[1] if len(nombre_completo.split(' ')) > 1 else nombre
        correo = self.txt_correo_usuario.get()
        rol = self.txt_rol_usuario.get() if self.txt_rol_usuario.get() == 'Administrador' else 'Cajero'
        telefono = self.txt_telefono_usuario.get()
        contrasena = self.txt_contrasenna_usuario.get()

        usuario_existente = UsuarioDAO.seleccionar_por_id(id_usuario=id_usuario)

        if usuario_existente:
            if contrasena:
                contrasena = encriptar_contrasena(contrasena)
                UsuarioDAO.actualizar(nombre, apellido, correo, contrasena, rol, telefono, id_usuario)
            else:
                UsuarioDAO.actualizar(nombre, apellido, correo, usuario_existente[4], rol, telefono, id_usuario)
            log.debug("Usuario actualizado con éxito")
            messagebox.showinfo("Éxito", "Usuario actualizado con éxito")
        else:
            if contrasena:
                contrasena = encriptar_contrasena(contrasena)
            nuevo_usuario = Usuario(id=id_usuario, nombre=nombre, apellido=apellido, correo=correo, contrasena=contrasena, rol=rol, telefono=telefono)
            UsuarioDAO.insertar(nuevo_usuario)
            log.debug("Nuevo usuario agregado")
            messagebox.showinfo("Éxito", "Nuevo usuario agregado con éxito")

        self.cerrar_y_reabrir_ventana_usuarios()

    def cerrar_y_reabrir_ventana_usuarios(self):
        log.debug("Cerrando y reabriendo ventana de usuarios")
        self.ventana_usuarios.destroy()
        self.mostrar_usuarios()

    def actualizar_datos_de_usuario(self):
        log.debug("Actualizando datos de usuario")

        # Antes de actualizar los datos verificamos si el usuario esta en la base de datos, en caso de que no este
        # se agrega un nuevo usuario
        registros = UsuarioDAO.seleccionar()
        for registro in registros:
            if registro[0] == int(self.txt_id_usuario.get()):
                nombre_completo = self.txt_nombre_usuario.get()
                nombre = nombre_completo.split(' ')[0]
                apellido = nombre_completo.split(' ')[1]
                correo = self.txt_correo_usuario.get()
                rol = self.txt_rol_usuario.get() if self.txt_rol_usuario.get() == 'Administrador' else 'Cajero'
                telefono = self.txt_telefono_usuario.get()
                id_usuario = int(self.txt_id_usuario.get())

                if self.txt_contrasenna_usuario.get():
                    contrasena = encriptar_contrasena(self.txt_contrasenna_usuario.get())
                    UsuarioDAO.actualizar_con_contrasena(nombre, apellido, correo, contrasena, rol, telefono, id_usuario)
                    log.debug("Usuario actualizado con contraseña")
                else:
                    UsuarioDAO.actualizar_sin_contrasena(nombre=nombre, apellido=apellido, correo=correo,
                                                            rol=rol, telefono=telefono, id_usuario=id_usuario)
                    log.debug("Usuario actualizado sin contraseña")
                return

        # Si el usuario no está en la base de datos, se agrega un nuevo usuario
        nombre_completo = self.txt_nombre_usuario.get()
        nombre = nombre_completo.split(' ')[0]
        apellido = nombre_completo.split(' ')[1]
        correo = self.txt_correo_usuario.get()
        contrasena = encriptar_contrasena(self.txt_contrasenna_usuario.get())
        rol = self.txt_rol_usuario.get() if self.txt_rol_usuario.get() == 'Administrador' else 'Cajero'
        telefono = self.txt_telefono_usuario.get()
        id_usuario = int(self.txt_id_usuario.get())

        nuevo_usuario = Usuario(id=id_usuario, nombre=nombre, apellido=apellido, correo=correo,
                                contrasena=contrasena, rol=rol, telefono=telefono)
        UsuarioDAO.insertar(nuevo_usuario)
        log.debug("Nuevo usuario agregado")

    def validar_todos_campos_formulario_usuarios(self):
        log.debug("Validando campos del formulario de usuarios")
        """
        Validar que los campos no estén vacíos
        """
        if not self.txt_nombre_usuario.get():
            messagebox.showwarning(title='Campo vacío', message='Por favor llene el campo de nombre')
            self.txt_nombre_usuario.focus()
            return False
        if not self.txt_correo_usuario.get():
            messagebox.showwarning(title='Campo vacío', message='Por favor llene el campo de correo')
            self.txt_correo_usuario.focus()
            return False
        if not self.txt_rol_usuario.get():
            messagebox.showwarning(title='Campo vacío', message='Por favor llene el campo de rol')
            self.txt_rol_usuario.focus()
            return False
        if not self.txt_telefono_usuario.get():
            messagebox.showwarning(title='Campo vacío', message='Por favor llene el campo de telefono')
            self.txt_telefono_usuario.focus()
            return False
        # if not self.txt_contrasenna_usuario.get():
        #     messagebox.showwarning(title='Campo vacío', message='Por favor llene el campo de contraseña')
        #     self.txt_contrasenna_usuario.focus()
        #     return False
        return True

    def mostrar_tabla_usuarios(self):
        log.debug("Mostrando tabla de usuarios")
        self.configurar_tabla()
        self.cargar_registros_en_tabla()

    def configurar_tabla(self):
        log.debug("Configurando tabla en ventana de usuarios")
        # Definir las columnas de la tabla
        columnas = ('ID', 'Nombre', 'Tipo')

        # Crear la tabla
        self.tabla_usuarios = ttk.Treeview(self.frame_usuarios_tabla, columns=columnas, show='headings')
        # Agregar los encabezados de la tabla
        self.tabla_usuarios.heading('ID', text='ID', anchor=tk.CENTER)
        self.tabla_usuarios.heading('Nombre', text='Nombre', anchor=tk.CENTER)
        self.tabla_usuarios.heading('Tipo', text='Tipo', anchor=tk.CENTER)
        # Definir las columnas de la tabla
        ancho_columna = 120
        self.tabla_usuarios.column('ID', width=10, anchor=tk.CENTER)
        self.tabla_usuarios.column('Nombre', width=ancho_columna, anchor=tk.CENTER)
        self.tabla_usuarios.column('Tipo', width=ancho_columna, anchor=tk.CENTER)
        # Agregamos barra de scroll
        scroll = ttk.Scrollbar(self.frame_usuarios_tabla, orient=tk.VERTICAL, command=self.tabla_usuarios.yview)
        scroll.grid(row=0, column=1, sticky='ns')
        self.tabla_usuarios.configure(yscrollcommand=scroll.set)
        self.tabla_usuarios.grid(row=0, column=0, sticky=tk.NSEW)

    def cargar_registros_en_tabla(self):
        log.debug("Cargando registros en tabla de usuarios")
        self.limpiar_registros_tabla_usuarios()
        # Caragamos los registros de la base de datos
        self.registro_usuarios = UsuarioDAO.seleccionar()
        for registro in self.registro_usuarios:
            self.tabla_usuarios.insert(parent='', index=tk.END, values=(registro[0], f'{registro[1]} {registro[2]}', registro[5]))

        # Asociar el evento SELECT a la tabla
        self.tabla_usuarios.bind('<<TreeviewSelect>>', self.cargar_registro_en_formulario)

    def limpiar_registros_tabla_usuarios(self):
        log.debug("Limpiando registros de la tabla de usuarios")
        for item in self.tabla_usuarios.get_children():
            self.tabla_usuarios.delete(item)

    def cargar_registro_en_formulario(self, event):
        log.debug("Cargando registro en formulario")
        self.limpiar_formulario_usuarios()

        # Obtener el id del registro seleccionado y cargar el nombre el formulario
        seleccion = self.tabla_usuarios.selection()
        if not seleccion:
            log.debug("No se ha seleccionado ningún registro")
            return

        id_cliente = self.tabla_usuarios.item(seleccion)['values'][0]
        self.id_cliente = id_cliente

        # Consultar los datos del usuario en la base de datos
        usuario = UsuarioDAO.seleccionar_por_id(id_usuario=self.id_cliente)
        if usuario:
            # Mostrar los datos en el formulario
            self.habilitar_todos_los_campos_formulario_usuarios()
            self.txt_id_usuario.delete(0, tk.END)
            self.txt_id_usuario.insert(0, usuario[0])

            self.txt_nombre_usuario.delete(0, tk.END)
            self.txt_nombre_usuario.insert(0, f'{usuario[1]} {usuario[2]}')

            self.txt_correo_usuario.delete(0, tk.END)
            self.txt_correo_usuario.insert(0, usuario[3])

            self.txt_rol_usuario.delete(0, tk.END)
            self.txt_rol_usuario.insert(0, usuario[5])

            self.txt_telefono_usuario.delete(0, tk.END)
            self.txt_telefono_usuario.insert(0, usuario[6])

            self.deshabilitar_todos_los_campos_formulario_usuarios()

    def habilitar_todos_los_campos_formulario_usuarios(self):
        log.debug("Habilitando todos los campos del formulario de usuarios")
        self.txt_id_usuario.config(state='normal')
        self.txt_nombre_usuario.config(state='normal')
        self.txt_correo_usuario.config(state='normal')
        self.txt_rol_usuario.config(state='normal')
        self.txt_telefono_usuario.config(state='normal')
        self.txt_contrasenna_usuario.config(state='normal')

    def deshabilitar_todos_los_campos_formulario_usuarios(self):
        log.debug("Deshabilitando todos los campos del formulario de usuarios")
        self.txt_id_usuario.config(state='disabled')
        self.txt_nombre_usuario.config(state='disabled')
        self.txt_correo_usuario.config(state='disabled')
        self.txt_rol_usuario.config(state='disabled')
        self.txt_telefono_usuario.config(state='disabled')
        self.txt_contrasenna_usuario.config(state='disabled')

    def limpiar_formulario_usuarios(self):
        log.debug("Limpiando formulario de usuarios")
        """
        Limpiar los campos del formulario
        """
        self.habilitar_todos_los_campos_formulario_usuarios()
        self.txt_id_usuario.delete(0, tk.END)
        self.txt_nombre_usuario.delete(0, tk.END)
        self.txt_correo_usuario.delete(0, tk.END)
        self.txt_rol_usuario.delete(0, tk.END)
        self.txt_telefono_usuario.delete(0, tk.END)
        self.txt_contrasenna_usuario.delete(0, tk.END)
        self.deshabilitar_todos_los_campos_formulario_usuarios()

    def mostrar_formulario_usuarios(self):
        log.debug("Mostrando formulario de usuarios")
        self.configurar_formulario_usuarios()
        self.labels_cajas_texto_formulario_usuarios()

    def configurar_formulario_usuarios(self):
        log.debug("Configurando formulario de usuarios")
        """
        Configurar los campos del formulario
        """
        self.frame_usuarios_formulario.columnconfigure(0, weight=0) # clave, nombre, correo, rol, telefono
        self.frame_usuarios_formulario.columnconfigure(1, weight=0) # campos de texto de los campos
        self.frame_usuarios_formulario.columnconfigure(2, weight=0) # lbl_contraseña
        self.frame_usuarios_formulario.columnconfigure(3, weight=0) # txt_contraseña

        self.frame_usuarios_formulario.rowconfigure(0, weight=0)  # clave, txt_campos, lbl_contraseña, contraseña
        self.frame_usuarios_formulario.rowconfigure(1, weight=0)  # nombre
        self.frame_usuarios_formulario.rowconfigure(2, weight=0)  # correo
        self.frame_usuarios_formulario.rowconfigure(3, weight=0)  # rol
        self.frame_usuarios_formulario.rowconfigure(4, weight=0)  # telefono

        self.frame_usuarios_formulario.grid(row=1, column=1, sticky='nsew')

    def labels_cajas_texto_formulario_usuarios(self):
        log.debug("Creando campos del formulario de usuarios")

        color_letra = 'white'

        pad = 5

        lbl_id = tk.Label(self.frame_usuarios_formulario,  # Frame donde se encuentra el label
                            text='ID',  # Texto del label                   # Color de fondo del label
                            fg=color_letra,
                            background=COLOR_FONDO)                     # Color de la letra del label
        lbl_id.grid(row=0, column=0, padx=pad, pady=pad)
        self.txt_id_usuario = ttk.Entry(self.frame_usuarios_formulario, state='disabled')
        self.txt_id_usuario.grid(row=0, column=1, padx=pad, pady=pad)

        lbl_nombre = tk.Label(self.frame_usuarios_formulario,  # Frame donde se encuentra el label
                            text='Nombre',  # Texto del label                   # Color de fondo del label
                            fg=color_letra,
                            background=COLOR_FONDO)                     # Color de la letra del label
        lbl_nombre.grid(row=1, column=0, padx=pad, pady=pad)
        self.txt_nombre_usuario = ttk.Entry(self.frame_usuarios_formulario)
        self.txt_nombre_usuario.grid(row=1, column=1, padx=pad, pady=pad)

        lbl_correo = tk.Label(self.frame_usuarios_formulario,  # Frame donde se encuentra el label
                            text='Correo',  # Texto del label                   # Color de fondo del label
                            fg=color_letra,
                            background=COLOR_FONDO)                     # Color de la letra del label
        lbl_correo.grid(row=2, column=0, padx=pad, pady=pad)
        self.txt_correo_usuario = ttk.Entry(self.frame_usuarios_formulario)
        self.txt_correo_usuario.grid(row=2, column=1, padx=pad, pady=pad)

        lbl_rol = tk.Label(self.frame_usuarios_formulario,  # Frame donde se encuentra el label
                            text='Rol',  # Texto del label                   # Color de fondo del label
                            fg=color_letra,
                            background=COLOR_FONDO)                     # Color de la letra del label
        lbl_rol.grid(row=3, column=0, padx=pad, pady=pad)
        self.txt_rol_usuario = ttk.Entry(self.frame_usuarios_formulario)
        self.txt_rol_usuario.grid(row=3, column=1, padx=pad, pady=pad)

        lbl_telefono = tk.Label(self.frame_usuarios_formulario,  # Frame donde se encuentra el label
                            text='Telefono',  # Texto del label                   # Color de fondo del label
                            fg=color_letra,
                            background=COLOR_FONDO)                     # Color de la letra del label
        lbl_telefono.grid(row=4, column=0, padx=pad, pady=pad)
        self.txt_telefono_usuario = ttk.Entry(self.frame_usuarios_formulario)
        self.txt_telefono_usuario.grid(row=4, column=1, padx=pad, pady=pad)

        lbl_contraseña = tk.Label(self.frame_usuarios_formulario,  # Frame donde se encuentra el label
                            text='Contraseña',  # Texto del label                   # Color de fondo del label
                            fg=color_letra,
                            background=COLOR_FONDO)                     # Color de la letra del label
        lbl_contraseña.grid(row=0, column=3, padx=pad, pady=pad)
        self.txt_contrasenna_usuario = ttk.Entry(self.frame_usuarios_formulario)
        self.txt_contrasenna_usuario.grid(row=0, column=4, padx=pad, pady=pad)

    # Fin de la clase VentanaPrincipal /////////////////////////////////////////////////////////////////////////////////



if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()