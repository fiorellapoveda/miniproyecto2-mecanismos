import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import os, tkinter as tk
from tkinter import ttk, messagebox
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
        """Interfaz con secciones en Canvas: esquinas redondas, sin bordes grises."""
        LIGHT_BLUE      = '#D6EAF8'
        SEC_W           = 320
        GEO_H, ANG_H, KIN_H = 150, 120, 120
        PAD_X, PAD_Y    = 20, 15
        OFFSET_Y        = 50
        SPACING_Y       = 30
        ENTRY_X_GEO     = 170
        ENTRY_X_ANG     = 120
        ENTRY_X_KIN     = 140

        # — Título —
        lbl_title = ttk.Label(self, text="Mecanismo de Catapulta", style='Header.TLabel')
        lbl_title.grid(row=0, column=0, columnspan=2, pady=(20,10))

        # ========== Sección Geométrica ==========
        c_geo = tk.Canvas(self, width=SEC_W, height=GEO_H, bg=SECONDARY, highlightthickness=0)
        c_geo.grid(row=1, column=0, padx=PAD_X, pady=PAD_Y, sticky='nw')
        self.create_rounded_rect(c_geo, 0, 0, SEC_W-1, GEO_H-1, r=20, fill=LIGHT_BLUE, outline='')
        c_geo.create_text(15, 15, text="Parámetros Geométricos", anchor='nw', fill=PRIMARY,
                          font=('Segoe UI', 12, 'bold'))

        geom_labels = ["Distancia de ataque:", "Longitud L₁:", "Longitud L₂:"]
        geom_tips   = [
            "Distancia desde el punto fijo hasta la posición de liberación del proyectil.",
            "Longitud del primer eslabón desde el punto fijo hasta la primera unión.",
            "Longitud del segundo eslabón, conectando la unión al acoplador."
        ]
        for i, txt in enumerate(geom_labels):
            y = OFFSET_Y + i * SPACING_Y
            # Etiqueta y entrada
            lbl = tk.Label(self, text=txt, bg=LIGHT_BLUE, fg=PRIMARY, font=('Segoe UI', 10))
            c_geo.create_window((15, y), window=lbl, anchor='nw')
            ent = ttk.Entry(c_geo, width=14)
            c_geo.create_window((ENTRY_X_GEO, y), window=ent, anchor='nw')
            if i == 0:
                self.entry_attack = ent
            elif i == 1:
                self.entry_L1 = ent
            else:
                self.entry_L2 = ent

            # Ícono “i” como Canvas widget
            info_w = tk.Canvas(c_geo, width=16, height=16, bg=LIGHT_BLUE, highlightthickness=0, bd=0)
            info_w.create_oval(0, 0, 16, 16, fill="#1976d2", outline="")
            info_w.create_text(8, 8, text="i", fill="white", font=("Segoe UI", 8, "bold"))
            c_geo.create_window((ENTRY_X_GEO - 30, y), window=info_w, anchor='nw')
            Tooltip(info_w, geom_tips[i])

        # ========== Sección Ángulos ==========
        c_ang = tk.Canvas(self, width=SEC_W, height=ANG_H, bg=SECONDARY, highlightthickness=0)
        c_ang.grid(row=2, column=0, padx=PAD_X, pady=PAD_Y, sticky='nw')
        self.create_rounded_rect(c_ang, 0, 0, SEC_W-1, ANG_H-1, r=20, fill=LIGHT_BLUE, outline='')
        c_ang.create_text(15, 15, text="Ángulos de Referencia", anchor='nw', fill=PRIMARY,
                          font=('Segoe UI', 12, 'bold'))

        ang_labels = ["θ₂ (°):", "θ₃ (°):"]
        ang_tips   = [
            "Ángulo inicial del eslabón de entrada medido desde la horizontal.",
            "Ángulo del segundo eslabón respecto a un eje fijo o relativo."
        ]
        for i, txt in enumerate(ang_labels):
            y = OFFSET_Y + i * SPACING_Y
            lbl = tk.Label(self, text=txt, bg=LIGHT_BLUE, fg=PRIMARY, font=('Segoe UI', 10))
            c_ang.create_window((15, y), window=lbl, anchor='nw')
            ent = ttk.Entry(c_ang, width=14)
            c_ang.create_window((ENTRY_X_ANG, y), window=ent, anchor='nw')
            if i == 0:
                self.entry_theta2 = ent
            else:
                self.entry_theta3 = ent

            info_w = tk.Canvas(c_ang, width=16, height=16, bg=LIGHT_BLUE, highlightthickness=0, bd=0)
            info_w.create_oval(0, 0, 16, 16, fill="#1976d2", outline="")
            info_w.create_text(8, 8, text="i", fill="white", font=("Segoe UI", 8, "bold"))
            c_ang.create_window((ENTRY_X_ANG - 30, y), window=info_w, anchor='nw')
            Tooltip(info_w, ang_tips[i])

        # ========== Sección Cinématica ==========
        c_kin = tk.Canvas(self, width=SEC_W, height=KIN_H, bg=SECONDARY, highlightthickness=0)
        c_kin.grid(row=3, column=0, padx=PAD_X, pady=PAD_Y, sticky='nw')
        self.create_rounded_rect(c_kin, 0, 0, SEC_W-1, KIN_H-1, r=20, fill=LIGHT_BLUE, outline='')
        c_kin.create_text(15, 15, text="Parámetros Cinématicos", anchor='nw', fill=PRIMARY,
                          font=('Segoe UI', 12, 'bold'))

        kin_labels = ["ω₂ (rad/s):", "α₂ (rad/s²):"]
        kin_tips   = [
            "Velocidad angular del eslabón de entrada. Se expresa en radianes por segundo.",
            "Aceleración angular del eslabón de entrada. Se mide en rad/s²."
        ]
        for i, txt in enumerate(kin_labels):
            y = OFFSET_Y + i * SPACING_Y
            lbl = tk.Label(self, text=txt, bg=LIGHT_BLUE, fg=PRIMARY, font=('Segoe UI', 10))
            c_kin.create_window((15, y), window=lbl, anchor='nw')
            ent = ttk.Entry(c_kin, width=14)
            c_kin.create_window((ENTRY_X_KIN, y), window=ent, anchor='nw')
            if i == 0:
                self.entry_omega2 = ent
            else:
                self.entry_alpha2 = ent

            info_w = tk.Canvas(c_kin, width=16, height=16, bg=LIGHT_BLUE, highlightthickness=0, bd=0)
            info_w.create_oval(0, 0, 16, 16, fill="#1976d2", outline="")
            info_w.create_text(8, 8, text="i", fill="white", font=("Segoe UI", 8, "bold"))
            c_kin.create_window((ENTRY_X_KIN - 30, y), window=info_w, anchor='nw')
            Tooltip(info_w, kin_tips[i])

        # ========== Botones centrados ==========
        fb = tk.Frame(self, bg=SECONDARY)
        fb.grid(row=4, column=0, pady=(0, 20), sticky='ew')
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
        
    def on_calculate(self):
        """Recupera entradas, valida espacios y separador decimal, convierte a float."""
        # 1) Captura cruda de cada campo
        raw = {
            "Distancia de ataque": self.entry_attack.get(),
            "Longitud L₁":         self.entry_L1.get(),
            "Longitud L₂":         self.entry_L2.get(),
            "Ángulo θ₂":           self.entry_theta2.get(),
            "Ángulo θ₃":           self.entry_theta3.get(),
            "Velocidad ω₂":        self.entry_omega2.get(),
            "Aceleración α₂":      self.entry_alpha2.get(),
        }

        # 2) Detectar vacíos y espacios
        empty_fields   = [k for k,v in raw.items() if v == ""]
        single_space   = [k for k,v in raw.items() if v == " "]
        multi_space    = [k for k,v in raw.items() if v.strip() == "" and len(v) > 1]
        whitespace_err = bool(empty_fields or single_space or multi_space)

        # 3) Detectar comas
        comma_multi    = [k for k,v in raw.items() if v.count(",") > 1]
        comma_single   = [k for k,v in raw.items() if v.count(",") == 1]
        decimal_err    = bool(comma_multi or comma_single)

        # 4) Si hay ambos tipos de error, mensaje combinado
        if whitespace_err and decimal_err:
            messagebox.showerror(
                "Error de entrada",
                "Algunas casillas están vacías o contienen solo espacios y otras usan coma como separador decimal.\n"
                "Por favor ingresa valores válidos y utiliza el punto (`.`) como separador."
            )
            return

        # 5) Sólo errores de espacios/vacíos
        if whitespace_err:
            if multi_space:
                messagebox.showerror(
                    "Espacios inválidos",
                    "Hay múltiples espacios vacíos en los campos:\n" +
                    "\n".join(multi_space)
                )
                return
            if single_space:
                messagebox.showerror(
                    "Espacio aislado",
                    "El/Los campo(s) " + ", ".join(single_space) +
                    " contienen un único espacio. Por favor ingresa un valor o bórralo."
                )
                return
            if empty_fields:
                messagebox.showerror(
                    "Campos vacíos",
                    "Los siguientes campos están vacíos:\n" +
                    "\n".join(empty_fields)
                )
                return

        # 6) Sólo errores de separador decimal
        if decimal_err:
            if comma_multi:
                messagebox.showerror(
                    "Separadores decimales",
                    "Hay múltiples comas (`,`) en los campos:\n" +
                    "\n".join(comma_multi) +
                    "\nUsa solo un punto (`.`) como separador."
                )
                return
            if comma_single:
                messagebox.showerror(
                    "Separador decimal incorrecto",
                    "El/Los campo(s) " + ", ".join(comma_single) +
                    " contienen una coma como separador decimal.\n"
                    "Por favor utiliza el punto (`.`) en su lugar."
                )
                return

        # 7) Conversión a float (resto de validación)
        try:
            attack = float(raw["Distancia de ataque"])
            L1     = float(raw["Longitud L₁"])
            L2     = float(raw["Longitud L₂"])
            theta2 = float(raw["Ángulo θ₂"])
            theta3 = float(raw["Ángulo θ₃"])
            omega2 = float(raw["Velocidad ω₂"])
            alpha2 = float(raw["Aceleración α₂"])
        except ValueError:
            messagebox.showerror(
                "Error de entrada",
                "Por favor ingresa valores numéricos válidos en todos los campos."
            )
            return

        # TODO: implementar lógica de Grashof, velocidades, aceleraciones, curva...
        messagebox.showinfo("Listo", "Entradas válidas. Ejecutando cálculos...")

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