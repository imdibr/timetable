import os
from flask import Flask, render_template, request
import pandas as pd

# Configure Flask app
app = Flask(__name__, 
            template_folder='ui',   # Set 'ui' as the folder for HTML templates
            static_folder='static') # Set 'static' as the folder for static files

# Configure folders for file uploads
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for the homepage
@app.route('/')
def homepage():
    return render_template('homepage.html')

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('homepage.html', error="No file part")

    file = request.files['file']
    if file.filename == '':
        return render_template('homepage.html', error="No file selected")

    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        # Read the Excel file
        data = pd.read_excel(file_path)

        # Check if the DataFrame is empty
        if data.empty:
            return render_template('homepage.html', error="Uploaded file is empty")

        # Process the DataFrame (Example: Print its head for debugging)
        print(data.head())

        # Return success popup
        return render_template('success.html')  # Redirect to success page

    except Exception as e:
        return render_template('homepage.html', error=f"An error occurred: {str(e)}")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
