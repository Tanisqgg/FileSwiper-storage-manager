from flask import Flask, request, jsonify, render_template
import os
import time
from main import list_old_files, find_duplicates, move_to_trash, undo_last_action

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/scan', methods=['POST'])
def scan_files():
    data = request.get_json()
    directory = data.get('directory', 'C:\\')
    days_unused = int(data.get('days_unused', 365))

    # Get old files using your scanning function
    old_files = list_old_files(directory, days_unused=days_unused)
    duplicates = find_duplicates(old_files)

    # Format the old files with additional details
    files_list = [{
        'file_path': path,
        'size': size,
        'last_accessed': time.ctime(os.stat(path).st_atime)
    } for path, size in old_files]

    duplicates_list = []
    for (size, name), paths in duplicates.items():
        duplicates_list.append({
            'file_name': name,
            'size': size,
            'copies': paths
        })

    return jsonify({
        'old_files': files_list,
        'duplicates': duplicates_list
    })


@app.route('/api/delete', methods=['POST'])
def delete_file():
    data = request.get_json()
    file_path = data.get('file_path')
    trash_folder = os.path.join(os.path.dirname(file_path), "Trash")
    try:
        move_to_trash(file_path, trash_folder)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500


@app.route('/api/undo', methods=['POST'])
def undo_action():
    try:
        undo_last_action()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
