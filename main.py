import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


class Finanzas(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.overrideredirect(True)
        # Adding a title to the window
        altura = 400
        anchura = 600
        altura_pantalla = self.winfo_screenheight()
        anchura_pantalla = self.winfo_screenwidth()
        x = (anchura_pantalla // 2) - (anchura//2)
        y = (altura_pantalla//2) - (altura//2)
        self.geometry(f"+{x}+{y}")
        
        self.conn = sqlite3.connect('finanzas.db')
        
        #root.overrideredirect(1)
        self.ingreso_var = tk.DoubleVar()
        self.ingreso_txt = tk.StringVar()
        self.egreso_var = tk.DoubleVar()
        self.egreso_txt = tk.StringVar()
        self.saldo_var = tk.DoubleVar()
        self.saldo_txt = tk.StringVar()
        # Crear tabla si no existe
        self.crear_tabla_finanzas()
        self.crear_tabla_usuario()
        self.ventana_login()
        self.barra_titulo()

    def barra_titulo(self):
        self.barra = tk.Frame(self, width=600, height=30, bg="gray19")
        self.barra.place(x=0, y=0)
        self.boton_cerrar = tk.Button(self.barra, command=self.destroy, text="x", bg="gray25")
        self.boton_cerrar.place(x=550, y=0, width=50, height=30)
        self.boton_usuario = tk.Button(self.barra, command=self.agregar_usuario, text="?", bg="gray25")
        self.boton_usuario.place(x=0, y=0, width=50, height=30)

    def ventana_login(self):
        # Frame de inicio de sesión
        self.login_frame = tk.Frame(self, width=300, height=200, bg="gray18")
        self.lbl_titulo_login = tk.Label(self.login_frame, text="INICIO DE SESION", bg="gray18", fg="white", font=("Arial",16))
        self.lbl_titulo_login.place(x=30, y=20, width=240)
        self.lbl_user = tk.Label(self.login_frame, text="Usuario:", bg="gray18", fg="white")
        self.lbl_user.place(x=30, y=50)
        self.entry_usuario = tk.Entry(self.login_frame, bg="gray18", fg="white")
        self.entry_usuario.place(x = 30, y=70, width=240)

        self.lbl_pass = tk.Label(self.login_frame, text="Contraseña:", bg="gray18", fg="white")
        self.lbl_pass.place(x = 30, y = 100)
        self.entry_contrasena = tk.Entry(self.login_frame, show="*", bg="gray18", fg="white")
        self.entry_contrasena.place(x = 30, y=120, width=240)

        self.btn_iniciar_sesion = tk.Button(self.login_frame, text="Iniciar Sesión", command=self.iniciar_sesion, bg="gray18", fg="white")
        self.btn_iniciar_sesion.place(x = 30, y = 150, width=240)

        # agregar_usuario
        self.login_frame.place(x=150, y=110)

        # Frame principal
        

    def quitar_login(self):
        self.login_frame.forget()
        self.boton_usuario.forget()

# Funciones de la base de datos
    def crear_tabla_usuario(self):
        self.conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS USUARIOS
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            USUARIO TEXT NOT NULL,
            CONTRASENIA TEXT NOT NULL,
            NOMBRE TEXT NOT NULL);
            '''
        )
        self.conn.commit()

    def agregar_usuario(self):
        if (self.verificar_credenciales('admin', 'admin') == 1):
            messagebox.showerror("Usuario existente", "Usuario administrador ya está registrado")
        else:
            self.conn.execute('''
            INSERT INTO USUARIOS (USUARIO, CONTRASENIA, NOMBRE)
            VALUES (?, ?, ?);
            ''', ('admin', 'admin', 'Administrador'))
            self.conn.commit()
            messagebox.showinfo("Exito!","Usuario Administrador creado con exito.")

    def verificar_credenciales(self,usuario, contrasena):
        query = '''
            SELECT COUNT(*) FROM USUARIOS
            WHERE USUARIO = ? AND CONTRASENIA = ?;
        '''
        resultado = self.conn.execute(query, (usuario, contrasena)).fetchone()[0]
        return resultado == 1

    def crear_tabla_finanzas(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS FINANZAS
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE TEXT NOT NULL,
            MONTO REAL NOT NULL,
            TIPO TEXT NOT NULL);
        ''')
        self.conn.commit()

    def agregar_transaccion(self, nombre, monto, tipo):
        self.conn.execute('''
            INSERT INTO FINANZAS (NOMBRE, MONTO, TIPO)
            VALUES (?, ?, ?);
        ''', (nombre, monto, tipo))
        self.conn.commit()



    def obtener_resumen(self):
        ingresos = self.conn.execute('SELECT SUM(MONTO) FROM FINANZAS WHERE TIPO="Ingreso";').fetchone()[0] or 0
        egresos = self.conn.execute('SELECT SUM(MONTO) FROM FINANZAS WHERE TIPO="Egreso";').fetchone()[0] or 0
        saldo = ingresos - egresos
        self.ingreso_var.set(ingresos)
        self.ingreso_txt.set(f"{self.ingreso_var.get():,.2f}")
        self.egreso_var.set(egresos)
        self.egreso_txt.set(f"{self.egreso_var.get():,.2f}")
        saldo = self.ingreso_var.get() - self.egreso_var.get()
        self.saldo_var.set(saldo)
        self.saldo_txt.set(f"{self.saldo_var.get():,.2f}")
        return f"Ingresos: {self.ingreso_txt.get()}\nEgresos: {self.egreso_txt.get()}\nSaldo: {self.saldo_txt.get()}"

    def limpiar_inputs(self):
        self.entry_nombre.set("")
        self.entry_monto.set("")


    def agregar_texto_transaccion(self):
        nombre_e = self.entry_nombre.get().lower()
        monto_e = self.entry_monto.get()
        tipo_e = self.var_tipo.get()
        print(f"Datos= nombre: {nombre_e} monto: {monto_e} tipo: {tipo_e}")
        if nombre_e and monto_e and tipo_e:
            self.agregar_transaccion(nombre_e, monto_e, tipo_e)
            messagebox.showinfo("Éxito", "Transacción agregada correctamente")
            self.actualizar_resumen()
            self.limpiar_inputs()
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos")

    def actualizar_resumen(self):
        self.resumen_text.config(state=tk.NORMAL)
        self.resumen_text.delete(1.0, tk.END)
        self.resumen_text.insert(tk.END, self.obtener_resumen())
        self.resumen_text.config(state=tk.DISABLED)

    
    def ventana_principal_abrir(self):
        
        self.ventana_principal = tk.Frame(root, width=600, height=390, bg="gray18")
        self.ventana_principal.place(x=0, y=30)

        # Variables
        self.var_tipo = tk.StringVar()

        # Formulario de transacciones


        fr_ingresos = tk.Frame(self.ventana_principal, width=180, height=70, bg="SpringGreen3")
        fr_ingresos.place(x=20, y=20)

        lbl_ingresos = tk.Label(self.ventana_principal, text="Ingresos", bg="SpringGreen3", fg="White")
        lbl_ingresos.place(x=30, y=30)

        txt_ingresos = tk.Label(self.ventana_principal, textvariable=self.ingreso_txt, bg="SpringGreen3", font=("Arial",14), fg="White")
        txt_ingresos.place(x=30, y=50)

        fr_egresos = tk.Frame(self.ventana_principal, width=180, height=70, bg="red4")
        fr_egresos.place(x=210, y=20)

        lbl_egresos = tk.Label(self.ventana_principal, text="Egresos", bg="red4", fg="White")
        lbl_egresos.place(x=220, y=30)

        txt_egresos = tk.Label(self.ventana_principal, textvariable=self.egreso_txt, bg="red4", font=("Arial",14), fg="White")
        txt_egresos.place(x=220, y=50)

        fr_saldo = tk.Frame(self.ventana_principal, width=180, height=70, bg="RoyalBlue4")
        fr_saldo.place(x=400, y=20)

        lbl_saldo = tk.Label(self.ventana_principal, text="Saldo", bg="RoyalBlue4", fg="White")
        lbl_saldo.place(x=410, y=30)

        txt_saldo = tk.Label(self.ventana_principal, textvariable=self.saldo_txt, bg="RoyalBlue4", font=("Arial",14), fg="White")
        txt_saldo.place(x=410, y=50)

        # Formulario de transacciones
        lbl_nombre = tk.Label(self.ventana_principal, text="Descripción:", bg="gray18", fg="white")
        lbl_nombre.place(x=20, y=110)
        self.entry_nombre = tk.Entry(self.ventana_principal)
        self.entry_nombre.place(x=100, y=110, width=480)

        lbl_monto = tk.Label(self.ventana_principal, text="Monto:", bg="gray18", fg="white")
        lbl_monto.place(x=20, y=135)
        self.entry_monto = tk.Entry(self.ventana_principal)
        self.entry_monto.place(x=100, y=135, width=480)

        lbl_tipo = tk.Label(self.ventana_principal, text="Tipo:", bg="gray18", fg="white")
        lbl_tipo.place(x=20, y=160)
        
        self.combo_tipo = ttk.Combobox(self.ventana_principal, textvariable=self.var_tipo)
        self.combo_tipo['values'] =  ("Ingreso", "Egreso")
        self.combo_tipo.place(x=100, y=160, width=480)

        btn_agregar_transaccion = tk.Button(self.ventana_principal, text="Agregar Transacción", command=self.agregar_texto_transaccion, bg="gray18", fg="white")
        btn_agregar_transaccion.place(x=20, y = 210, width=560)

        # Resumen financiero
        lbl_resumen = tk.Label(self.ventana_principal, text="Resumen Financiero:", bg="gray18", fg="white")
        lbl_resumen.place(x=20, y=240)
        self.resumen_text = tk.Text(self.ventana_principal, bg="gray18", fg="white")
        self.resumen_text.place(x=20, y=270, height=55, width=560)
        
        # Botón de cerrar sesión
        btn_cerrar_sesion = tk.Button(self.ventana_principal, text="Cerrar Sesión", command=self.cerrar_sesion, bg="gray18", fg="white")
        btn_cerrar_sesion.place(x=20, y=350, width=560)

        self.actualizar_resumen()

# Funciones de la interfaz gráfica
    def iniciar_sesion(self):
        usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        if self.verificar_credenciales(usuario, contrasena):
            self.quitar_login()
            self.ventana_principal_abrir()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")


    def cerrar_sesion(self):
        self.quit()
    

if __name__ == '__main__':
    root = Finanzas()
    root.geometry('600x420')
    root.mainloop()
