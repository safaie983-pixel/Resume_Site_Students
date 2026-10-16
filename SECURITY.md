# مستند امنیتی پروژه

## اطلاعات پروژه
- نام پروژه: سایت رزومه‌ساز شخصی
- فریم‌ورک: Django 6.1.2
- استانداردها: OWASP Top 10 (2021) و OWASP WSTG v4.2

---

## پوشش OWASP Top 10

| کد | آسیب‌پذیری | وضعیت | اقدام انجام شده |
|----|------------|-------|----------------|
| A01 | Broken Access Control | پوشش داده شد | استفاده از login_required، بررسی مالکیت اشیاء، مسدودسازی دسترسی کاربر عادی به پنل ادمین |
| A02 | Cryptographic Failures | پوشش داده شد | انتقال SECRET_KEY به .env، کوکی‌های Secure و HttpOnly |
| A03 | Injection | پوشش داده شد | استفاده کامل از Django ORM، عدم استفاده از Raw SQL |
| A04 | Insecure Design | پوشش داده شد | محدودیت حجم آپلود و تعداد فیلدها، Rate Limiting |
| A05 | Security Misconfiguration | پوشش داده شد | اجرای check --deploy، هدرهای امنیتی، صفحات خطای سفارشی |
| A06 | Vulnerable Components | پوشش داده شد | استفاده از آخرین نسخه Django |
| A07 | Authentication Failures | پوشش داده شد | Password Validators قوی، Brute-Force Protection |
| A08 | Software and Data Integrity | پوشش داده شد | Audit Log برای تمام تغییرات |
| A09 | Logging and Monitoring | پوشش داده شد | django-auditlog، ثبت تلاش‌های ورود ناموفق |
| A10 | SSRF | پوشش داده شد | عدم دریافت URL از کاربر به صورت مستقیم |

---

## تست‌های WSTG انجام شده

### WSTG-CONF
- WSTG-CONF-01: بررسی پیکربندی شبکه
- WSTG-CONF-07: بررسی هدرهای امنیتی HTTP
  - Content-Security-Policy تنظیم شده
  - X-Frame-Options: DENY فعال
  - X-Content-Type-Options: nosniff فعال
  - Referrer-Policy تنظیم شده
  - Permissions-Policy تنظیم شده

### WSTG-ATHN
- WSTG-ATHN-01: بررسی رمزهای ضعیف (Password Validators فعال)
- WSTG-ATHN-03: تست قفل حساب (django-axes بعد از ۵ تلاش ناموفق)
- WSTG-ATHN-07: تست سیاست رمز عبور

### WSTG-ATHZ
- WSTG-ATHZ-01: تست دسترسی افقی و عمودی
- WSTG-ATHZ-02: تست دور زدن مسیر
- WSTG-ATHZ-04: تست IDOR در viewهای delete

### WSTG-SESS
- WSTG-SESS-01: تست مکانیزم Session
- WSTG-SESS-02: بررسی ویژگی‌های کوکی
- WSTG-SESS-06: تست logout

### WSTG-INPV
- WSTG-INPV-01: تست XSS
- WSTG-INPV-05: تست SQL Injection
- WSTG-INPV-11: تست Code Injection

---

## پکیج‌های امنیتی استفاده شده

- django-axes: محافظت در برابر Brute-Force
- django-auditlog: ثبت تمام تغییرات ادمین
- python-dotenv: مدیریت متغیرهای محیطی

---

## نتیجه‌گیری

پروژه با رعایت اصول امنیتی OWASP Top 10 و انجام تست‌های WSTG آماده ارائه است.

---

## منابع

- OWASP Top 10: https://owasp.org/Top10/
- OWASP WSTG: https://owasp.org/www-project-web-security-testing-guide/
- Django Security: https://docs.djangoproject.com/en/stable/topics/security/