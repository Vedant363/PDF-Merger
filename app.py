from flask import Flask, request, render_template, send_file
import io
import PyPDF2
from werkzeug.utils import secure_filename

app = Flask(__name__)

def merge_pdfs(pdf_files):
    # Create a PDF writer object
    pdf_writer = PyPDF2.PdfWriter()
    
    # Iterate through each PDF file
    for pdf_file in pdf_files:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        # Iterate through each page of the PDF and add it to the writer object
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

    # Use BytesIO to save the merged PDF in memory
    output_stream = io.BytesIO()
    pdf_writer.write(output_stream)
    output_stream.seek(0)  # Move to the beginning of the stream for reading
    return output_stream

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    final_output_text = request.form.get('final_output_text')
    uploaded_files = request.files.getlist('pdf_files')
    
    if final_output_text == '':
        return "Please enter the final PDF name.", 400
    
    finalname = final_output_text + '.pdf'

    # Merge the PDFs and get the output stream
    merged_pdf_stream = merge_pdfs(uploaded_files)

    # Return the merged PDF file for download
    return send_file(
        merged_pdf_stream,
        as_attachment=True,
        download_name=finalname,
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
