from tkinter import Button, Entry, Label, OptionMenu, StringVar, Tk, messagebox

from costos import calcular_costos
from figuras import FIGURAS, calcular_volumen_figura
from resultados import mostrar_resultados
from validacion import FACTORES_LONGITUD_CM, evaluar_real

MATERIALES = {
    "PLA": {"densidad": 1.25, "costo": 0.15},
    "ABS": {"densidad": 1.04, "costo": 0.20},
    "PETG": {"densidad": 1.27, "costo": 0.18},
    "Resina estandar": {"densidad": 1.10, "costo": 0.25},
    "Resina flexible": {"densidad": 1.15, "costo": 0.30},
}

class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora 3D - Figuras y Costos")

        for columna in range(4):
            self.root.grid_columnconfigure(columna, weight=1)

        self.figura_var = StringVar(self.root, value="Prisma rectangular")
        self.unidad_var = StringVar(self.root, value="cm")
        self.material_var = StringVar(self.root, value="PLA")
        self.ocupacion_var = StringVar(value="100")
        self.soportes_var = StringVar(value="0")
        self.desperdicio_var = StringVar(value="5")
        self.tiempo_var = StringVar(value="1")
        self.tarifa_var = StringVar(value="0")
        self.descripcion_var = StringVar()

        self.param_vars = [StringVar(), StringVar(), StringVar()]
        self.param_label_widgets = []
        self.param_entries = []
        self.param_hint_widgets = []
        self.ultima_ventana_resultados = None

        self._crear_layout()
        self.figura_var.trace_add("write", self.actualizar_campos_figura)
        self.actualizar_campos_figura()

    def _crear_layout(self):
        fila = 0
        Label(self.root, text="Figura a imprimir:").grid(row=fila, column=0, sticky="w", padx=4, pady=2)
        OptionMenu(self.root, self.figura_var, *FIGURAS.keys()).grid(
            row=fila, column=1, columnspan=3, sticky="ew", padx=4, pady=2
        )

        fila += 1
        Label(self.root, text="Unidad de entrada:").grid(row=fila, column=0, sticky="w", padx=4, pady=2)
        OptionMenu(self.root, self.unidad_var, "mm", "cm", "m").grid(
            row=fila, column=1, sticky="ew", padx=4, pady=2
        )

        fila += 1
        Label(self.root, textvariable=self.descripcion_var, justify="left", anchor="w").grid(
            row=fila, column=0, columnspan=4, sticky="ew", padx=4, pady=4
        )

        for indice in range(3):
            fila += 1
            label_widget = Label(self.root, text="")
            label_widget.grid(row=fila, column=0, sticky="w", padx=4, pady=2)
            entrada = Entry(self.root, textvariable=self.param_vars[indice])
            entrada.grid(row=fila, column=1, sticky="ew", padx=4, pady=2)
            pista = Label(self.root, text="", justify="left", anchor="w")
            pista.grid(row=fila, column=2, columnspan=2, sticky="w", padx=4, pady=2)
            self.param_label_widgets.append(label_widget)
            self.param_entries.append(entrada)
            self.param_hint_widgets.append(pista)

        fila += 1
        Label(self.root, text="Material:").grid(row=fila, column=0, sticky="w", padx=4, pady=2)
        OptionMenu(self.root, self.material_var, *MATERIALES.keys()).grid(
            row=fila, column=1, sticky="ew", padx=4, pady=2
        )

        fila += 1
        Label(self.root, text="Material usado (%):").grid(row=fila, column=0, sticky="w", padx=4, pady=2)
        Entry(self.root, textvariable=self.ocupacion_var).grid(row=fila, column=1, sticky="ew", padx=4, pady=2)
        Label(self.root, text="Extra por soportes (%):").grid(row=fila, column=2, sticky="w", padx=4, pady=2)
        Entry(self.root, textvariable=self.soportes_var).grid(row=fila, column=3, sticky="ew", padx=4, pady=2)

        fila += 1
        Label(self.root, text="Margen por desperdicio (%):").grid(row=fila, column=0, sticky="w", padx=4, pady=2)
        Entry(self.root, textvariable=self.desperdicio_var).grid(row=fila, column=1, sticky="ew", padx=4, pady=2)
        Label(self.root, text="Horas estimadas (h):").grid(row=fila, column=2, sticky="w", padx=4, pady=2)
        Entry(self.root, textvariable=self.tiempo_var).grid(row=fila, column=3, sticky="ew", padx=4, pady=2)

        fila += 1
        Label(self.root, text="Costo por hora (Bs/h):").grid(row=fila, column=0, sticky="w", padx=4, pady=2)
        Entry(self.root, textvariable=self.tarifa_var).grid(row=fila, column=1, sticky="ew", padx=4, pady=2)

        fila += 1
        Button(self.root, text="Calcular", command=self.ejecutar_calculo).grid(
            row=fila, column=0, columnspan=4, sticky="ew", padx=4, pady=6
        )

        fila += 1
        ayuda_texto = (
            "Uso recomendado:\n"
            "- Elige una figura conocida.\n"
            "- Ingresa solo sus dimensiones basicas.\n"
            "- El sistema calcula el volumen con integrales internamente.\n"
            "- Luego estima material, masa y costo de impresion.\n"
            "- Si la pieza no es maciza, reduce el porcentaje de material usado.\n"
            "- Si la impresion necesita soportes, agrega un porcentaje extra.\n"
            "- Puedes ingresar expresiones simples como pi/2."
        )
        Label(self.root, text=ayuda_texto, justify="left", anchor="w").grid(
            row=fila, column=0, columnspan=4, sticky="ew", padx=4, pady=4
        )

    def actualizar_campos_figura(self, *_args):
        figura = self.figura_var.get()
        definicion = FIGURAS[figura]

        self.descripcion_var.set(
            f"{definicion['descripcion']}\n"
            "El programa calcula el volumen por dentro usando integrales y luego estima el costo de impresion."
        )

        for indice, label_widget in enumerate(self.param_label_widgets):
            if indice < len(definicion["parametros"]):
                nombre, detalle = definicion["parametros"][indice]
                label_widget.config(text=f"{nombre}:")
                self.param_hint_widgets[indice].config(text=detalle)
                self.param_vars[indice].set(definicion["defaults"][indice])
                label_widget.grid()
                self.param_entries[indice].grid()
                self.param_hint_widgets[indice].grid()
            else:
                label_widget.grid_remove()
                self.param_entries[indice].grid_remove()
                self.param_hint_widgets[indice].grid_remove()
                self.param_vars[indice].set("")

    def ejecutar_calculo(self):
        try:
            figura = self.figura_var.get()
            unidad = self.unidad_var.get()
            factor = FACTORES_LONGITUD_CM[unidad]
            definicion = FIGURAS[figura]

            parametros_cm = {}
            parametros_unidad = {}
            for indice, (nombre, _) in enumerate(definicion["parametros"]):
                valor_unidad = evaluar_real(self.param_vars[indice].get(), nombre)
                parametros_unidad[nombre] = valor_unidad
                parametros_cm[nombre] = valor_unidad * factor

            volumen_cm3, integral_usada = calcular_volumen_figura(figura, parametros_cm)
            volumen_unidad3 = volumen_cm3 / (factor**3)

            material = self.material_var.get()
            densidad = MATERIALES[material]["densidad"]
            costo_material = MATERIALES[material]["costo"]

            ocupacion = evaluar_real(self.ocupacion_var.get(), "Porcentaje de material usado")
            soportes = evaluar_real(self.soportes_var.get(), "Material extra por soportes", permitir_cero=True)
            desperdicio = evaluar_real(
                self.desperdicio_var.get(), "Margen extra por desperdicio", permitir_cero=True
            )
            tiempo = evaluar_real(self.tiempo_var.get(), "Horas estimadas de impresion", permitir_cero=True)
            tarifa = evaluar_real(self.tarifa_var.get(), "Costo por hora de impresion", permitir_cero=True)

            if ocupacion > 100:
                raise ValueError("El porcentaje de material usado debe estar entre 0 y 100.")

            costos = calcular_costos(
                volumen_cm3, densidad, costo_material, ocupacion, soportes, desperdicio, tiempo, tarifa
            )

            datos_resultado = {
                "figura": figura,
                "unidad": unidad,
                "parametros_unidad": parametros_unidad,
                "integral_usada": integral_usada,
                "material": material,
                "densidad": densidad,
                "costo_material": costo_material,
                "volumen_unidad3": volumen_unidad3,
                "volumen_cm3": volumen_cm3,
                "ocupacion": ocupacion,
                "soportes": soportes,
                "desperdicio": desperdicio,
                "costos": costos,
            }

            if self.ultima_ventana_resultados is not None and self.ultima_ventana_resultados.winfo_exists():
                self.ultima_ventana_resultados.destroy()

            self.ultima_ventana_resultados = mostrar_resultados(self.root, datos_resultado)
        except Exception as exc:
            messagebox.showerror("Error de calculo", str(exc))

def crear_interfaz():
    root = Tk()
    CalculadoraApp(root)
    return root

