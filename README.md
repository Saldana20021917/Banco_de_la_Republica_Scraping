# 📊 Scraper de Indicadores Económicos del Banco de la República
## 🧠 Descripción general
Este proyecto es un script en Python que automatiza la descarga de indicadores económicos desde el portal Suameca del Banco de la República de Colombia. Está diseñado para facilitar la recolección de datos estadísticos relevantes, permitiendo que el usuario seleccione categorías, indicadores y rangos de fechas desde una interfaz interactiva en consola.

## ⚙️ ¿Qué hace el script?
El script simula la navegación por el sitio web oficial del Banco de la República, accediendo automáticamente a las categorías de datos, seleccionando indicadores y descargando archivos en formato .xlsx. Todo esto se realiza sin intervención manual en el navegador, lo que lo convierte en una herramienta útil para ahorrar tiempo y reducir errores en la recolección de información económica.

### Entre sus funcionalidades principales se encuentran:
- Selección interactiva de categorías e indicadores.
- Ingreso personalizado del rango de fechas.
- Descarga automática del archivo Excel.
- Renombrado dinámico y limpio del archivo descargado.
- Almacenamiento organizado en una carpeta local (downloads/).

## 📂 Categorías disponibles
1. Precios e inflación
2. Reservas internacionales y operaciones del Banco
3. Tasas de interés y agregados monetarios
4. Actividad económica, mercado laboral y salarios
5. Sector público y deuda

Cada una incluye varios indicadores clave como inflación, PIB, tasa de desempleo, salario mínimo, reservas internacionales, entre otros.

## 🛠 Tecnologías utilizadas
- Python 3
- Selenium
- WebDriver Manager
- Google Chrome
- Módulo unicodedata (para limpiar y normalizar nombres de archivo)

## ▶️ ¿Cómo usar este scraper?

Este script permite automatizar la descarga de indicadores económicos desde el sitio web del Banco de la República de Colombia.


### 🧱 Paso 1: Requisitos previos

Antes de comenzar, asegúrese de tener instalado:

- ✅ [Python 3.7 o superior](https://www.python.org/downloads/)
- ✅ Google Chrome
- ✅ pip (el gestor de paquetes de Python, incluido con Python)


### 📦 Paso 2: Instalar las librerías necesarias

Abra una terminal y ejecute el siguiente comando:

```bash
pip install selenium webdriver-manager
```
### ⚙️ Paso 3: Ejecutar el scraper

- Abra la terminal o Vscode.
- Navegue hasta la carpeta donde se encuentra el archivo scraper.py

### 💬 Paso 4: Usar la interfaz interactiva en consola
Durante la ejecución, el script le pedirá:

- Seleccionar una categoría (por número).
- Elegir uno o varios indicadores, separados por comas (ejemplo: 1,2,3).
- Ingresar la fecha de inicio y la fecha de fin en formato DD/MM/AAAA.
- 
#### 📌 Ejemplo de entrada en consola:
> Ingresa el número de la categoría: 2

> Ingresa el(los) número(s) del/los indicador(es), separados por comas: 1,2

> Fecha de inicio (DD/MM/AAAA): 01/01/2018

> Fecha de fin (DD/MM/AAAA): 30/12/2023

### 📥 Paso 5: Descarga automática
Una vez completados los pasos anteriores:
- El navegador Google Chrome se abrirá automáticamente.
- El script seleccionará los indicadores en el sitio web del Banco de la República.
- El archivo .xlsx se descargará automáticamente y será renombrado según los indicadores y fechas.

#### 📂 Ubicación del archivo descargado:
El archivo se guardará en la carpeta de Descargas del sistema operativo

## 📌 Recomendaciones
- No cierres el navegador mientras el script esté en ejecución.

- Si no se encuentra un indicador, el script lo notificará.

- Los archivos descargados se guardarán en la carpeta downloads/.

## 👤 Autor
Desarrollado por Jesus David Saldaña Arroyo

**Contacto:** saldanajesusdavid@gmail.com

**LinkedIn:** [Jesús Saldaña](https://www.linkedin.com/in/jesus-david-saldaña-arroyo-41b43718a)
