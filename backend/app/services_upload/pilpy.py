from PIL import Image, ImageDraw, ImageFont
import io
from astropy.io import fits
import numpy as np

def add_star_names(filename, image_bytes, stars):
    star_coordinates = {name: (x, y) for name, x, y in zip(stars['main_id'], stars['field_x'], stars['field_y'])}
    
    # Crear un objeto tipo archivo en memoria
    if filename.endswith('.fits'):
        buffer_binario = io.BytesIO(image_bytes)
        hdul = fits.open(buffer_binario)
        data = hdul[0].data
        data_min = data.min()
        data_max = data.max()
        normalized_data = 255 * (data - data_min) / (data_max - data_min)
        image_array_8bit = normalized_data.astype(np.uint8)
        hdul.close()
        pil_image = Image.fromarray(image_array_8bit)
        output_buffer = io.BytesIO()
        pil_image.save(output_buffer, "JPEG")
        image_bytes = output_buffer.getvalue()
        output_buffer.close()

    
    image_stream = io.BytesIO(image_bytes)

    # Abrir la imagen usando Pillow
    image = Image.open(image_stream)

    # Obtener las dimensiones de la imagen (originales)
    width, height = image.size
    img_size = {'width': width, 'height': height}

    # Convertir imagen para reducir paleta de colores
    image = image.convert('RGB')
    draw = ImageDraw.Draw(image)
    
    # Elegir una fuente (puedes ajustar el tamaño si es necesario)
    try:
        font = ImageFont.truetype("arial.ttf", 20)  # Intenta con Arial si está disponible
    except IOError:
        font = ImageFont.load_default()  # Usa fuente predeterminada si no está Arial

    # Definir el radio del círculo
    radius = 10
    # Dibujar los nombres y los círculos en las coordenadas especificadas
    for star_name, (x, y) in star_coordinates.items():
        # Dibujar un círculo alrededor de las coordenadas
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline="greenyellow", width=2)
        
        # Dibujar el nombre de la estrella
        draw.text((x + radius + 5, y - radius), star_name, fill="greenyellow", font=font)

    # Guardar la imagen con los nombres añadidos
    #image.save('image.jpg')

    img_bytes = io.BytesIO()
    image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_size, img_bytes, image

