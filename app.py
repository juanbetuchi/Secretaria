from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import uuid
from PIL import Image
from rembg import remove

app = Flask(__name__)

# Carpeta para guardar las fotos
CARPETA_FOTOS = os.path.join('static', 'fotos')
os.makedirs(CARPETA_FOTOS, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tomar_foto', methods=['POST'])
def tomar_foto():
    foto_data = request.files.get('foto')
    if not foto_data:
        return jsonify({'error': 'No se recibió foto'}), 400

    nombre_unico = f"{uuid.uuid4()}.png"
    ruta_foto = os.path.join(CARPETA_FOTOS, nombre_unico)
    foto_data.save(ruta_foto)

    # Procesar la foto para remover fondo usando rembg
    with open(ruta_foto, "rb") as f:
        input_data = f.read()
    output_data = remove(input_data)
    ruta_procesada = os.path.join(CARPETA_FOTOS, f"procesada_{nombre_unico}")
    with open(ruta_procesada, "wb") as f:
        f.write(output_data)

    # Normalizar la ruta para URL (reemplazar '\' por '/')
    ruta_foto_normalizada = ruta_procesada.replace('\\', '/')

    return jsonify({
        'foto_url': f"/{ruta_foto_normalizada}",
        'nombre_foto': nombre_unico
    })

# Ruta para servir las fotos procesadas (si usas static ya lo sirve automáticamente)
# Pero si necesitás una ruta explícita:
@app.route('/static/fotos/<filename>')
def fotos(filename):
    return send_from_directory(CARPETA_FOTOS, filename)

if __name__ == "__main__":
    app.run(debug=True)
