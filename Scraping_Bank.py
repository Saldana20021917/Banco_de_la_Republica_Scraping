import os
import time
import unicodedata
import sys
import platform
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# =========================
# Categorías y subcategorías
# =========================
categorias = {
    "1": {"nombre": "Precios e inflación","subcategoria_xpath": {
            "1": "//span[contains(text(),'Inflación al consumidor')]",
            "2": "//span[contains(text(),'Inflación al consumidor')]",
            "3": "//span[contains(text(),'Inflación al consumidor')]",
            "4": "//span[contains(text(),'Inflación al consumidor')]",
            "5": "//span[contains(text(),'Índices de precios al productor')]"},
        "indicadores": {
            "1": "Inflación total",
            "2": "Inflación total, anual",
            "3": "Índice de Precios al Consumidor",
            "4": "Índice de precios al consumidor (IPC): de alimentos",
            "5": "Índice de Precios del Productor (IPP)"}},

    "2": {"nombre": "Operaciones del Banco en los mercados y reservas internacionales","subcategoria_xpath": {
            "1": "//span[contains(text(),'Reservas internacionales')]",
            "2": "//span[contains(text(),'Reservas internacionales')]"},
        "indicadores": {
            "1": "Reservas internacionales netas",
            "2": "Reservas internacionales brutas"}},

    "3": {"nombre": "Tasas de interés y sector financiero","subcategoria_xpath": {
            "1": "//span[contains(text(),'Agregados monetarios')]",
            "2": "//span[contains(text(),'Agregados monetarios')]",
            "3": "//span[contains(text(),'Agregados monetarios')]",
            "4": "//span[contains(text(),'Agregados monetarios')]",
            "5": "//span[contains(text(),'Agregados monetarios')]",
            "6": "//span[contains(text(),'Agregados monetarios')]",
            "7": "//span[contains(text(),'Posición de Encaje y Pasivos Sujetos a Encaje')]",
            "8": "//span[contains(text(),'Posición de Encaje y Pasivos Sujetos a Encaje')]"},
        "indicadores": {
            "1": "Base monetaria, mensual",
            "2": "Base monetaria, semanal",
            "3": "Efectivo, mensual",
            "4": "Efectivo, semanal",
            "5": "Reserva Bancaria, mensual",
            "6": "Reserva Bancaria, semanal",
            "7": "Encaje disponible diario",
            "8": "Encaje efectivo en caja"}},

    "4": {"nombre": "Actividad económica, mercado laboral y cuentas financieras","subcategoria_xpath": {
            "1": "//span[contains(text(),'Producto interno bruto')]",
            "2": "//span[contains(text(),'Producto interno bruto')]",
            "3": "//span[contains(text(),'Producto interno bruto')]",
            "4": "//span[contains(text(),'Producto interno bruto')]",
            "5": "//span[contains(text(),'Producto interno bruto')]",
            "6": "//span[contains(text(),'Producto interno bruto')]",
            "7": "//span[contains(text(),'Producto interno bruto')]",
            "8": "//span[contains(text(),'Producto interno bruto')]",
            "9": "//span[contains(text(),'Producto interno bruto')]",
            "10": "//span[contains(text(),'Producto interno bruto')]",
            "11": "//span[contains(text(),'Mercado laboral')]",
            "12": "//span[contains(text(),'Mercado laboral')]",
            "13": "//span[contains(text(),'Salarios')]",
            "14": "//span[contains(text(),'Salarios')]"},
        "indicadores": {
            "1": "Crecimiento PIB nominal, Anual, metodología: 2015",
            "2": "Crecimiento PIB real, Anual, base: 2015",
            "3": "Exportaciones, nominal",
            "4": "Exportaciones, real",
            "5": "Formación bruta de capital, nominal",
            "6": "Formación bruta de capital, real",
            "7": "Importaciones, nominal",
            "8": "Importaciones, real",
            "9": "Producto Interno Bruto (PIB) nominal, Anual, metodología: 2015",
            "10": "Producto Interno Bruto (PIB) real, Anual, base: 2015",
            "11": "Tasa de desempleo - total nacional",
            "12": "Tasa de ocupación - total nacional",
            "13": "Salario mínimo diario",
            "14": "Salario mínimo mensual"}},

    "5": {"nombre": "Sector público y deuda pública","subcategoria_xpath": {
            "1": "//span[contains(text(),'Deuda pública')]",
            "2": "//span[contains(text(),'Deuda pública')]"},
        "indicadores": {
            "1": "BID-ASK Spread TES Pesos",
            "2": "BID-ASK Spread TES UVR"}}}

def get_download_folder():
    sistema = platform.system()

    if sistema == "Windows":
        try:
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                downloads, _ = winreg.QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')
                return downloads
        except Exception as e:
            print(f"⚠️ Error accediendo al registro de Windows: {e}")
            return os.path.join(os.path.expanduser("~"), "Downloads")  # Fallback

    else:  # macOS o Linux
        try:
            from platformdirs import user_download_dir
            return user_download_dir()
        except ImportError:
            print("⚠️ La librería platformdirs no está instalada. Usando ruta por defecto.")
            return os.path.join(os.path.expanduser("~"), "Downloads") 


# Directorio de descarga
download_dir = get_download_folder()
os.makedirs(download_dir, exist_ok=True)

# Renombrar archivo descargado
def rename_latest_download(new_name):
    while any(f.endswith(".crdownload") for f in os.listdir(download_dir)):
        time.sleep(1)

    files = [f for f in os.listdir(download_dir) if f.endswith('.xlsx')]
    if not files:
        print("⚠️ No se encontró archivo descargado para renombrar.")
        return

    latest = max([os.path.join(download_dir, f) for f in files], key=os.path.getctime)
    
    # Si ya existe el archivo, busca un nombre alternativo
    name, ext = os.path.splitext(new_name)
    target = os.path.join(download_dir, new_name)
    contador = 1
    while os.path.exists(target):
        target = os.path.join(download_dir, f"{name} ({contador}){ext}")
        contador += 1

    os.rename(latest, target)
    print(f"✅ Archivo renombrado como: {os.path.basename(target)}")


# Generar nombre para archivo con fechas
def limpiar_texto(texto):
    # Elimina tildes, ñ → n, y caracteres especiales
    texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
    texto = texto.replace("(", "").replace(")", "").replace(":", "").replace(",", "")
    return texto

def generar_chucho(indicadores_seleccionados, fecha_inicio, fecha_fin, download_dir="."):
    if len(indicadores_seleccionados) == 1:
        nombre_base = limpiar_texto(indicadores_seleccionados[0]).replace(" ", "_").lower()
    else:
        palabras_clave = []
        for indicador in indicadores_seleccionados[:5]:  # Máximo 5 indicadores
            palabras = limpiar_texto(indicador).split()
            if palabras:
                palabras_clave.append(palabras[0][:3].lower())
        
        nombre_base = "_".join(palabras_clave)

    nombre_base = f"{nombre_base}_{fecha_inicio[-4:]}_{fecha_fin[-4:]}"
    
    if len(nombre_base) > 100:
        print("⚠️ Advertencia: el nombre fue recortado para no superar 100 caracteres.")
        nombre_base = nombre_base[:100]

    chucho = f"{nombre_base}.xlsx"
    contador = 1
    while os.path.exists(os.path.join(download_dir, chucho)):
        chucho = f"{nombre_base} ({contador}).xlsx"
        contador += 1

    return chucho

# =========================
# Ciclo de descarga
# =========================
while True:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True})

    print("\n Selecciona la categoría:")
    for cod, info in categorias.items():
        print(f"{cod}. {info['nombre']}")
    categoria_opcion = input("> Ingresa el número de la categoría: ").strip()
    while categoria_opcion not in categorias:
        print("❌ Categoría inválida. Intenta de nuevo.")
        categoria_opcion = input("> Ingresa el número de la categoría: ").strip()

    categoria = categorias[categoria_opcion]
    print(f"📊 Indicadores disponibles en '{categoria['nombre']}':")
    for cod, nombre in categoria["indicadores"].items():
        print(f"{cod}. {nombre}")

    opciones = input("> Ingresa el(los) número(s) del/los indicador(es), separados por comas: ").split(",")
    opciones = [op.strip() for op in opciones if op.strip() in categoria["indicadores"]]
    if not opciones:
        print("⚠️ No seleccionaste indicadores válidos. Intenta de nuevo.")
        continue

    # Fechas personalizadas
    print("📅 Ingresa las fechas que deseas descargar:")
    fecha_inicio = input("🟢 Fecha de inicio (DD/MM/AAAA): ").strip()
    fecha_fin = input("🔴 Fecha de fin (DD/MM/AAAA): ").strip()
    if not fecha_inicio or not fecha_fin:
        print("⚠️ Fechas no válidas. Se usarán las predeterminadas.")
        fecha_inicio = "01/01/2015"
        fecha_fin = "30/05/2025"

    with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
        wait = WebDriverWait(driver, 20)
        driver.get("https://suameca.banrep.gov.co/buscador-de-series/#/")
        wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(),'{categoria['nombre']}')]"))).click()

        indicadores_por_subcat = defaultdict(list)
        for op in opciones:
            subcat_xpath = categoria["subcategoria_xpath"][op]
            indicadores_por_subcat[subcat_xpath].append(op)

        for subcat_xpath, ops_en_subcat in indicadores_por_subcat.items():
            try:
                elemento = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, subcat_xpath)))
                elemento.click()
            except:
                print(f"No se pudo hacer clic en subcategoría: {subcat_xpath}")
                continue

            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//table//tbody//tr")))
                filas = driver.find_elements(By.XPATH, "//table//tbody//tr")
            except:
                print("No se cargaron las filas de la tabla.")
                continue

            wait.until(EC.presence_of_element_located((By.XPATH, "//table//tbody//tr")))
            filas = driver.find_elements(By.XPATH, "//table//tbody//tr")

            for op in ops_en_subcat:
                nombre_indicador = categoria["indicadores"][op]
                encontrado = False
                for i, fila in enumerate(filas, 1):
                    if nombre_indicador.lower() in fila.text.lower():
                        print(f"✅ Indicador '{nombre_indicador}' encontrado en fila {i}")
                        icon = fila.find_element(By.XPATH, ".//img[@title='Agregar al carrito de series']")
                        driver.execute_script("arguments[0].scrollIntoView(true);", icon)
                        icon.click()
                        encontrado = True
                        break
                if not encontrado:
                    print(f"❌ No se encontró el indicador '{nombre_indicador}'")

        # Fechas dinámicas
        carrito_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[contains(@src,'shopping_cart_series_8')]")))
        carrito_icon.click()
        time.sleep(1)

        inputs = driver.find_elements(By.CSS_SELECTOR, "p-calendar input")
        for i, fecha in enumerate([fecha_inicio, fecha_fin]):
            inputs[i].click()
            time.sleep(0.5)
            inputs[i].send_keys(Keys.CONTROL + "a")
            inputs[i].send_keys(Keys.BACKSPACE)
            inputs[i].send_keys(fecha)
            inputs[i].send_keys(Keys.ENTER)
            time.sleep(1)

        driver.find_element(By.TAG_NAME, "body").click()
        time.sleep(1)

        # Descargar
        carrito_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[contains(@src,'shopping_cart_series_8')]")))
        carrito_icon.click()
        time.sleep(2)
        boton_descarga = wait.until(EC.element_to_be_clickable((By.XPATH, "//img[contains(@src,'shopping_cart_exportar_excel.svg')]")))
        boton_descarga.click()
        time.sleep(5)

        indicadores_seleccionados = [categoria["indicadores"][op] for op in opciones]
        chucho = generar_chucho(indicadores_seleccionados, fecha_inicio, fecha_fin)
        rename_latest_download(chucho)

    seguir = input("\n🔁 ¿Deseas descargar más indicadores? (si/no): ").strip().lower()
    if seguir != "si":
        print("👋 Programa finalizado. ¡Hasta pronto!")
        break
