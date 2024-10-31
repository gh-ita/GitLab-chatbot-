from flask import Blueprint, request, current_app, url_for, jsonify 

main = Blueprint('main',__name__)

#endpoint for data ingestion
@main.route('/upload', method = ['POST'])
def upload_documents():
    files = request.list.getlist('files')
    results = {}

    pdf_files = []
    img = []
    mkd_files = []
    html_files = []
    for file in files :
        if file.filename.endswith("pdf") :
            pdf_files.append(file)
        elif file.filename.endswith("md") :
            mkd_files.append(file)
        elif file.filename.endswith("html") :
            html_files.append(file)
        elif file.content_type.startswith("image/") :
            img.append(file)
        else :
            results[file.filename] = "Unsupported file type"
        
    handle_pdf(pdf_files)
    handle_mkd(mkd_files)
    handle_img(img)
    handle_html(html_files)

    results["processed"] = {
        'pdf' : len(pdf_files),
        'markdown' : len(mkd_files),
        'image' : len(img),
        'html' : len(html_files)
    }

    return jsonify(results)
#sub-route to handle pdf files
def handle_pdf(file_list) :
    for file in file_list :
        current_app.embedchain_app.add(file, data_type = 'pdf_file')
#sub-route to handle web pages
def handle_html(file_list) :
    for file in file_list :
        current_app.embedchain_app.add(file, data_type = 'web_page')
#sub-route to handle image data
def handle_img(file_list) :
    for file in file_list :
        current_app.embedchain_app.add(file, data_type = 'image')
#sub-route to handle markdown files
def handle_mkd(file_list) :
    for file in file_list :
        current_app.embedchain_app.add(file, data_type = 'mdx')