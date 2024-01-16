import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from utils.data_manager import DataManager

# TODO: make these arguments you pass in
IMAGES_BASE_PATH="/Users/melanie.hanna/basic_annotation_tool/images/"
METADATA_PATH="/Users/melanie.hanna/basic_annotation_tool/metadata/test_metadata.csv"
smart_sort = False

data_manager = DataManager(METADATA_PATH, IMAGES_BASE_PATH, smart_sort)

app = Flask(__name__)

@app.route('/images/<path:filename>')
def custom_static(filename):
    return send_from_directory(IMAGES_BASE_PATH, filename)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'change_label':
            data_manager.change_label(request.form.get('new_label'))
        elif action == 'use_predicted':
            data_manager.use_predicted_label()
        elif action == 'next':
            data_manager.next_image()
        elif action == 'previous':
            data_manager.previous_image()
        elif action == 'delete':
            data_manager.delete_image()
        elif action == 'done':
            data_manager.save_changes()
            return redirect(url_for('index'))
    return render_template('index.html', data=data_manager.current_data(), labels=data_manager.unique_labels(), progress=data_manager.get_progress())

if __name__ == "__main__":
    app.run(debug=True, port=5001)
