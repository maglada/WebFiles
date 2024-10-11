from flask import Flask, render_template, request, jsonify, abort, send_file
import os
import mimetypes

app = Flask(__name__)

@app.route('/')
@app.route('/<path:subpath>')
def explore(subpath=''):
    base_path = os.path.expanduser('~')  # Start from the user's home directory
    full_path = os.path.join(base_path, subpath)
    
    if not os.path.exists(full_path):
        abort(404)
    
    if os.path.isfile(full_path):
        return send_file(full_path)
    
    files = get_directory_contents(full_path)
    
    return render_template('explorer.html', files=files, current_path=subpath)

@app.route('/add_file', methods=['POST'])
def add_file():
    base_path = os.path.expanduser('~')
    current_path = request.form.get('current_path', '')
    file = request.files.get('file')
    
    if file:
        filename = file.filename
        full_path = os.path.join(base_path, current_path, filename)
        file.save(full_path)
        return jsonify({'status': 'success', 'message': f'File {filename} uploaded successfully'})
    return jsonify({'status': 'error', 'message': 'No file uploaded'})

@app.route('/create_file', methods=['POST'])
def create_file():
    base_path = os.path.expanduser('~')
    current_path = request.form.get('current_path', '')
    filename = request.form.get('filename', '')
    content = request.form.get('content', '')
    
    if filename:
        full_path = os.path.join(base_path, current_path, filename)
        with open(full_path, 'w') as f:
            f.write(content)
        return jsonify({'status': 'success', 'message': f'File {filename} created successfully'})
    return jsonify({'status': 'error', 'message': 'No filename provided'})

@app.route('/preview/<path:filepath>')
def preview_file(filepath):
    base_path = os.path.expanduser('~')
    full_path = os.path.join(base_path, filepath)
    
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        abort(404)
    
    mime_type, _ = mimetypes.guess_type(full_path)
    
    if mime_type and mime_type.startswith('text/'):
        with open(full_path, 'r') as file:
            content = file.read()
        return jsonify({'type': 'text', 'content': content})
    elif mime_type and mime_type.startswith('image/'):
        return jsonify({'type': 'image', 'src': f'/download/{filepath}'})
    else:
        return jsonify({'type': 'unsupported'})

@app.route('/download/<path:filepath>')
def download_file(filepath):
    base_path = os.path.expanduser('~')
    full_path = os.path.join(base_path, filepath)
    
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        abort(404)
    
    return send_file(full_path, as_attachment=True)

def get_directory_contents(path):
    files = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        files.append({
            'name': item,
            'is_dir': os.path.isdir(item_path),
            'size': os.path.getsize(item_path) if os.path.isfile(item_path) else None
        })
    return files

if __name__ == '__main__':
    app.run(debug=True)
