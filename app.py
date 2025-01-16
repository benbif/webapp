from flask import Flask, request, jsonify
from minio import Minio
import os

app = Flask(__name__)

# Configura MinIO
MINIO_URL = "127.0.0.1:9000"  # Cambia con l'IP del server se necessario
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "password"
BUCKET_NAME = "benedetto-storage"

client = Minio(
    MINIO_URL,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # Deve essere False per MinIO locale
)

# Controlla se il bucket esiste, altrimenti lo crea
if not client.bucket_exists(BUCKET_NAME):
    client.make_bucket(BUCKET_NAME)

@app.route('/')
def home():
    return "Benvenuto nella tua web app Flask con Blob Storage!"

# Endpoint per caricare file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Nessun file ricevuto"}), 400

    file = request.files['file']
    file_name = file.filename

    # Carica il file su MinIO
    client.put_object(
        BUCKET_NAME,
        file_name,
        file,
        length=-1,
        part_size=10 * 1024 * 1024
    )

    return jsonify({"message": f"File {file_name} caricato con successo!"})

# Endpoint per scaricare file
@app.route('/download/<file_name>', methods=['GET'])
def download_file(file_name):
    url = client.presigned_get_object(BUCKET_NAME, file_name)
    return jsonify({"download_url": url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)