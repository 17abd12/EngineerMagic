from flask import Flask, render_template, request, jsonify, render_template_string, send_file
import os
from werkzeug.utils import secure_filename
from main import generate_chat_completion  # Ensure this can handle image input
from flask import Flask, render_template, abort
import subprocess
import random
import os
import re
import time


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Ensure this directory exists
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
OPENSCAD_EXECUTABLE_PATH = '/usr/local/bin/openscad'

app.secret_key = '12345678'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def process_text_and_image(input_text, image_file=None):
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(image_path)
        completion = generate_chat_completion(input_text, image_path=image_path)
    else:
        completion = generate_chat_completion(input_text)
    scad_code = completion
    return scad_code

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text_value = request.form['prompt']
        image_file = request.files.get('image', None)

        processed_text = process_text_and_image(text_value, image_file)
        no = random.randint(1,1000)
        model_directory = '/tmp'
        os.makedirs(model_directory, exist_ok=True)
        scad_path = f'/tmp/model{no}.scad'
        with open(scad_path,"w") as file:
            file.write(processed_text)
        print("generating File")
        flag=generate_stl(no)
        print(flag)
        if not flag:
            print("False")
            abort(500)
        
        parameters = extract_parameters(scad_path)
        data = {"processed_text":processed_text,"identifier":no,"parameters":parameters}
        return jsonify(data)
    
    else:
        return render_template('index.html',parameters={})




##ABD code
@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    update_parameters(data["parameters"],data["id"])
    flag=generate_stl(data["id"])
    print(flag)
    if not flag:
        print(flag)
        abort(500)
    return jsonify({"message": "Data received"})


##Creating a route for download file
@app.route('/download', methods=['GET'])
def download_file():
    identifier = request.args.get('identifier')
    if identifier:
        file_path = f'static/model/model{identifier}.scad'
    else:
        file_path = f'static/model/model0.scad'
    
    return send_file(file_path, as_attachment=True)

@app.route('/download-stl', methods=['GET'])
def download_stl_file():
    identifier = request.args.get('identifier')
    if identifier:
        file_path = f'static/model/model{identifier}.stl'
    else:
        file_path = f'static/model/model0.stl'
    
    return send_file(file_path, as_attachment=True)



def extract_parameters(filename):

    with open(filename, 'r') as file:
        content = file.read()
    pattern = re.compile(r'(\$\w+|\w+)\s*=\s*(\d+)\s*;')
    matches = pattern.findall(content)
    return {name: value for name, value in matches}

def update_parameters(new_params,identifier):
    SCAD_FILE = f'tmp/model{identifier}.scad'
    with open(SCAD_FILE, 'r') as file:
        content = file.readlines()
    pattern = re.compile(r'(\$\w+|\w+)\s*=\s*(\d+)\s*;')

    with open(SCAD_FILE, 'w') as file:
        for line in content:
            match = pattern.match(line)
            if match:
                name = match.group(1)
                if name in new_params:
                    line = f"{name} = {new_params[name]};\n"
            file.write(line)

def generate_stl(identifier,turn = 0):
    SCAD_FILE = f'/tmp/model{identifier}.scad'
    STL_FILE = f'/tmp/model{identifier}.stl'
    if not os.path.isfile(SCAD_FILE):
        abort(404, description="Model not found")

    try:
        # Run the subprocess with OpenSCAD
        result = subprocess.run(
            [
                OPENSCAD_EXECUTABLE_PATH,
                '-o', STL_FILE,
                SCAD_FILE,
                '--export-format=binstl',
                '--enable=manifold',
                '--enable=fast-csg',
                # '--enable=lazy-union',
                '--enable=roof',
            ],check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    except subprocess.CalledProcessError:
        print(turn)
        if  turn < 2: 
            return generate_stl(identifier,turn = turn+1)
        print("Error in subprocess")
        return False

    except subprocess.TimeoutExpired:
        print("Error: Process timed out.")
        return False
    return True


if __name__ == '__main__':
    app.run(debug=True)


