from django.conf import settings


class SecurityHeadersMiddleware:
    """اضافه کردن هدرهای امنیتی به تمام پاسخ‌ها - مطابق OWASP"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Content Security Policy - جلوگیری از XSS
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdn.tailwindcss.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com https://cdn.fontcdn.ir; "
            "font-src 'self' https://cdn.jsdelivr.net https://fonts.gstatic.com https://cdn.fontcdn.ir data:; "
            "img-src 'self' data: https:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )

        # جلوگیری از Clickjacking
        response['X-Frame-Options'] = 'DENY'

        # جلوگیری از MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'

        # کنترل اطلاعات ارجاع‌دهنده
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # کنترل دسترسی به ویژگی‌های مرورگر
        response['Permissions-Policy'] = (
            'geolocation=(), microphone=(), camera=(), '
            'payment=(), usb=(), magnetometer=(), gyroscope=()'
        )

        # جلوگیری از XSS در مرورگرهای قدیمی
        response['X-XSS-Protection'] = '1; mode=block'

        # مخفی کردن اطلاعات سرور
        if 'Server' in response:
            del response['Server']

        return response