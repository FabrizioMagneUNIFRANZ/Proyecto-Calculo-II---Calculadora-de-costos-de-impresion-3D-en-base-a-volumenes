# Calculadora de costos de Impresión 3D

App de escritorio para estimar costos de impresión 3D. Calcula el volumen exacto de figuras geométricas utilizando integrales (vía `sympy`) y genera una vista previa 3D (`matplotlib`), aplicando luego parámetros reales de impresión (relleno, soportes, desperdicio y costo de máquina).

## Módulos
* `calc-impresion-3d.py`: Lanzador principal.
* `ui.py`: Interfaz de usuario (`tkinter`).
* `figuras.py`: Catálogo de figuras e integrales de volumen.
* `costos.py`: Estimación de material y costo total.
* `resultados.py`: Ventana de resultados y gráfico 3D.
* `validacion.py`: Conversión de unidades y seguridad.

## Historial aportes integrantes
Brayan Pacheco:
* Funciones iniciales para integrales dobles y triples en Python
* Definición de funciones para figuras geométricas en Python
* Esquema inicial de UI del primer prototipo
* Obtención de costos aproximados de materiales de impresión (filamentos) y costos de operación

Fabrizio Magne:
* Programación de primer, segundo, tercer y cuarto prototipo (v1, v2, v3, v4)
* Definición de graficación de las figuras geométricas en R3 (matplotlib)
* Definición de parámetros adicionales para el cálculo de costos de una impresión (relleno, soportes, desperdicio, horas estimadas)
* Definición del modelo matemático para las figuras y las coordenadas a usar


## Instalaciones adicionales para uso:
```bash
pip install sympy matplotlib numpy
python calc-impresion-3d.py
```
