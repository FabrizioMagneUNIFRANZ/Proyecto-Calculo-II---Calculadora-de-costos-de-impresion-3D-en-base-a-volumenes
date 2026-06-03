import sympy as sp

FIGURAS = {
    "Prisma rectangular": {
        "parametros": [
            ("Largo", "Dimension en el eje x"),
            ("Ancho", "Dimension en el eje y"),
            ("Alto", "Dimension en el eje z"),
        ],
        "defaults": ["10", "8", "5"],
        "descripcion": "Caja o bloque rectangular.",
    },
    "Cilindro": {
        "parametros": [
            ("Radio", "Radio de la base circular"),
            ("Altura", "Altura del cilindro"),
        ],
        "defaults": ["5", "12"],
        "descripcion": "Cilindro recto de base circular.",
    },
    "Esfera": {
        "parametros": [("Radio", "Radio de la esfera")],
        "defaults": ["6"],
        "descripcion": "Esfera completa.",
    },
    "Semiesfera": {
        "parametros": [("Radio", "Radio de la semiesfera")],
        "defaults": ["6"],
        "descripcion": "Mitad superior de una esfera.",
    },
    "Cono": {
        "parametros": [
            ("Radio", "Radio de la base"),
            ("Altura", "Altura del cono"),
        ],
        "defaults": ["5", "10"],
        "descripcion": "Cono circular recto.",
    },
    "Paraboloide": {
        "parametros": [
            ("Radio", "Radio de la base"),
            ("Altura", "Altura maxima del paraboloide"),
        ],
        "defaults": ["5", "10"],
        "descripcion": "Paraboloide circular truncado en la base.",
    },
}

def calcular_volumen_figura(figura, parametros_cm):
    z = sp.symbols("z", nonnegative=True)
    x = sp.Symbol("x")
    y = sp.Symbol("y")

    r_sym = sp.Symbol("r", positive=True)
    theta_sym = sp.Symbol("theta", positive=True)
    rho_sym = sp.Symbol("rho", positive=True)
    phi_sym = sp.Symbol("phi", positive=True)

    if figura == "Prisma rectangular":
        largo = parametros_cm["Largo"]
        ancho = parametros_cm["Ancho"]
        alto = parametros_cm["Alto"]
        volumen = sp.integrate(1, (x, 0, largo), (y, 0, ancho), (z, 0, alto))
        integral = "Integral triple rectangular de 1"
    elif figura == "Cilindro":
        radio = parametros_cm["Radio"]
        altura = parametros_cm["Altura"]
        volumen = sp.integrate(r_sym, (theta_sym, 0, 2 * sp.pi), (r_sym, 0, radio), (z, 0, altura))
        integral = "Integral triple cilindrica con jacobiano r"
    elif figura == "Esfera":
        radio = parametros_cm["Radio"]
        volumen = sp.integrate(
            rho_sym**2 * sp.sin(phi_sym),
            (theta_sym, 0, 2 * sp.pi),
            (phi_sym, 0, sp.pi),
            (rho_sym, 0, radio),
        )
        integral = "Integral triple esferica con jacobiano rho^2*sin(phi)"
    elif figura == "Semiesfera":
        radio = parametros_cm["Radio"]
        volumen = sp.integrate(
            rho_sym**2 * sp.sin(phi_sym),
            (theta_sym, 0, 2 * sp.pi),
            (phi_sym, 0, sp.pi / 2),
            (rho_sym, 0, radio),
        )
        integral = "Integral triple esferica sobre media esfera"
    elif figura == "Cono":
        radio = float(sp.N(parametros_cm["Radio"]))
        altura = float(sp.N(parametros_cm["Altura"]))
        # Volumen de un cono: (1/3) * pi * R^2 * H
        volumen = (1 / 3) * sp.pi * (radio**2) * altura
        integral = "Formula geometrica: (1/3)*pi*R^2*H"
    elif figura == "Paraboloide":
        radio = float(sp.N(parametros_cm["Radio"]))
        altura = float(sp.N(parametros_cm["Altura"]))
        # Volumen de un paraboloide circular: (1/2) * pi * R^2 * H
        volumen = (1 / 2) * sp.pi * (radio**2) * altura
        integral = "Formula geometrica: (1/2)*pi*R^2*H"
    else:
        raise ValueError("Figura no soportada.")

    return float(sp.N(volumen)), integral
