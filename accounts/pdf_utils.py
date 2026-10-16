from io import BytesIO
import os
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.conf import settings


def link_callback(uri, rel):
    """حل مسیر فایل‌ها برای xhtml2pdf (فونت، تصاویر و ...)"""
    if uri.startswith('file://'):
        path = uri[7:]
        if os.path.isfile(path):
            return path
    if os.path.isabs(uri) and os.path.isfile(uri):
        return uri
    if not uri.startswith(('http://', 'https://')):
        for prefix, folder in [('/static/', 'static'), ('/media/', 'media')]:
            if uri.startswith(prefix):
                path = os.path.join(settings.BASE_DIR, folder, uri[len(prefix):])
                if os.path.isfile(path):
                    return path
        path = os.path.join(settings.BASE_DIR, uri)
        if os.path.isfile(path):
            return path
    return uri


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")),
        result,
        encoding='UTF-8',
        link_callback=link_callback
    )
    if not pdf.err:
        return result.getvalue()
    return None