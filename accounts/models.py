from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, blank=True, verbose_name='نام و نام خانوادگی')
    bio = models.TextField(blank=True, verbose_name='درباره من')
    job_title = models.CharField(max_length=100, blank=True, verbose_name='عنوان شغلی')
    email = models.EmailField(blank=True, verbose_name='ایمیل')
    phone = models.CharField(max_length=20, blank=True, verbose_name='شماره تماس')
    location = models.CharField(max_length=100, blank=True, verbose_name='محل سکونت')
    website = models.URLField(blank=True, verbose_name='وب‌سایت')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='عکس پروفایل')
    linkedin = models.URLField(blank=True, verbose_name='لینکدین')
    github = models.URLField(blank=True, verbose_name='گیت‌هاب')
    twitter = models.URLField(blank=True, verbose_name='توییتر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین ویرایش')

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل‌ها'

    def __str__(self):
        return f'پروفایل {self.user.username}'


class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100, verbose_name='نام مهارت')
    level = models.PositiveIntegerField(default=50, verbose_name='سطح (0-100)')

    class Meta:
        verbose_name = 'مهارت'
        verbose_name_plural = 'مهارت‌ها'

    def __str__(self):
        return f'{self.name} - {self.profile.user.username}'


class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=100, verbose_name='عنوان شغلی')
    company = models.CharField(max_length=100, verbose_name='نام شرکت/سازمان')
    start_date = models.DateField(verbose_name='تاریخ شروع')
    end_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان')
    description = models.TextField(blank=True, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'تجربه کاری'
        verbose_name_plural = 'تجربه‌های کاری'

    def __str__(self):
        return f'{self.title} - {self.company}'


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=100, verbose_name='مدرک')
    field = models.CharField(max_length=100, verbose_name='رشته تحصیلی')
    university = models.CharField(max_length=150, verbose_name='دانشگاه/موسسه')
    start_year = models.CharField(max_length=10, verbose_name='سال شروع')
    end_year = models.CharField(max_length=10, blank=True, verbose_name='سال پایان')

    class Meta:
        verbose_name = 'تحصیلات'
        verbose_name_plural = 'تحصیلات'

    def __str__(self):
        return f'{self.degree} - {self.field}'


class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=150, verbose_name='عنوان پروژه')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    link = models.URLField(blank=True, verbose_name='لینک پروژه')
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name='عکس پروژه')
    technologies = models.CharField(max_length=200, blank=True, verbose_name='تکنولوژی‌ها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.profile.user.username}'


class Certificate(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certificates')
    title = models.CharField(max_length=150, verbose_name='عنوان گواهی‌نامه')
    issuer = models.CharField(max_length=150, verbose_name='صادرکننده')
    issue_date = models.CharField(max_length=20, blank=True, verbose_name='تاریخ صدور')
    link = models.URLField(blank=True, verbose_name='لینک گواهی‌نامه')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'گواهی‌نامه'
        verbose_name_plural = 'گواهی‌نامه‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.profile.user.username}'


auditlog.register(Profile)
auditlog.register(Skill)
auditlog.register(Experience)
auditlog.register(Education)
auditlog.register(Project)
auditlog.register(Certificate)