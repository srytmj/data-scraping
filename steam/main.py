from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/panggil_fungsi_python', methods=['POST'])
def panggil_fungsi_python():
    data = request.get_json()
    input_nilai = data['inputNilai']
    
    # Panggil fungsi Python sesuai kebutuhan
    hasil_output = fungsi_python(input_nilai)
    
    return jsonify({'output': hasil_output})

# Contoh fungsi Python
def fungsi_python(nilai):
    # Manipulasi atau proses data di sini
    hasil = nilai * 2
    return hasil

if __name__ == '__main__':
    app.run()
