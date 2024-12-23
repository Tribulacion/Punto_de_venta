"""
Definición de las ventanas de la aplicación
"""
import tkinter as tk
from tkinter import ttk, messagebox
from app.modelos import UsuarioDAO, encriptar_contrasena
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

    # Falta implementar la funcion del filtro********************************************************************************
    def mostrar_filtro_usuarios(self):
        log.debug("Mostrando filtro de usuarios")
        lbl_filtro = tk.Label(self.frame_usuarios_filtro,
                                text='Filtrar por tipo:',
                                bg=COLOR_FONDO,
                                fg='white')
        lbl_filtro.grid(row=0, column=0, padx=10, pady=10)

        filtros = ['Todos', 'Administrador', 'Usuario']

        combobox = ttk.Combobox(self.frame_usuarios_filtro, values=filtros)
        combobox.grid(row=0, column=1, padx=10, pady=10)

        # Seleccionamos un elemento por default a mostrar
        combobox.current(0)

        # Aqui se puede agregar la funcion para que al seleccionar un elemento se filtre la tabla sin necesidad de un boton****************

    # Falta implementar la funcion de los usuarios********************************************************************************
    def mostrar_botones_usuarios(self):
        log.debug("Mostrando botones de usuarios")

        btn_nuevo = ttk.Button(self.frame_usuarios_botones,
                                text='Nuevo',
                                command=lambda: print('Nuevo'))
        btn_nuevo.grid(row=0, column=0, pady=10, padx=5)

        btn_guardar = ttk.Button(self.frame_usuarios_botones,
                                text='Guardar',
                                command=lambda: print('Guardar'))
        btn_guardar.grid(row=0, column=1, pady=10, padx=5)

        btn_deshacer = ttk.Button(self.frame_usuarios_botones,
                                text='Deshacer',
                                command=lambda: print('Deshacer'))
        btn_deshacer.grid(row=0, column=2, pady=10, padx=5)

        btn_editar = ttk.Button(self.frame_usuarios_botones,
                                text='Editar',
                                command=lambda: print('Editar'))
        btn_editar.grid(row=0, column=3, pady=10, padx=5)

        btn_buscar = ttk.Button(self.frame_usuarios_botones,
                                text='Buscar',
                                command=lambda: print('Buscar'))
        btn_buscar.grid(row=0, column=4, pady=10, padx=5)

        btn_eliminar = ttk.Button(self.frame_usuarios_botones,
                                text='Eliminar',
                                command=lambda: print('Eliminar'))
        btn_eliminar.grid(row=0, column=5, pady=10, padx=5)

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
        # Caragamos los registros de la base de datos
        self.registro_usuarios = UsuarioDAO.seleccionar()
        for registro in self.registro_usuarios:
            self.tabla_usuarios.insert(parent='', index=tk.END, values=(registro[0], f'{registro[1]} {registro[2]}', registro[5]))

        # Asociar el evento SELECT a la tabla
        self.tabla_usuarios.bind('<<TreeviewSelect>>', self.cargar_registro_en_formulario)

    def cargar_registro_en_formulario(self, event):
        log.debug("Cargando registro en formulario")
        """
        Cargar los datos del registro en el formulario
        """
        self.limpiar_formulario_usuarios()

        # Obtener el id del registro seleccionado y cargar el nombre el formulario
        seleccion = self.tabla_usuarios.selection()
        if seleccion:
            item = self.tabla_usuarios.item(seleccion[0])
            valores = item['values']
            if valores:
                self.id_cliente = valores[0]

                # Consultar los datos del usuario en la base de datos
                usuario = UsuarioDAO.seleccionar_por_id(self.id_cliente)
                if usuario:
                    # Tupla: (id[0], nombre[1], apellido[2], correo[3], contraseña[4], rol[5], telefono[6])

                    # Mostrar los datos en el formulario
                    self.habilitar_todos_los_campos_formulario_usuarios()
                    self.txt_id_usuario.insert(0, usuario[0])  # Accessing tuple elements directly
                    self.nombre_usuario.insert(0, f'{usuario[1]} {usuario[2]}')
                    self.correo_usuario.insert(0, usuario[3])
                    self.rol_usuario.insert(0, usuario[5])
                    self.telefono_usuario.insert(0, usuario[6])
                    # self.contraseña_usuario.insert(0, usuario[4])
                    self.deshabilitar_todos_los_campos_formulario_usuarios()

    def habilitar_todos_los_campos_formulario_usuarios(self):
        log.debug("Habilitando todos los campos del formulario de usuarios")
        self.txt_id_usuario.config(state='normal')
        self.nombre_usuario.config(state='normal')
        self.correo_usuario.config(state='normal')
        self.rol_usuario.config(state='normal')
        self.telefono_usuario.config(state='normal')
        self.contraseña_usuario.config(state='normal')

    def deshabilitar_todos_los_campos_formulario_usuarios(self):
        log.debug("Deshabilitando todos los campos del formulario de usuarios")
        self.txt_id_usuario.config(state='disabled')
        self.nombre_usuario.config(state='disabled')
        self.correo_usuario.config(state='disabled')
        self.rol_usuario.config(state='disabled')
        self.telefono_usuario.config(state='disabled')
        self.contraseña_usuario.config(state='disabled')

    def limpiar_formulario_usuarios(self):
        log.debug("Limpiando formulario de usuarios")
        """
        Limpiar los campos del formulario
        """
        self.habilitar_todos_los_campos_formulario_usuarios()
        self.txt_id_usuario.delete(0, tk.END)
        self.nombre_usuario.delete(0, tk.END)
        self.correo_usuario.delete(0, tk.END)
        self.rol_usuario.delete(0, tk.END)
        self.telefono_usuario.delete(0, tk.END)
        self.contraseña_usuario.delete(0, tk.END)
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
        self.nombre_usuario = ttk.Entry(self.frame_usuarios_formulario)
        self.nombre_usuario.grid(row=1, column=1, padx=pad, pady=pad)

        lbl_correo = tk.Label(self.frame_usuarios_formulario,  # Frame donde se encuentra el label
                            text='Correo',  # Texto del label                   # Color de fondo del label
                            fg=color_letra,
                            background=COLOR_FONDO)                     # Color de la letra del label
        lbl_correo.grid(row=2, column=0, padx=pad, pady=pad)
        self.correo_usuario = ttk.Entry(self.frame_usuarios_formulario)
        self.correo_usuario.grid(row=2, column=1, padx=pad, pady=pad)

        lbl_rol = tk.Label(self.frame_usuarios_formulario,  # Frame donde se encuentra el label
                            text='Rol',  # Texto del label                   # Color de fondo del label
                            fg=color_letra,
                            background=COLOR_FONDO)                     # Color de la letra del label
        lbl_rol.grid(row=3, column=0, padx=pad, pady=pad)
        self.rol_usuario = ttk.Entry(self.frame_usuarios_formulario)
        self.rol_usuario.grid(row=3, column=1, padx=pad, pady=pad)

        lbl_telefono = tk.Label(self.frame_usuarios_formulario,  # Frame donde se encuentra el label
                            text='Telefono',  # Texto del label                   # Color de fondo del label
                            fg=color_letra,
                            background=COLOR_FONDO)                     # Color de la letra del label
        lbl_telefono.grid(row=4, column=0, padx=pad, pady=pad)
        self.telefono_usuario = ttk.Entry(self.frame_usuarios_formulario)
        self.telefono_usuario.grid(row=4, column=1, padx=pad, pady=pad)

        lbl_contraseña = tk.Label(self.frame_usuarios_formulario,  # Frame donde se encuentra el label
                            text='Contraseña',  # Texto del label                   # Color de fondo del label
                            fg=color_letra,
                            background=COLOR_FONDO)                     # Color de la letra del label
        lbl_contraseña.grid(row=0, column=3, padx=pad, pady=pad)
        self.contraseña_usuario = ttk.Entry(self.frame_usuarios_formulario)
        self.contraseña_usuario.grid(row=0, column=4, padx=pad, pady=pad)

    # Fin de la clase VentanaPrincipal /////////////////////////////////////////////////////////////////////////////////



if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()