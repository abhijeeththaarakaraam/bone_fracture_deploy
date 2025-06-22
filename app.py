from flask import Flask, render_template, request
from predictions import predict
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_result = None
    fracture_result = None
    image_path = None

    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            prediction_result = predict(filepath)
            fracture_result = predict(filepath, prediction_result)
            image_path = filename

    return render_template("index.html", 
                           prediction=prediction_result, 
                           fracture=fracture_result, 
                           image=image_path)

if __name__ == '__main__':
    app.run(debug=True)
