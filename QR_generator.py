"""
=============================
     GENERADOR DE QR (v2)
=============================

Autor: Art-Phy
Descripción:
  Programa que genera códigos QR personalizados con opción de añadir un logo
  centrado en el código. Permite introducir texto o URLs, arrastrar archivos
  directamente a la terminal y elegir la ubicación de guardado del PNG.

Mejoras respecto a la versión anterior:
- Interfaz interactiva con inputs en consola.
- Posibilidad de arrastrar archivos (QR o logo).
- Validación y normalización de rutas (acepta carpetas).
- Nombres automáticos si no se especifica archivo.
- Limpieza de pantalla entre ejecuciones.
- Código modular y comentado.
"""

import os
import sys
import shlex
import datetime
import qrcode
from pathlib import Path
from PIL import Image


def limpiar_ruta_entrada(ruta: str) -> list[str]:
    """
    Limpia rutas introducidas o arrastradas en la terminal.
    Si el usuario arrastra un archivo, macOS/Linux agregan comillas.
    Ejemplo: '/Users/arturo/Desktop/logo.png'
    """
    try:
        return shlex.split(ruta)
    except ValueError:
        return [ruta.strip()]


def limpiar_pantalla():
    """Limpia la pantalla según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def normalizar_ruta_salida(ruta_usuario: str) -> str:
    """
    Normaliza la ruta de salida que el usuario ha introducido.

    Comportamiento:
      - Si ruta_usuario es una carpeta existente -> crea nombre automático dentro.
      - Si ruta_usuario no tiene extensión .png -> la añade.
      - Si ruta no existe, se crearán las carpetas necesarias al guardar.
      - Si no se introduce nada, se guarda en la carpeta actual.
    """
    ruta_usuario = ruta_usuario.strip()
    if not ruta_usuario:
        base = Path.cwd() / f"qr_{datetime.datetime.now():%Y%m%d_%H%M%S}.png"
        return str(base)

    partes = limpiar_ruta_entrada(ruta_usuario)
    ruta = Path(partes[0]) if partes else Path(ruta_usuario)

    # Si el usuario pasó un directorio existente
    if ruta.exists() and ruta.is_dir():
        nombre = f"qr_{datetime.datetime.now():%Y%m%d_%H%M%S}.png"
        return str(ruta / nombre)

    # Si termina con / o \ (directorio)
    if ruta.as_posix().endswith(os.sep):
        nombre = f"qr_{datetime.datetime.now():%Y%m%d_%H%M%S}.png"
        return str(ruta / nombre)

    # Si no tiene extensión .png, se la añadimos
    if ruta.suffix.lower() != ".png":
        ruta = ruta.with_suffix(".png")

    return str(ruta)


def generar_qr(data: str, logo_path: str | None, salida_path: str):
    """
    Genera el código QR con las opciones indicadas.

    data: texto o URL que contendrá el QR.
    logo_path: ruta opcional a una imagen para colocar en el centro.
    salida_path: ruta donde se guardará el PNG final.
    """
    # Creamos el objeto QR configurado
    qr = qrcode.QRCode(version=8, box_size=7, border=3)
    qr.add_data(data)
    qr.make(fit=True)

    # Generamos la imagen base
    img = qr.make_image(fill_color='black', back_color='white').convert('RGB')

    # Si se proporcionó logo, lo procesamos
    if logo_path:
        try:
            logo = Image.open(logo_path)
            logo_size = 120
            logo = logo.resize((logo_size, logo_size))

            # Si el logo tiene canal alfa (transparencia), usamos máscara
            if logo.mode in ('RGBA', 'LA') or (logo.mode == 'P' and 'transparency' in logo.info):
                mask = logo.split()[3]
            else:
                mask = None

            # Centramos el logo en el QR
            qr_width, qr_height = img.size
            logo_position = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

            img.paste(logo, logo_position, mask)
        except Exception as e:
            print(f"⚠️ No se pudo añadir el logo: {e}")

    # Creamos carpeta si no existe
    salida_final = Path(salida_path)
    salida_final.parent.mkdir(parents=True, exist_ok=True)

    # Guardamos la imagen final
    img.save(salida_final)
    print(f"✅ QR generado correctamente en: {salida_final}")


def solicitar_datos_interactivo() -> tuple[str, str | None, str]:
    """
    Pide al usuario los datos necesarios: contenido del QR, logo opcional y ruta de salida.
    Soporta arrastrar rutas y normaliza la salida.
    """
    print("\n=== GENERADOR DE QR (interactivo) ===\n")
    data = input("Introduce el texto o la URL para el QR: ").strip()
    if not data:
        raise ValueError("No has introducido datos para el QR.")

    print("\n(Arrastra aquí el archivo del logo si quieres usar uno, o pulsa Enter para omitir)")
    entrada_logo = input("Logo (opcional): ").strip()
    logos = limpiar_ruta_entrada(entrada_logo)
    logo_path = logos[0] if logos else None

    print("\nIntroduce la ruta de salida del PNG (ej: /Users/tuusuario/Desktop/qr.png)")
    print("También puedes arrastrar una carpeta (ej: /Users/tuusuario/Desktop/) y se creará el archivo automáticamente.")
    salida_raw = input("Salida: ").strip()

    salida_normalizada = normalizar_ruta_salida(salida_raw)
    return data, logo_path, salida_normalizada


def main():
    """
    Bucle principal del programa. Permite generar varios QR seguidos.
    """
    while True:
        limpiar_pantalla()
        try:
            data, logo_path, salida = solicitar_datos_interactivo()
            generar_qr(data, logo_path, salida)
        except Exception as e:
            print(f"\n❌ Ha ocurrido un error: {e}")

        opcion = input("\n¿Quieres generar otro QR? (s/n): ").lower().strip()
        if opcion != "s":
            print("\n👋 Gracias por usar el Generador de QR. ¡Hasta pronto!\n")
            break


if __name__ == "__main__":
    main()


