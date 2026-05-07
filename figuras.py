import sympy as sp

r, theta, rho, phi = sp.symbols("r theta rho phi", positive=True)

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

    if figura == "Prisma rectangular":
        largo = parametros_cm["Largo"]
        ancho = parametros_cm["Ancho"]
        alto = parametros_cm["Alto"]
        volumen = sp.integrate(1, (x, 0, largo), (y, 0, ancho), (z, 0, alto))
        integral = "Integral triple rectangular de 1"
    elif figura == "Cilindro":
        radio = parametros_cm["Radio"]
        altura = parametros_cm["Altura"]
        volumen = sp.integrate(r, (theta, 0, 2 * sp.pi), (r, 0, radio), (z, 0, altura))
        integral = "Integral triple cilindrica con jacobiano r"
    elif figura == "Esfera":
        radio = parametros_cm["Radio"]
        volumen = sp.integrate(
            rho**2 * sp.sin(phi),
            (theta, 0, 2 * sp.pi),
            (phi, 0, sp.pi),
            (rho, 0, radio),
        )
        integral = "Integral triple esferica con jacobiano rho^2*sin(phi)"
    elif figura == "Semiesfera":
        radio = parametros_cm["Radio"]
        volumen = sp.integrate(
            rho**2 * sp.sin(phi),
            (theta, 0, 2 * sp.pi),
            (phi, 0, sp.pi / 2),
            (rho, 0, radio),
        )
        integral = "Integral triple esferica sobre media esfera"
    elif figura == "Cono":
        radio = parametros_cm["Radio"]
        altura = parametros_cm["Altura"]
        volumen = sp.integrate(
            r,
            (theta, 0, 2 * sp.pi),
            (r, 0, radio),
            (z, 0, altura * (1 - r / radio)),
        )
        integral = "Integral triple cilindrica con z entre 0 y H(1-r/R)"
    elif figura == "Paraboloide":
        radio = parametros_cm["Radio"]
        altura = parametros_cm["Altura"]
        volumen = sp.integrate(
            r,
            (theta, 0, 2 * sp.pi),
            (r, 0, radio),
            (z, 0, altura * (1 - (r**2 / radio**2))),
        )
        integral = "Integral triple cilindrica con z entre 0 y H(1-r^2/R^2)"
    else:
        raise ValueError("Figura no soportada.")

    return float(sp.N(volumen)), integral
