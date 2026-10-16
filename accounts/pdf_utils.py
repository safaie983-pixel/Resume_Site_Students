from io import BytesIO
import os
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ثبت فونت فارسی برای xhtml2pdf
FONT_PATH = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Vazirmatn-Regular.ttf')
if os.path.exists(FONT_PATH):
    try:
        pdfmetrics.registerFont(TTFont('Vazirmatn', FONT_PATH))
    except Exception:
        pass


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')
    if not pdf.err:
        return result.getvalue()
    return None