from flask import Flask, request, render_template, send_file, redirect, url_for
import os
import PyPDF2
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MERGED_FOLDER'] = 'merged'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MERGED_FOLDER'], exist_ok=True)

def merge_pdfs(pdf_files, output_path):
    # Create a PDF writer object
    pdf_writer = PyPDF2.PdfWriter()
    
    # Iterate through each PDF file
    for pdf_file in pdf_files:
        # Open the PDF file in read-binary mode
        with open(pdf_file, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            # Iterate through each page of the PDF and add it to the writer object
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)

    # Write the merged PDF to the output path
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    final_output_text = request.form.get('final_output_text')
    uploaded_files = request.files.getlist('pdf_files')
    
    if final_output_text == '':
        return "Please enter the final pdf name.", 400
    
    finalname = final_output_text + '.pdf'

    # Save each uploaded file to the upload folder
    pdf_file_paths = []
    for file in uploaded_files:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        pdf_file_paths.append(file_path)

    # Define the path for the output merged PDF
    output_path = os.path.join(app.config['MERGED_FOLDER'], finalname)
    merge_pdfs(pdf_file_paths, output_path)

    # Clean up uploaded files after merging
    for file_path in pdf_file_paths:
        os.remove(file_path)

    return redirect(url_for('download_file', filename=finalname))

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['MERGED_FOLDER'], filename), as_attachment=True)

    

if __name__ == '__main__':
    app.run(debug=True)
