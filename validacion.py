import sympy as sp

FACTORES_LONGITUD_CM = {"mm": 0.1, "cm": 1.0, "m": 100.0}
LOCALES_NUMERICOS = {"pi": sp.pi, "E": sp.E}

def evaluar_real(texto, nombre, permitir_cero=False):
    texto = texto.strip()
    if not texto:
        raise ValueError(f"{nombre} no puede estar vacio.")
    try:
        expresion = sp.sympify(texto, locals=LOCALES_NUMERICOS)
    except (sp.SympifyError, TypeError) as exc:
        raise ValueError(f"{nombre} no es un valor valido.") from exc

    valor = sp.N(expresion)
    if valor.free_symbols or valor.has(sp.I):
        raise ValueError(f"{nombre} debe ser un numero real.")

    valor_float = float(valor)
    if permitir_cero:
        if valor_float < 0:
            raise ValueError(f"{nombre} no puede ser negativo.")
    elif valor_float <= 0:
        raise ValueError(f"{nombre} debe ser mayor que cero.")

    return valor_float
