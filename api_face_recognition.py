import os
import subprocess
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from werkzeug import secure_filename

UPLOAD_FOLDER = '/root/uploads'
ALLOWED_EXTENSIONS = set(['.png', '.jpg', '.jpeg'])

def run(cmd):
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))


def face_searcher(filename):
    try:
        return run('python3 face_detection.py ' + UPLOAD_FOLDER + '/' + filename).decode('utf-8')
    except Exception as e:
        print('An error ocurred: ', e)


def allowed_file(filename):
    return os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS 


def remove_uploaded_file(filename):
    run('rm -f ' + UPLOAD_FOLDER + '/' + filename)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            has_face = face_searcher(filename)
            remove_uploaded_file(filename)
            if has_face:
                return jsonify({'hasFace': True})
            return jsonify({'hasFace': False})


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=8080, debug=True)
