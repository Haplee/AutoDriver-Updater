# Analizador de Drivers para Windows

Este proyecto contiene una herramienta de línea de comandos desarrollada en Python para analizar el estado de los drivers en un sistema operativo Windows. El ejecutable identifica drivers que pueden estar desactualizados, detenidos o sin firmar, y genera un informe de texto.

La herramienta **no descarga ni instala drivers**, sino que actúa como un complemento a Windows Update, proporcionando una visión detallada para que el usuario pueda tomar decisiones informadas.

## Estructura del Proyecto

- `src/driver_analyzer.py`: El script principal de Python que contiene toda la lógica de análisis.
- `web/`: Carpeta que contiene la página web explicativa (`index.html` y `style.css`).
- `README.md`: Este archivo.

## Características

- **Análisis Detallado**: Ejecuta `driverquery /v` para obtener una lista completa de drivers, incluyendo su estado, fabricante, versión y fecha.
- **Verificación de Firmas**: Utiliza `driverquery /si` para identificar drivers que no están firmados digitalmente.
- **Informe Automático**: Genera un archivo `report.txt` con un resumen de los drivers que requieren atención.
- **Seguridad**: No modifica el sistema. Su función es únicamente de lectura y reporte.
- **Requisito de Administrador**: Verifica si se está ejecutando con los privilegios necesarios para acceder a la información del sistema.

## ¿Cómo Usarlo?

### Requisitos Previos

- Python 3.x
- El módulo `pyinstaller` si deseas compilar el ejecutable. Puedes instalarlo con:
  ```
  pip install pyinstaller
  ```

### Ejecutar el Script

Existen dos modos de ejecución:

**1. Análisis de Drivers (requiere administrador)**

1. Abre una terminal (PowerShell o CMD) **como administrador**.
2. Navega al directorio raíz del proyecto.
3. Ejecuta el script:
   ```
   python src/driver_analyzer.py
   ```
4. El análisis comenzará y los resultados se mostrarán en la consola. Al finalizar, encontrarás un archivo `report.txt` en el mismo directorio.

**2. Ver la Página de Ayuda (no requiere administrador)**

1. Abre una terminal normal.
2. Navega al directorio raíz del proyecto.
3. Ejecuta el script con el siguiente argumento:
   ```
   python src/driver_analyzer.py --view-web
   ```
4. Se abrirá la página web explicativa en tu navegador por defecto.

### Compilar el `.exe`

Para crear un ejecutable independiente que puedas distribuir, puedes usar `PyInstaller`.

1. Asegúrate de tener PyInstaller instalado.
2. Abre una terminal (no es necesario que sea como administrador para compilar).
3. Navega al directorio raíz del proyecto.
4. Ejecuta el siguiente comando:
   ```
   pyinstaller --onefile --console --name DriverAnalyzer src/driver_analyzer.py
   ```
   - `--onefile`: Empaqueta todo en un único archivo `.exe`.
   - `--console`: Asegura que la aplicación se ejecute en una ventana de consola, lo cual es necesario para ver la salida del script.
   - `--name DriverAnalyzer`: Asigna un nombre al ejecutable final.

5. Una vez finalizado el proceso, encontrarás el archivo `DriverAnalyzer.exe` dentro de la carpeta `dist`.

## Página Web Explicativa

El proyecto incluye una página web (`web/index.html`) que explica en detalle qué hace la herramienta, cómo funciona y las advertencias de seguridad. Es recomendable distribuir el enlace a esta página junto con el ejecutable para que los usuarios finales comprendan su propósito y limitaciones.

## Aviso Legal

Esta herramienta se proporciona "tal cual". El uso del programa es bajo la total responsabilidad del usuario. No se ofrecen garantías y el desarrollador no se hace responsable de ningún daño que pueda surgir de su uso.
