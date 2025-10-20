from astropy.io import fits
import numpy as np
import os

def eliminar_fila_fits(nombre_entrada, nombre_salida, indice_fila_a_eliminar):
    """
    Lee un archivo FITS, elimina una fila de la tabla de datos
    y guarda el resultado en un nuevo archivo FITS.

    Parámetros:
    - nombre_entrada (str): Nombre del archivo FITS original (ej. 'corr.fits').
    - nombre_salida (str): Nombre del nuevo archivo FITS (ej. 'corr_mod.fits').
    - indice_fila_a_eliminar (int): El índice basado en 0 de la fila que se va a eliminar.
    """
    print(f"Abriendo archivo: {nombre_entrada}")
    
    try:
        # 1. Abrir el archivo FITS
        with fits.open('./batch/eliminar_fila_corr.fits') as hdul:
            
            # 2. Identificar la extensión de la tabla (HDU)
            # Los archivos FITS de astrometry.net (corr.fits) suelen tener la tabla en la primera 
            # o segunda extensión (índice 1) si la primera es la HDU primaria vacía.
            # Buscamos la primera extensión que sea una BinTableHDU.
            data_hdu = None
            for hdu in hdul:
                if isinstance(hdu, fits.BinTableHDU) or isinstance(hdu, fits.TableHDU):
                    data_hdu = hdu
                    break

            if data_hdu is None:
                print("Error: No se encontró ninguna extensión de tabla de datos en el archivo FITS.")
                return

            # 3. Acceder a los datos de la tabla
            datos_originales = data_hdu.data
            
            num_filas = len(datos_originales)
            print(f"Tabla de datos encontrada con {num_filas} filas.")

            # 4. Validar el índice de la fila
            if not (0 <= indice_fila_a_eliminar < num_filas):
                print(f"Error: El índice '{indice_fila_a_eliminar}' está fuera del rango [0, {num_filas - 1}].")
                return

            # 5. Eliminar la fila usando indexing de NumPy
            # Creamos una máscara booleana: True para las filas que queremos CONSERVAR
            mascara_conservar = np.ones(num_filas, dtype=bool)
            mascara_conservar[indice_fila_a_eliminar] = False
            
            datos_modificados = datos_originales[mascara_conservar]
            
            print(f"Fila {indice_fila_a_eliminar} eliminada. Nueva tabla con {len(datos_modificados)} filas.")
            
            # 6. Crear una nueva extensión de tabla (HDU) con los datos modificados
            # Se mantienen las cabeceras y definiciones de columnas de la HDU original
            nueva_hdu = fits.BinTableHDU(data=datos_modificados, header=data_hdu.header)
            
            # 7. Crear una nueva lista de HDUs
            # Se copian todas las HDUs originales, pero se reemplaza la tabla modificada
            hdul_modificado = fits.HDUList([hdul[0]]) # Siempre incluimos la PrimaryHDU

            # Volvemos a añadir el resto de HDUs, reemplazando la de la tabla.
            for hdu in hdul[1:]:
                if hdu is data_hdu:
                    hdul_modificado.append(nueva_hdu)
                else:
                    hdul_modificado.append(hdu)

            # 8. Guardar el nuevo archivo FITS
            if os.path.exists(nombre_salida):
                os.remove(nombre_salida)
                
            hdul_modificado.writeto(nombre_salida)
            print(f"Archivo modificado guardado exitosamente como: {nombre_salida}")
            
    except FileNotFoundError:
        print(f"Error: El archivo de entrada '{nombre_entrada}' no fue encontrado.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# --------------------------------------------------------------------------------
# EJEMPLO DE USO:
# --------------------------------------------------------------------------------

# Define el índice de la fila que quieres eliminar (ej. la quinta fila)
indice_a_quitar = 2 # Recuerda: Python usa índice base 0

# Define los nombres de los archivos
archivo_entrada = './batch/eliminar_fila_corr.fits'
archivo_salida =  './batch/eliminar_fila_corr_mod.fits'

# ***NOTA: Asegúrate de que el archivo 'corr.fits' existe en el mismo directorio***
# Si el archivo 'corr.fits' no existe, la función devolverá un error.

# Llamar a la función
eliminar_fila_fits(archivo_entrada, archivo_salida, indice_a_quitar)

# ***Descomenta la línea de arriba para ejecutar la función.***