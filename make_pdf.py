import os
import sys
from io import BytesIO
from xhtml2pdf import pisa

# مسیر فایل HTML
HTML_FILE = 'DOCUMENTATION.html'
PDF_FILE = 'DOCUMENTATION.pdf'


def link_callback(uri, rel):
    if os.path.isabs(uri) and os.path.isfile(uri):
        return uri
    return uri


def convert_html_to_pdf(source_html, output_filename):
    with open(source_html, 'r', encoding='utf-8') as f:
        html_content = f.read()

    with open(output_filename, 'wb') as result_file:
        pdf = pisa.pisaDocument(
            BytesIO(html_content.encode('UTF-8')),
            result_file,
            encoding='UTF-8',
            link_callback=link_callback
        )
        if pdf.err:
            print('خطا در ساخت PDF')
            return False
    return True


if __name__ == '__main__':
    if not os.path.exists(HTML_FILE):
        print(f'فایل {HTML_FILE} پیدا نشد!')
        sys.exit(1)

    print('در حال ساخت PDF...')
    if convert_html_to_pdf(HTML_FILE, PDF_FILE):
        print(f'✅ PDF با موفقیت ساخته شد: {PDF_FILE}')
    else:
        print('❌ ساخت PDF با خطا مواجه شد')