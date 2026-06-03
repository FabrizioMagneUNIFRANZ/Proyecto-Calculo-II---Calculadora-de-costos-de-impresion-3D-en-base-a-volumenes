# Calculadora de Costos de Impresión 3D para figuras regulares

Este proyecto es una herramienta interactiva desarrollada en Python para calcular el volumen de diversas figuras geométricas mediante integrales triples y estimar los costos asociados a la impresión 3D de dichas piezas.

## Características

- **Cálculo de Volumen Geométrico**: Utiliza la librería `sympy` para realizar cálculos precisos de volumen para:
  - Prisma Rectangular
  - Cilindro
  - Esfera
  - Semiesfera
  - Cono
  - Paraboloide
- **Estimación de Costos de Impresión**:
  - Soporte para múltiples materiales (PLA, ABS, PETG, Resinas).
  - Configuración de parámetros de impresión: porcentaje de relleno (ocupación), material extra para soportes y margen de desperdicio.
  - Cálculo de costo por tiempo de uso de la impresora (tarifa por hora).
- **Interfaz Gráfica (GUI)**: Desarrollada con `tkinter` para una experiencia de usuario sencilla e intuitiva.
- **Validación de Entradas**: Soporta expresiones matemáticas simples (como `pi/2`) en los campos de dimensiones.

## Estructura del Proyecto

- `calc-impresion-3d-v4.py`: Punto de entrada principal de la aplicación.
- `ui.py`: Define la interfaz gráfica y la lógica de interacción.
- `figuras.py`: Contiene las fórmulas y lógica para el cálculo de volúmenes.
- `costos.py`: Lógica para el cálculo de masa y costos finales.
- `validacion.py`: Funciones para validar y procesar las entradas del usuario.
- `resultados.py`: Maneja la ventana secundaria donde se muestran los resultados detallados.

## Requisitos

- Python 3.x
- Librerías listadas en `requirements.txt` (principalmente `sympy`).

## Instalación

1. Clona o descarga este repositorio.
2. Instala las dependencias necesarias:
   ```powershell
   pip install -r requirements.txt
   ```

## Uso

Para iniciar la aplicación, ejecuta el archivo principal:

```powershell
python calc-impresion-3d-v4.py
```

1. Selecciona la **Figura** que deseas calcular.
2. Ingresa las **Dimensiones** en la unidad seleccionada (mm, cm, m).
3. Configura los parámetros de **Material** y **Costos**.
4. Haz clic en **Calcular** para ver el desglose detallado del volumen, masa y precio estimado.
