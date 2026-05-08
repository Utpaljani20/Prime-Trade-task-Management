from app import create_app
from flask import send_from_directory
import os

app = create_app()

# Base directory for templates
TEMPLATE_DIR = os.path.join(app.root_path, '../static/templates')

@app.route('/')
def home():
    return send_from_directory(TEMPLATE_DIR, 'index.html')

# Ye route har HTML file ko serve karega (Dashboard ke liye zaroori hai)
@app.route('/templates/<path:filename>')
def serve_template(filename):
    return send_from_directory(TEMPLATE_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)