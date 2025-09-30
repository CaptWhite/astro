import io
import zipfile
from astropy.io import fits
from astropy.table import Table
from PIL import Image
import numpy as np

def unzip(filename, zip_bytes):
  # 1.1 Usar BytesIO para tratar los bytes como un archivo
  buffer_zip = io.BytesIO(zip_bytes)
  ficheros_desencapsulados = {}

  with zipfile.ZipFile(buffer_zip, 'r') as archivo_zip:
    # 1.3 Obtener la lista de miembros y filtrar directorios
    nombres_en_zip = archivo_zip.namelist()
    nombres_ficheros = [name for name in nombres_en_zip if not name.endswith('/')]
            
    # 1.4 Leer el contenido de cada archivo y almacenarlo en el diccionario
    for nombre in nombres_ficheros:
       ficheros_desencapsulados[nombre] = archivo_zip.read(nombre)

    # Crear un iterador de las claves (los nombres de los ficheros)
    iterador_claves = iter(ficheros_desencapsulados)
    first_key = next(iterador_claves)
    second_key = next(iterador_claves)  

    if first_key.endswith('corr.fits'):
      corr_file_zip_buf = ficheros_desencapsulados[first_key]
      corr_file_zip_name = first_key
      image_file_zip_buf = ficheros_desencapsulados[second_key]
      image_file_zip_name = second_key
    else:
      corr_file_zip_buf = ficheros_desencapsulados[second_key]
      corr_file_zip_name = second_key
      image_file_zip_buf = ficheros_desencapsulados[first_key]
      image_file_zip_name = first_key

    # 2. Abrir el fichero FITS usando el buffer de memoria
    buffer_binario = io.BytesIO(corr_file_zip_buf)
    hdul = fits.open(buffer_binario)
    data = Table(hdul[1].data)
    df_corr = data.to_pandas()

    if image_file_zip_name.endswith('.fits'):
        buffer_binario = io.BytesIO(image_file_zip_buf)
        hdul = fits.open(buffer_binario)
        data = hdul[0].data
        # 3. Normaliza los datos a un rango de 0 a 255 (8 bits)
        data_min = data.min()
        data_max = data.max()
        normalized_data = 255 * (data - data_min) / (data_max - data_min)
        # Convierte el array normalizado a enteros sin signo de 8 bits
        image_array_8bit = normalized_data.astype(np.uint8)
        # Cierra el HDUList para liberar recursos
        hdul.close()
        # 4. Crea un objeto de imagen Pillow (PIL)
        pil_image = Image.fromarray(image_array_8bit)

        # Opción B: Guardar en un buffer de bytes (útil para web o API)
        output_buffer = io.BytesIO()
        pil_image.save(output_buffer, "JPEG")
        jpg_bytes = output_buffer.getvalue()
        output_buffer.close()
  
        image_file_zip_buf = jpg_bytes
        image_file_zip_name = image_file_zip_name.replace(".fits", ".jpg")
 

  return df_corr, image_file_zip_name, image_file_zip_buf