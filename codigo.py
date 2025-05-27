import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import os, tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import math

# Paleta de colores
PRIMARY    = '#2E4053'
SECONDARY  = '#85C1E9'
ACCENT     = '#F7DC6F'
LIGHT_BLUE = '#D6EAF8'

class CatapultApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Catapulta – Miniproyecto 2")
        self.configure(bg=SECONDARY)
        self.minsize(800, 500)

        # Cargar iconos desde carpeta icons/
        self.load_icons()

        # Configurar estilos ttk
        self.setup_styles()

        # Construir la interfaz
        self.create_widgets()

    def load_icons(self):
        """Carga iconos solo si existen; si no, deja el atributo en None."""
        base = os.path.dirname(__file__)
        ico_folder = os.path.join(base, 'icons')

        def try_load(name):
            path = os.path.join(ico_folder, name)
            if os.path.exists(path):
                try:
                    return tk.PhotoImage(file=path)
                except tk.TclError:
                    return None
            return None

        self.icon_attack = try_load('attack.png')
        self.icon_length = try_load('length.png')
        self.icon_calc   = try_load('calc.png')
        self.icon_clear  = try_load('clear.png')

    def setup_styles(self):
        """Define temas y estilos para ttk, con paleta y fuente moderna."""
        style = ttk.Style(self)
        style.theme_use('clam')

        # Colores
        LIGHT_BLUE = '#D6EAF8'

        # Título principal
        style.configure('Header.TLabel',
                        background=SECONDARY,
                        foreground=PRIMARY,
                        font=('Segoe UI', 16, 'bold'))

        # Secciones (LabelFrame)
        style.configure('Section.TLabelframe',
                        background=LIGHT_BLUE,
                        borderwidth=1,
                        relief='solid')
        style.configure('Section.TLabelframe.Label',
                        background=LIGHT_BLUE,
                        foreground=PRIMARY,
                        font=('Segoe UI', 12, 'bold'))

        # Etiquetas y entradas
        style.configure('TLabel',
                        background=SECONDARY,
                        foreground=PRIMARY,
                        font=('Segoe UI', 11))
        style.configure('TEntry',
                        fieldbackground='white',
                        foreground=PRIMARY)

        # Botones de acento
        style.configure('Accent.TButton',
                        background=ACCENT,
                        foreground=PRIMARY,
                        font=('Segoe UI', 10, 'bold'),
                        padding=6)
        style.map('Accent.TButton',
                  background=[('active', PRIMARY), ('pressed', SECONDARY)],
                  foreground=[('active', 'white')])

        # Frames genéricos para que hereden el fondo
        style.configure('TFrame', background=SECONDARY)
    def create_rounded_rect(self, canvas, x1, y1, x2, y2, r, fill, outline):
        """Dibuja un rectángulo con esquinas redondeadas y sombra redondeada."""
        shadow_offset = 3
        shadow_color  = '#AAAAAA'

        # — Sombra redondeada —
        # Esquinas de la sombra
        canvas.create_arc(x1+shadow_offset,         y1+shadow_offset,
                          x1+2*r+shadow_offset,    y1+2*r+shadow_offset,
                          start= 90, extent= 90, style='pieslice',
                          fill=shadow_color, outline='')
        canvas.create_arc(x2-2*r+shadow_offset,     y1+shadow_offset,
                          x2+shadow_offset,         y1+2*r+shadow_offset,
                          start=  0, extent= 90, style='pieslice',
                          fill=shadow_color, outline='')
        canvas.create_arc(x2-2*r+shadow_offset,     y2-2*r+shadow_offset,
                          x2+shadow_offset,         y2+shadow_offset,
                          start=270, extent= 90, style='pieslice',
                          fill=shadow_color, outline='')
        canvas.create_arc(x1+shadow_offset,         y2-2*r+shadow_offset,
                          x1+2*r+shadow_offset,    y2+shadow_offset,
                          start=180, extent= 90, style='pieslice',
                          fill=shadow_color, outline='')
        # Centros de la sombra
        canvas.create_rectangle(x1+r+shadow_offset, y1+shadow_offset,
                                x2-r+shadow_offset, y2+shadow_offset,
                                fill=shadow_color, outline='')
        canvas.create_rectangle(x1+shadow_offset,    y1+r+shadow_offset,
                                x2+shadow_offset,    y2-r+shadow_offset,
                                fill=shadow_color, outline='')

        # — Rectángulo principal redondeado —
        # Esquinas
        canvas.create_arc(x1,         y1,         x1+2*r, y1+2*r,
                          start= 90, extent= 90, style='pieslice',
                          fill=fill, outline=outline)
        canvas.create_arc(x2-2*r,     y1,         x2,     y1+2*r,
                          start=  0, extent= 90, style='pieslice',
                          fill=fill, outline=outline)
        canvas.create_arc(x2-2*r,     y2-2*r,     x2,     y2,
                          start=270, extent= 90, style='pieslice',
                          fill=fill, outline=outline)
        canvas.create_arc(x1,         y2-2*r,     x1+2*r, y2,
                          start=180, extent= 90, style='pieslice',
                          fill=fill, outline=outline)
        # Centros
        canvas.create_rectangle(x1+r, y1,     x2-r, y2,
                                fill=fill, outline=outline)
        canvas.create_rectangle(x1,   y1+r,   x2,   y2-r,
                                fill=fill, outline=outline)


    def create_widgets(self):
        attack_options = ["120", "130", "140", "150", "160", "170", "180", "190", "200"]
        L1_options = ["83"]
        L2_options = ["230"]
        
        """Interfaz con secciones en Canvas: esquinas redondas, sin bordes grises."""
        LIGHT_BLUE      = '#D6EAF8'
        SEC_W           = 270
        GEO_H, KIN_H = 130, 370
        PAD_X, PAD_Y    = 20, 10
        OFFSET_Y        = 40
        SPACING_Y       = 25
        ENTRY_X_GEO     = 200
        ENTRY_X_KIN     = 220

        # — Título —
        lbl_title = ttk.Label(self, text="Mecanismo de Catapulta", style='Header.TLabel')
        lbl_title.grid(row=0, column=0, columnspan=2, pady=(20,10))

        # ========== Sección Geométrica ==========
        c_geo = tk.Canvas(self, width=SEC_W, height=GEO_H, bg=SECONDARY, highlightthickness=0)
        c_geo.grid(row=1, column=0, padx=PAD_X, pady=PAD_Y, sticky='nw')
        self.create_rounded_rect(c_geo, 0, 0, SEC_W-1, GEO_H-1, r=20, fill=LIGHT_BLUE, outline='')
        c_geo.create_text(15, 15, text="Parámetros Geométricos", anchor='nw', fill=PRIMARY,
                          font=('Segoe UI', 12, 'bold'))

        geom_labels = ["Altura de entrada (mm):", "Longitud L₁ (mm):", "Longitud L₂ (mm):"]
        geom_tips   = [
            "Altura desde la que se liberará la caja en la corredera.",
            "Longitud del primer eslabón desde el punto fijo hasta la primera unión.",
            "Longitud del segundo eslabón, conectando la unión al acoplador."
        ]
        for i, txt in enumerate(geom_labels):
            y = OFFSET_Y + i * SPACING_Y
            # Etiqueta y entrada
            lbl = tk.Label(self, text=txt, bg=LIGHT_BLUE, fg=PRIMARY, font=('Segoe UI', 10))
            c_geo.create_window((15, y), window=lbl, anchor='nw')
            if i == 0:
                cb = ttk.Combobox(c_geo, width=5, values=attack_options, state="readonly")
                self.entry_attack = cb
            elif i == 1:
                cb = ttk.Combobox(c_geo, width=5, values=L1_options, state="readonly")
                self.entry_L1 = cb
            else:
                cb = ttk.Combobox(c_geo, width=5, values=L2_options, state="readonly")
                self.entry_L2 = cb

            cb.current(0)  # Selecciona la primera opción por defecto
            c_geo.create_window((ENTRY_X_GEO, y), window=cb, anchor='nw')

            # Ícono “i” como Canvas widget
            #info_w = tk.Canvas(c_geo, width=16, height=16, bg=LIGHT_BLUE, highlightthickness=0, bd=0)
            #info_w.create_oval(0, 0, 16, 16, fill="#1976d2", outline="")
            #info_w.create_text(8, 8, text="i", fill="white", font=("Segoe UI", 8, "bold"))
            #c_geo.create_window((ENTRY_X_GEO - 30, y), window=info_w, anchor='nw')
            #Tooltip(info_w, geom_tips[i])

        # ========== Sección Cinemática (actualizada con subapartados) ==========
        c_kin = tk.Canvas(self, width=SEC_W, height=KIN_H, bg=SECONDARY, highlightthickness=0)
        c_kin.grid(row=2, column=0, padx=PAD_X, pady=PAD_Y, sticky='nw')
        self.create_rounded_rect(c_kin, 0, 0, SEC_W-1, KIN_H-1, r=20, fill=LIGHT_BLUE, outline='')
        c_kin.create_text(15, 15, text="Parámetros Cinématicos", anchor='nw', fill=PRIMARY,
                          font=('Segoe UI', 12, 'bold'))

        self.kin_entries_dict = {}

        # Subapartados: título + campos
        sections = [
            ("Eslabón 1:", [
                ("Velocidad angular ω₁ (rad/s):", "Velocidad angular del eslabón 1 en radianes por segundo."),
                ("Aceleración angular α₁ (rad/s²):", "Aceleración angular del eslabón 1 en rad/s²."),
                ["Ángulo de entrada θ₂ (°):", "Ángulo inicial del eslabón de entrada medido desde la horizontal."]
            ]),
            ("Eslabón 2:", [
                ("Velocidad angular ω₂ (rad/s):", "Velocidad angular del eslabón 2 en radianes por segundo."),
                ("Aceleración angular α₂ (rad/s²):", "Aceleración angular del eslabón 2 en rad/s².")
            ]),
            ("Puntos A, B y D:", [
                ("Velocidad vA (mm/s):", "Velocidad lineal en el punto A."),
                ("Aceleración aA (mm/s²):", "Aceleración lineal en el punto A."),
                ("Velocidad vB (mm/s):", "Velocidad lineal en el punto B."),
                ("Aceleración aB (mm/s²):", "Aceleración lineal en el punto B."),
                ("Velocidad vD (mm/s):", "Velocidad lineal en el punto D."),
                ("Aceleración aD (mm/s²):", "Aceleración lineal en el punto D.")
]           ),
        ]

        y_offset = OFFSET_Y

        for section_title, fields in sections:
            # Subapartado (con más espacio arriba)
            c_kin.create_text(15, y_offset, text=section_title, anchor='nw',
                              fill=PRIMARY, font=('Segoe UI', 10, 'bold'))
            y_offset += SPACING_Y - 10  # Espacio después del título

            for label, tip in fields:
                lbl = tk.Label(self, text=label, bg=LIGHT_BLUE, fg=PRIMARY, font=('Segoe UI', 10))
                c_kin.create_window((15, y_offset), window=lbl, anchor='nw')

                ent = ttk.Entry(c_kin, width=5)
                c_kin.create_window((ENTRY_X_KIN, y_offset), window=ent, anchor='nw')
                clave = label.split(":")[0].strip().replace(" ", "_").lower()
                self.kin_entries_dict[clave] = ent
                ent.configure(state="readonly")  # Para que no se puedan editar

                #info_w = tk.Canvas(c_kin, width=16, height=16, bg=LIGHT_BLUE, highlightthickness=0, bd=0)
                #info_w.create_oval(0, 0, 16, 16, fill="#1976d2", outline="")
                #info_w.create_text(8, 8, text="i", fill="white", font=("Segoe UI", 8, "bold"))
                #c_kin.create_window((ENTRY_X_KIN - 30, y_offset), window=info_w, anchor='nw')
                #Tooltip(info_w, tip)

                y_offset += SPACING_Y  # Espacio entre campos

        # ========== Botones centrados ==========
        fb = tk.Frame(self, bg=SECONDARY)
        fb.grid(row=3, column=0, pady=(0, 20), sticky='ew')
        fb.grid_columnconfigure(0, weight=1)
        fb.grid_columnconfigure(3, weight=1)

        btn_calc = ttk.Button(fb, text="Calcular", style='Accent.TButton',
                              cursor='hand2', command=self.on_calculate)
        if self.icon_calc:
            btn_calc.configure(image=self.icon_calc, compound='left')
        btn_calc.grid(row=0, column=1, padx=5)

        btn_clear = ttk.Button(fb, text="Limpiar", style='Accent.TButton',
                               cursor='hand2', command=self.on_clear)
        if self.icon_clear:
            btn_clear.configure(image=self.icon_clear, compound='left')
        btn_clear.grid(row=0, column=2, padx=5)

        # ========== Curva de Acoplador ==========
        c_plot = tk.Canvas(self, bg='white', highlightthickness=1,
                           highlightbackground=PRIMARY)
        c_plot.grid(row=1, column=1, rowspan=4, padx=PAD_X, pady=PAD_Y, sticky='nsew')
        self.plot_canvas = c_plot

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # Cargar y redimensionar la imagen al tamaño del canvas
        try:
            imagen_original = Image.open("esquema.jpg")
            ancho_canvas = self.plot_canvas.winfo_reqwidth()
            alto_canvas = self.plot_canvas.winfo_reqheight()
            imagen_redimensionada = imagen_original.resize((ancho_canvas, alto_canvas))
            self.imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)
            self.plot_canvas.create_image(40, 170, anchor='nw', image=self.imagen_tk)
        except Exception as e:
            print("Error al cargar la imagen:", e)

    def calcular_cinematica(self):
        # Diccionario con datos de referencia por altura
        self.data_por_altura = {
            120: {"theta2": 139, "y0": 0.247},
            130: {"theta2": 144, "y0": 0.241},
            140: {"theta2": 147, "y0": 0.235},
            150: {"theta2": 149, "y0": 0.234},
            160: {"theta2": 150, "y0": 0.230},
            170: {"theta2": 151, "y0": 0.229},
            180: {"theta2": 151, "y0": 0.229},
            190: {"theta2": 150, "y0": 0.229},
            200: {"theta2": 149, "y0": 0.234},
        }

        try:
            altura = int(self.entry_attack.get())
            L1 = float(self.entry_L1.get())
            L2 = float(self.entry_L2.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor selecciona valores válidos para altura, L1 y L2.")
            return

        datos = self.data_por_altura.get(altura)
        if not datos:
            messagebox.showerror("Error", f"No hay datos precalculados para altura = {altura}.")
            return

        theta2 = datos["theta2"]
        y0 = datos["y0"]
        #altura = int(self.entry_attack.get())
        #L1 = float(self.entry_L1.get())
        #L2 = float(self.entry_L2.get())

        g = 9.81  # gravedad en m/s²
        # convertir mm a metros
        y0_m = y0/1000  
        L1_m = L1/1000
        L2_m = L2/1000

        # velocidad de B (caída libre)
        vB = round(math.sqrt(2*g*altura*0.001),2)
        # posición de punto A 
        Ax = L1_m*math.cos(math.radians(theta2))
        Ay = L1_m*math.sin(math.radians(theta2))
        # posición de punto B respecto a A
        rB_Ax = L2_m-Ax	
        rB_Ay = -Ay
        # velocidades angulares
        omega1 = round((vB*rB_Ax)/(Ax*rB_Ay-Ay*rB_Ax),1)
        omega2 = round((Ax*vB)/(Ax*rB_Ay-Ay*rB_Ax),2)
        # aceleración del punto B
        aB=-g
        # velocidad del punto A
        vA = round((omega1*math.sqrt(Ax**2+Ay**2)),2)

        
        #alfa1=(vB*rB_Ay-(-(omega1**2)*rB_Ay)-(-(rB_Ay**2)*Ay))/(Ay*rB_Ay-Ax*rB_Ax)


        # Mostrar resultados
        resultados = {
            "velocidad_angular_ω₁_(rad/s)": omega1,
            #"aceleración_angular_α₁_(rad/s²)": alfa1,
            "ángulo_de_entrada_θ₂_(°)": theta2,
            
            "velocidad_angular_ω₂_(rad/s)": omega2,
            #"aceleración_angular_α₂_(rad/s²)":
            
            "velocidad_va_(mm/s)": vA,
            #"aceleración_aa_(mm/s²)":
            "velocidad_vb_(mm/s)": vB,
            "aceleración_ab_(mm/s²)": aB
            #"velocidad_vd_(mm/s)":
            #"aceleración_ad_(mm/s²)":
        }

        for clave, valor in resultados.items():
            if clave in self.kin_entries_dict:
                campo = self.kin_entries_dict[clave]
                campo.configure(state="normal")
                campo.delete(0, tk.END)
                campo.insert(0, str(valor))
                campo.configure(state="readonly")

    def on_calculate(self):
        """Valida las entradas geométricas y ejecuta los cálculos cinemáticos."""

        raw = {
            "Altura de entrada": self.entry_attack.get(),
            "Longitud L₁":        self.entry_L1.get(),
            "Longitud L₂":        self.entry_L2.get(),
        }

        # Validación de campos vacíos o con espacios
        errores = []
        for k, v in raw.items():
            if v.strip() == "":
                errores.append(k)
            elif "," in v:
                errores.append(f"{k} (usa punto en lugar de coma)")

        if errores:
            messagebox.showerror("Error de entrada", "Corrige los siguientes campos:\n" + "\n".join(errores))
            return

        try:
            attack = float(raw["Altura de entrada"])
            L1     = float(raw["Longitud L₁"])
            L2     = float(raw["Longitud L₂"])
        except ValueError:
            messagebox.showerror("Error", "Los valores deben ser numéricos válidos.")
            return

        # Ejecutar cálculo cinemático y mostrar resultados
        self.calcular_cinematica()
        messagebox.showinfo("Listo", "Resultados cinemáticos calculados correctamente.")


    def on_clear(self):
        """Limpia todos los campos de entrada."""
        for e in (self.entry_attack, self.entry_L1, self.entry_L2,
                  self.entry_theta2, self.entry_theta3,
                  self.entry_omega2, self.entry_alpha2):
            e.delete(0, tk.END)

class Tooltip:
    def __init__(self, widget, text, delay=500):
        """
        widget: el widget o canvas sobre el que se activa el tooltip
        text:   el texto a mostrar
        delay:  milisegundos antes de aparecer el tooltip
        """
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip = None
        self._after_id = None

        widget.bind("<Enter>", self._schedule)
        widget.bind("<Leave>", self._hide)
        widget.bind("<Motion>", self._move)  # para reposicionar si mueves el mouse

    def _schedule(self, event=None):
        self._unschedule()
        self._after_id = self.widget.after(self.delay, self._show)

    def _unschedule(self):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None

    def _show(self):
        if self.tooltip:
            return
        # Calculamos posición cerca del widget
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty() + 5

        # Creamos Toplevel sin decoración
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        self.tooltip.attributes('-alpha', 0.90)

        label = tk.Label(self.tooltip,
                         text=self.text,
                         background="#333333",
                         foreground="white",
                         relief='solid',
                         borderwidth=1,
                         font=("Segoe UI", 9),
                         padx=6, pady=3,
                         wraplength=200,
                         justify='left')
        label.pack()

    def _move(self, event):
        # Si ya está visible, reposicionamos al mover el mouse
        if self.tooltip:
            x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
            y = self.widget.winfo_rooty() + 5
            self.tooltip.wm_geometry(f"+{x}+{y}")

    def _hide(self, event=None):
        self._unschedule()
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

if __name__ == "__main__":
    app = CatapultApp()
    app.mainloop()