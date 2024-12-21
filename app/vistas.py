"""
Definición de las ventanas de la aplicación
"""
import tkinter as tk
from tkinter import ttk, messagebox
from app.modelos import UsuarioDAO, encriptar_contrasena
from logger_base import log


def centrar_ventana(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    log.debug(f"Ventana centrada en x={x}, y={y}")


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
        log.debug("Iniciando aplicación")
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
                    log.debug("Login finalizado")
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

    # a

if __name__ == "__main__":
    app = App()
    app.mainloop()