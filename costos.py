def calcular_costos(volumen_geometrico_cm3, densidad, costo_material, ocupacion, soportes, desperdicio, tiempo, tarifa):
    volumen_material_cm3 = volumen_geometrico_cm3 * (ocupacion / 100.0)
    volumen_material_cm3 *= 1.0 + (soportes / 100.0)
    volumen_material_cm3 *= 1.0 + (desperdicio / 100.0)

    masa_g = volumen_material_cm3 * densidad
    costo_material_bs = masa_g * costo_material
    costo_tiempo_bs = tiempo * tarifa
    costo_total_bs = costo_material_bs + costo_tiempo_bs

    return {
        "volumen_material_cm3": volumen_material_cm3,
        "masa_g": masa_g,
        "costo_material_bs": costo_material_bs,
        "costo_tiempo_bs": costo_tiempo_bs,
        "costo_total_bs": costo_total_bs,
    }

