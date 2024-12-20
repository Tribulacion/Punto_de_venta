"""
Definición de las ventanas de la aplicación
"""
import tkinter as tk
from tkinter import ttk, messagebox
from app.modelos import UsuarioDAO
from logger_base import log
import modelos

def centrar_ventana(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    log.debug(f"Ventana centrada en x={x}, y={y}")

class App(tk.Tk):
    # Variables globales ===============================================================================================
    COLOR_FONDO = '#1F446E'
    COLOR_PRUEBA = '#AA870C'
    ANCHO = 500
    ALTO = 400

    # Constructor ======================================================================================================
    def __init__(self):
        log.debug("Iniciando aplicación")
        super().__init__()
        self.id_cliente = None
        self.configurar_ventana()
        self.configurar_grid()
        self.crear_widgets()

        log.debug("Aplicación iniciada exitosamente")

    # Estilos ==========================================================================================================

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
        pass

    def mostrar_titulo(self):
        log.debug("Mostrando título")
        frame_titulo = tk.Frame(self, bg=self.COLOR_FONDO)

        lbl_titulo = tk.Label(frame_titulo,
                                text='Login',
                                bg=self.COLOR_PRUEBA,  # Cambiar a COLOR_FONDO
                                fg='white',
                                font=('Arial', 20),
                                padx=10,
                                pady=10,
                                anchor=tk.CENTER)
        lbl_titulo.pack(expand=True, fill='both')

        frame_titulo.grid(row=0, column=0, columnspan=2, sticky='nsew')

    def mostrar_tabla(self):
        log.debug("Mostrando tabla")
        # Crear un frame para la tabla
        frame_tabla = tk.Frame(self,
                               bg=self.COLOR_PRUEBA,  # Cambiar a COLOR_FONDO
                               relief='raised',  # Eliminar linea despues de las pruebas
                               bd=1
                               )
        frame_tabla.columnconfigure(0, weight=1)
        frame_tabla.grid(row=1, column=0, sticky='nsew')
        pass

    def mostrar_formulario(self):
        log.debug("Mostrando formulario")
        pass

    def mostrar_botones(self):
        log.debug("Mostrando botones")
        pass

    # Eventos ==========================================================================================================
    def _salir(self):
        log.debug("Saliendo de la aplicación")
        self.quit()
        log.debug("Aplicación finalizada exitosamente")

    def _login(self, event=None):
        log.debug("Iniciando login")
        usuario = self.usuario.get()
        password = self.password.get()

        usuario_db = UsuarioDAO.buscar_por_nombre(usuario)
        if usuario_db and usuario_db['contrasena'] == hashlib.sha256(password.encode()).hexdigest():
            messagebox.showinfo("Login", "Login exitoso")
            log.info("Login exitoso")
        else:
            messagebox.showerror("Login", "Usuario o contraseña incorrectos")
            log.error("Usuario o contraseña incorrectos")

        self.usuario.set("")
        self.password.set("")
        self.txt_usuario.focus()
        log.debug("Login finalizado")

    def cargar_registro(self, event):
        log.debug("Cargando registro")
        item = self.tabla.selection()
        nombre = self.tabla.item(item, 'values')
        self.nombre.set(nombre[0])
        log.debug("Registro cargado")

    # a

if __name__ == "__main__":
    app = App()
    app.mainloop()