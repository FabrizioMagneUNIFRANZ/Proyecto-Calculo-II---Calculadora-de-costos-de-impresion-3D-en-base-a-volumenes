from tkinter import BOTH, LEFT, RIGHT, TOP, Frame, Label, Toplevel, X

def mostrar_resultados(raiz, datos_resultado):
    ventana = Toplevel(raiz)
    ventana.title("Resultados de la impresion")
    ventana.geometry("1000x700")

    panel_texto = Frame(ventana)
    panel_texto.pack(side=TOP, fill=X, padx=10, pady=10)

    resumen = construir_resumen(datos_resultado)
    Label(panel_texto, text=resumen, justify="left", anchor="w").pack(fill=X)

    panel_grafico = Frame(ventana)
    panel_grafico.pack(fill=BOTH, expand=True, padx=10, pady=10)

    try:
        figura = crear_figura_matplotlib(
            datos_resultado["figura"],
            datos_resultado["parametros_unidad"],
            datos_resultado["unidad"],
        )
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        canvas = FigureCanvasTkAgg(figura, master=panel_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)
    except Exception as exc:
        mensaje = (
            "No se pudo generar la vista previa de la figura.\n"
            "Verifica que matplotlib y numpy esten instalados en el entorno activo.\n\n"
            f"Detalle: {exc}"
        )
        Label(panel_grafico, text=mensaje, justify="left", anchor="w").pack(side=RIGHT, fill=BOTH, expand=True)

    return ventana

def construir_resumen(datos):
    parametros = ", ".join(
        f"{nombre}={valor:.4f} {datos['unidad']}"
        for nombre, valor in datos["parametros_unidad"].items()
    )
    return (
        f"Figura: {datos['figura']}\n"
        f"Parametros: {parametros}\n"
        f"Calculo matematico interno: {datos['integral_usada']}\n"
        f"Material: {datos['material']}\n"
        f"Densidad: {datos['densidad']:.2f} g/cm^3 | Costo: {datos['costo_material']:.2f} Bs/g\n"
        f"Volumen geometrico: {datos['volumen_unidad3']:.4f} {datos['unidad']}^3\n"
        f"Volumen geometrico convertido: {datos['volumen_cm3']:.4f} cm^3\n"
        f"Material usado: {datos['ocupacion']:.1f}% | Extra por soportes: {datos['soportes']:.1f}% | "
        f"Margen por desperdicio: {datos['desperdicio']:.1f}%\n"
        f"Volumen de material estimado: {datos['costos']['volumen_material_cm3']:.4f} cm^3\n"
        f"Masa estimada: {datos['costos']['masa_g']:.4f} g\n"
        f"Costo material: {datos['costos']['costo_material_bs']:.2f} Bs\n"
        f"Costo por tiempo de impresion: {datos['costos']['costo_tiempo_bs']:.2f} Bs\n"
        f"Costo total estimado: {datos['costos']['costo_total_bs']:.2f} Bs"
    )

def crear_figura_matplotlib(figura, parametros_unidad, unidad):
    import numpy as np
    from matplotlib.figure import Figure

    fig = Figure(figsize=(7, 5), dpi=100)
    ax = fig.add_subplot(111, projection="3d")

    color = "#4F81BD"
    alpha = 0.75

    if figura == "Prisma rectangular":
        largo = parametros_unidad["Largo"]
        ancho = parametros_unidad["Ancho"]
        alto = parametros_unidad["Alto"]
        _graficar_prisma(ax, largo, ancho, alto, color, alpha)
    elif figura == "Cilindro":
        radio = parametros_unidad["Radio"]
        altura = parametros_unidad["Altura"]
        _graficar_cilindro(ax, radio, altura, color, alpha)
    elif figura == "Esfera":
        radio = parametros_unidad["Radio"]
        _graficar_esfera(ax, radio, color, alpha, media=False)
    elif figura == "Semiesfera":
        radio = parametros_unidad["Radio"]
        _graficar_esfera(ax, radio, color, alpha, media=True)
    elif figura == "Cono":
        radio = parametros_unidad["Radio"]
        altura = parametros_unidad["Altura"]
        _graficar_cono(ax, radio, altura, color, alpha)
    elif figura == "Paraboloide":
        radio = parametros_unidad["Radio"]
        altura = parametros_unidad["Altura"]
        _graficar_paraboloide(ax, radio, altura, color, alpha)
    else:
        raise ValueError("Figura no soportada para visualizacion.")

    ax.set_title(f"Muestra de {figura}")
    ax.set_xlabel(f"X ({unidad})")
    ax.set_ylabel(f"Y ({unidad})")
    ax.set_zlabel(f"Z ({unidad})")
    _ajustar_aspecto(ax)
    return fig

def _graficar_prisma(ax, largo, ancho, alto, color, alpha):
    import numpy as np

    x = np.array([[0, largo], [0, largo]])
    y = np.array([[0, 0], [ancho, ancho]])
    z0 = np.zeros((2, 2))
    z1 = np.full((2, 2), alto)

    ax.plot_surface(x, y, z0, color=color, alpha=alpha)
    ax.plot_surface(x, y, z1, color=color, alpha=alpha)

    y_side = np.array([[0, 0], [0, 0]])
    y_side2 = np.array([[ancho, ancho], [ancho, ancho]])
    z_side = np.array([[0, 0], [alto, alto]])
    x_side = np.array([[0, largo], [0, largo]])
    ax.plot_surface(x_side, y_side, z_side, color=color, alpha=alpha)
    ax.plot_surface(x_side, y_side2, z_side, color=color, alpha=alpha)

    x_side2 = np.array([[0, 0], [0, 0]])
    x_side3 = np.array([[largo, largo], [largo, largo]])
    y_face = np.array([[0, ancho], [0, ancho]])
    z_face = np.array([[0, 0], [alto, alto]])
    ax.plot_surface(x_side2, y_face, z_face, color=color, alpha=alpha)
    ax.plot_surface(x_side3, y_face, z_face, color=color, alpha=alpha)

def _graficar_cilindro(ax, radio, altura, color, alpha):
    import numpy as np

    theta = np.linspace(0, 2 * np.pi, 40)
    z = np.linspace(0, altura, 30)
    theta_m, z_m = np.meshgrid(theta, z)
    x = radio * np.cos(theta_m)
    y = radio * np.sin(theta_m)
    ax.plot_surface(x, y, z_m, color=color, alpha=alpha)

    r_grid = np.linspace(0, radio, 25)
    theta_base, r_base = np.meshgrid(theta, r_grid)
    x_base = r_base * np.cos(theta_base)
    y_base = r_base * np.sin(theta_base)
    ax.plot_surface(x_base, y_base, np.zeros_like(x_base), color=color, alpha=alpha * 0.8)
    ax.plot_surface(x_base, y_base, np.full_like(x_base, altura), color=color, alpha=alpha * 0.8)

def _graficar_esfera(ax, radio, color, alpha, media=False):
    import numpy as np

    u = np.linspace(0, 2 * np.pi, 50)
    v_max = np.pi / 2 if media else np.pi
    v = np.linspace(0, v_max, 40)
    u_m, v_m = np.meshgrid(u, v)
    x = radio * np.cos(u_m) * np.sin(v_m)
    y = radio * np.sin(u_m) * np.sin(v_m)
    z = radio * np.cos(v_m)
    ax.plot_surface(x, y, z, color=color, alpha=alpha)

def _graficar_cono(ax, radio, altura, color, alpha):
    import numpy as np

    theta = np.linspace(0, 2 * np.pi, 50)
    t = np.linspace(0, 1, 30)
    theta_m, t_m = np.meshgrid(theta, t)
    radios = radio * (1 - t_m)
    x = radios * np.cos(theta_m)
    y = radios * np.sin(theta_m)
    z = altura * t_m
    ax.plot_surface(x, y, z, color=color, alpha=alpha)

def _graficar_paraboloide(ax, radio, altura, color, alpha):
    import numpy as np

    theta = np.linspace(0, 2 * np.pi, 50)
    radios = np.linspace(0, radio, 35)
    theta_m, r_m = np.meshgrid(theta, radios)
    x = r_m * np.cos(theta_m)
    y = r_m * np.sin(theta_m)
    z = altura * (1 - (r_m**2 / radio**2))
    ax.plot_surface(x, y, z, color=color, alpha=alpha)

def _ajustar_aspecto(ax):
    x_lim = ax.get_xlim3d()
    y_lim = ax.get_ylim3d()
    z_lim = ax.get_zlim3d()
    rangos = [
        abs(x_lim[1] - x_lim[0]),
        abs(y_lim[1] - y_lim[0]),
        abs(z_lim[1] - z_lim[0]),
    ]
    max_rango = max(rangos) if max(rangos) else 1
    try:
        ax.set_box_aspect([r / max_rango for r in rangos])
    except AttributeError:
        pass

