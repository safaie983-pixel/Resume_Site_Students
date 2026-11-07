from django.db import models
from django.contrib.auth.models import User
from auditlog.registry import auditlog
from django.utils import timezone
import random
import string


class Profile(models.Model):
    THEME_CHOICES = [
        ('dark', 'Ã˜ÂªÃ˜Â§Ã˜Â±Ã›Å’ÃšÂ© (Ã™Â¾Ã›Å’Ã˜Â´Ã¢â‚¬Å’Ã™ÂÃ˜Â±Ã˜Â¶)'),
        ('light', 'Ã˜Â±Ã™Ë†Ã˜Â´Ã™â€ '),
        ('neon', 'Ã™â€ Ã˜Â¦Ã™Ë†Ã™â€ '),
        ('ocean', 'Ã˜Â§Ã™â€šÃ›Å’Ã˜Â§Ã™â€ Ã™Ë†Ã˜Â³ (Ã˜Â¢Ã˜Â¨Ã›Å’)'),
        ('sunset', 'Ã˜ÂºÃ˜Â±Ã™Ë†Ã˜Â¨ (Ã™â€ Ã˜Â§Ã˜Â±Ã™â€ Ã˜Â¬Ã›Å’/Ã˜Â¨Ã™â€ Ã™ÂÃ˜Â´)'),
        ('forest', 'Ã˜Â¬Ã™â€ ÃšÂ¯Ã™â€ž (Ã˜Â³Ã˜Â¨Ã˜Â²)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, blank=True, verbose_name='Ã™â€ Ã˜Â§Ã™â€¦ Ã™Ë† Ã™â€ Ã˜Â§Ã™â€¦ Ã˜Â®Ã˜Â§Ã™â€ Ã™Ë†Ã˜Â§Ã˜Â¯ÃšÂ¯Ã›Å’')
    bio = models.TextField(blank=True, verbose_name='Ã˜Â¯Ã˜Â±Ã˜Â¨Ã˜Â§Ã˜Â±Ã™â€¡ Ã™â€¦Ã™â€ ')
    job_title = models.CharField(max_length=100, blank=True, verbose_name='Ã˜Â¹Ã™â€ Ã™Ë†Ã˜Â§Ã™â€  Ã˜Â´Ã˜ÂºÃ™â€žÃ›Å’')
    email = models.EmailField(blank=True, verbose_name='Ã˜Â§Ã›Å’Ã™â€¦Ã›Å’Ã™â€ž')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Ã˜Â´Ã™â€¦Ã˜Â§Ã˜Â±Ã™â€¡ Ã˜ÂªÃ™â€¦Ã˜Â§Ã˜Â³')
    location = models.CharField(max_length=100, blank=True, verbose_name='Ã™â€¦Ã˜Â­Ã™â€ž Ã˜Â³ÃšÂ©Ã™Ë†Ã™â€ Ã˜Âª')
    website = models.URLField(blank=True, verbose_name='Ã™Ë†Ã˜Â¨Ã¢â‚¬Å’Ã˜Â³Ã˜Â§Ã›Å’Ã˜Âª')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Ã˜Â¹ÃšÂ©Ã˜Â³ Ã™Â¾Ã˜Â±Ã™Ë†Ã™ÂÃ˜Â§Ã›Å’Ã™â€ž')
    linkedin = models.URLField(blank=True, verbose_name='Ã™â€žÃ›Å’Ã™â€ ÃšÂ©Ã˜Â¯Ã›Å’Ã™â€ ')
    github = models.URLField(blank=True, verbose_name='ÃšÂ¯Ã›Å’Ã˜ÂªÃ¢â‚¬Å’Ã™â€¡Ã˜Â§Ã˜Â¨')
    twitter = models.URLField(blank=True, verbose_name='Ã˜ÂªÃ™Ë†Ã›Å’Ã›Å’Ã˜ÂªÃ˜Â±')
    
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='dark', verbose_name='Ã™â€šÃ˜Â§Ã™â€žÃ˜Â¨ Ã˜Â³Ã˜Â§Ã›Å’Ã˜Âª Ã˜Â´Ã˜Â®Ã˜ÂµÃ›Å’')
    has_mini_site = models.BooleanField(default=False, verbose_name='Ã™â€¦Ã›Å’Ã™â€ Ã›Å’Ã¢â‚¬Å’Ã˜Â³Ã˜Â§Ã›Å’Ã˜Âª Ã˜Â³Ã˜Â§Ã˜Â®Ã˜ÂªÃ™â€¡ Ã˜Â´Ã˜Â¯Ã™â€¡ Ã˜Â§Ã˜Â³Ã˜Âª')
    card_number = models.CharField(max_length=30, blank=True, verbose_name='Ã˜Â´Ã™â€¦Ã˜Â§Ã˜Â±Ã™â€¡ ÃšÂ©Ã˜Â§Ã˜Â±Ã˜Âª Ã˜Â¨Ã˜Â±Ã˜Â§Ã›Å’ Ã˜Â¯Ã˜Â±Ã›Å’Ã˜Â§Ã™ÂÃ˜Âª Ã™Ë†Ã˜Â¬Ã™â€¡')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ã˜ÂªÃ˜Â§Ã˜Â±Ã›Å’Ã˜Â® Ã˜Â§Ã›Å’Ã˜Â¬Ã˜Â§Ã˜Â¯')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ã˜Â¢Ã˜Â®Ã˜Â±Ã›Å’Ã™â€  Ã™Ë†Ã›Å’Ã˜Â±Ã˜Â§Ã›Å’Ã˜Â´')

    class Meta:
        verbose_name = 'Ã™Â¾Ã˜Â±Ã™Ë†Ã™ÂÃ˜Â§Ã›Å’Ã™â€ž'
        verbose_name_plural = 'Ã™Â¾Ã˜Â±Ã™Ë†Ã™ÂÃ˜Â§Ã›Å’Ã™â€žÃ¢â‚¬Å’Ã™â€¡Ã˜Â§'

    def __str__(self):
        return f'Ã™Â¾Ã˜Â±Ã™Ë†Ã™ÂÃ˜Â§Ã›Å’Ã™â€ž {self.user.username}'


class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100, verbose_name='Ã™â€ Ã˜Â§Ã™â€¦ Ã™â€¦Ã™â€¡Ã˜Â§Ã˜Â±Ã˜Âª')
    level = models.PositiveIntegerField(default=50, verbose_name='Ã˜Â³Ã˜Â·Ã˜Â­ (0-100)')

    class Meta:
        verbose_name = 'Ã™â€¦Ã™â€¡Ã˜Â§Ã˜Â±Ã˜Âª'
        verbose_name_plural = 'Ã™â€¦Ã™â€¡Ã˜Â§Ã˜Â±Ã˜ÂªÃ¢â‚¬Å’Ã™â€¡Ã˜Â§'

    def __str__(self):
        return f'{self.name} - {self.profile.user.username}'


class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=100, verbose_name='Ã˜Â¹Ã™â€ Ã™Ë†Ã˜Â§Ã™â€  Ã˜Â´Ã˜ÂºÃ™â€žÃ›Å’')
    company = models.CharField(max_length=100, verbose_name='Ã™â€ Ã˜Â§Ã™â€¦ Ã˜Â´Ã˜Â±ÃšÂ©Ã˜Âª/Ã˜Â³Ã˜Â§Ã˜Â²Ã™â€¦Ã˜Â§Ã™â€ ')
    start_date = models.DateField(verbose_name='Ã˜ÂªÃ˜Â§Ã˜Â±Ã›Å’Ã˜Â® Ã˜Â´Ã˜Â±Ã™Ë†Ã˜Â¹')
    end_date = models.DateField(null=True, blank=True, verbose_name='Ã˜ÂªÃ˜Â§Ã˜Â±Ã›Å’Ã˜Â® Ã™Â¾Ã˜Â§Ã›Å’Ã˜Â§Ã™â€ ')
    description = models.TextField(blank=True, verbose_name='Ã˜ÂªÃ™Ë†Ã˜Â¶Ã›Å’Ã˜Â­Ã˜Â§Ã˜Âª')

    class Meta:
        verbose_name = 'Ã˜ÂªÃ˜Â¬Ã˜Â±Ã˜Â¨Ã™â€¡ ÃšÂ©Ã˜Â§Ã˜Â±Ã›Å’'
        verbose_name_plural = 'Ã˜ÂªÃ˜Â¬Ã˜Â±Ã˜Â¨Ã™â€¡Ã¢â‚¬Å’Ã™â€¡Ã˜Â§Ã›Å’ ÃšÂ©Ã˜Â§Ã˜Â±Ã›Å’'

    def __str__(self):
        return f'{self.title} - {self.company}'


class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=100, verbose_name='Ã™â€¦Ã˜Â¯Ã˜Â±ÃšÂ©')
    field = models.CharField(max_length=100, verbose_name='Ã˜Â±Ã˜Â´Ã˜ÂªÃ™â€¡ Ã˜ÂªÃ˜Â­Ã˜ÂµÃ›Å’Ã™â€žÃ›Å’')
    university = models.CharField(max_length=150, verbose_name='Ã˜Â¯Ã˜Â§Ã™â€ Ã˜Â´ÃšÂ¯Ã˜Â§Ã™â€¡/Ã™â€¦Ã™Ë†Ã˜Â³Ã˜Â³Ã™â€¡')
    start_year = models.CharField(max_length=10, verbose_name='Ã˜Â³Ã˜Â§Ã™â€ž Ã˜Â´Ã˜Â±Ã™Ë†Ã˜Â¹')
    end_year = models.CharField(max_length=10, blank=True, verbose_name='Ã˜Â³Ã˜Â§Ã™â€ž Ã™Â¾Ã˜Â§Ã›Å’Ã˜Â§Ã™â€ ')

    class Meta:
        verbose_name = 'Ã˜ÂªÃ˜Â­Ã˜ÂµÃ›Å’Ã™â€žÃ˜Â§Ã˜Âª'
        verbose_name_plural = 'Ã˜ÂªÃ˜Â­Ã˜ÂµÃ›Å’Ã™â€žÃ˜Â§Ã˜Âª'

    def __str__(self):
        return f'{self.degree} - {self.field}'


class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=150, verbose_name='Ã˜Â¹Ã™â€ Ã™Ë†Ã˜Â§Ã™â€  Ã™Â¾Ã˜Â±Ã™Ë†ÃšËœÃ™â€¡')
    description = models.TextField(blank=True, verbose_name='Ã˜ÂªÃ™Ë†Ã˜Â¶Ã›Å’Ã˜Â­Ã˜Â§Ã˜Âª')
    link = models.URLField(blank=True, verbose_name='Ã™â€žÃ›Å’Ã™â€ ÃšÂ© Ã™Â¾Ã˜Â±Ã™Ë†ÃšËœÃ™â€¡')
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name='Ã˜Â¹ÃšÂ©Ã˜Â³ Ã™Â¾Ã˜Â±Ã™Ë†ÃšËœÃ™â€¡')
    technologies = models.CharField(max_length=200, blank=True, verbose_name='Ã˜ÂªÃšÂ©Ã™â€ Ã™Ë†Ã™â€žÃ™Ë†ÃšËœÃ›Å’Ã¢â‚¬Å’Ã™â€¡Ã˜Â§')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ã˜ÂªÃ˜Â§Ã˜Â±Ã›Å’Ã˜Â® Ã˜Â§Ã›Å’Ã˜Â¬Ã˜Â§Ã˜Â¯')

    class Meta:
        verbose_name = 'Ã™Â¾Ã˜Â±Ã™Ë†ÃšËœÃ™â€¡'
        verbose_name_plural = 'Ã™Â¾Ã˜Â±Ã™Ë†ÃšËœÃ™â€¡Ã¢â‚¬Å’Ã™â€¡Ã˜Â§'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.profile.user.username}'


class Product(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=150, verbose_name='Ã™â€ Ã˜Â§Ã™â€¦ Ã™â€¦Ã˜Â­Ã˜ÂµÃ™Ë†Ã™â€ž')
    description = models.TextField(blank=True, verbose_name='Ã˜ÂªÃ™Ë†Ã˜Â¶Ã›Å’Ã˜Â­Ã˜Â§Ã˜Âª')
    price = models.PositiveIntegerField(default=0, verbose_name='Ã™â€šÃ›Å’Ã™â€¦Ã˜Âª (Ã˜ÂªÃ™Ë†Ã™â€¦Ã˜Â§Ã™â€ )')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Ã˜Â¹ÃšÂ©Ã˜Â³ Ã™â€¦Ã˜Â­Ã˜ÂµÃ™Ë†Ã™â€ž')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ã˜ÂªÃ˜Â§Ã˜Â±Ã›Å’Ã˜Â® Ã˜Â§Ã›Å’Ã˜Â¬Ã˜Â§Ã˜Â¯')

    class Meta:
        verbose_name = 'Ã™â€¦Ã˜Â­Ã˜ÂµÃ™Ë†Ã™â€ž'
        verbose_name_plural = 'Ã™â€¦Ã˜Â­Ã˜ÂµÃ™Ë†Ã™â€žÃ˜Â§Ã˜Âª'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.profile.user.username}'


def generate_tracking_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ã˜Â¯Ã˜Â± Ã˜Â§Ã™â€ Ã˜ÂªÃ˜Â¸Ã˜Â§Ã˜Â± Ã˜Â¨Ã˜Â±Ã˜Â±Ã˜Â³Ã›Å’'),
        ('approved', 'Ã˜ÂªÃ˜Â£Ã›Å’Ã›Å’Ã˜Â¯ Ã˜Â´Ã˜Â¯Ã™â€¡'),
        ('delivered', 'Ã˜ÂªÃ˜Â­Ã™Ë†Ã›Å’Ã™â€ž Ã˜Â¯Ã˜Â§Ã˜Â¯Ã™â€¡ Ã˜Â´Ã˜Â¯Ã™â€¡'),
        ('rejected', 'Ã˜Â±Ã˜Â¯ Ã˜Â´Ã˜Â¯Ã™â€¡'),
    ]
    tracking_code = models.CharField(max_length=10, unique=True, default=generate_tracking_code, editable=False, verbose_name='ÃšÂ©Ã˜Â¯ Ã˜Â±Ã™â€¡ÃšÂ¯Ã›Å’Ã˜Â±Ã›Å’')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders', verbose_name='Ã™â€¦Ã˜Â­Ã˜ÂµÃ™Ë†Ã™â€ž')
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='my_orders', verbose_name='Ã˜Â®Ã˜Â±Ã›Å’Ã˜Â¯Ã˜Â§Ã˜Â± (Ã˜Â§ÃšÂ©Ã˜Â§Ã™â€ Ã˜Âª)')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_orders', verbose_name='Ã™ÂÃ˜Â±Ã™Ë†Ã˜Â´Ã™â€ Ã˜Â¯Ã™â€¡')
    
    first_name = models.CharField(max_length=50, verbose_name='Ã™â€ Ã˜Â§Ã™â€¦')
    last_name = models.CharField(max_length=50, verbose_name='Ã™â€ Ã˜Â§Ã™â€¦ Ã˜Â®Ã˜Â§Ã™â€ Ã™Ë†Ã˜Â§Ã˜Â¯ÃšÂ¯Ã›Å’')
    phone = models.CharField(max_length=20, verbose_name='Ã˜Â´Ã™â€¦Ã˜Â§Ã˜Â±Ã™â€¡ Ã˜ÂªÃ™â€¦Ã˜Â§Ã˜Â³')
    address = models.TextField(verbose_name='Ã˜Â¢Ã˜Â¯Ã˜Â±Ã˜Â³ Ã˜Â¯Ã™â€šÃ›Å’Ã™â€š')
    postal_code = models.CharField(max_length=10, verbose_name='ÃšÂ©Ã˜Â¯ Ã™Â¾Ã˜Â³Ã˜ÂªÃ›Å’')
    location = models.CharField(max_length=100, verbose_name='Ã˜Â§Ã˜Â³Ã˜ÂªÃ˜Â§Ã™â€ /Ã˜Â´Ã™â€¡Ã˜Â±')
    
    receipt_image = models.ImageField(upload_to='order_receipts/', blank=True, null=True, verbose_name='Ã˜ÂªÃ˜ÂµÃ™Ë†Ã›Å’Ã˜Â± Ã™ÂÃ›Å’Ã˜Â´ Ã™Â¾Ã˜Â±Ã˜Â¯Ã˜Â§Ã˜Â®Ã˜Âª')
    digital_file = models.FileField(upload_to='deliverables/', blank=True, null=True, verbose_name='Ã™ÂÃ˜Â§Ã›Å’Ã™â€ž Ã™â€¦Ã˜Â­Ã˜ÂµÃ™Ë†Ã™â€ž (Ã˜ÂªÃ˜Â­Ã™Ë†Ã›Å’Ã™â€ž Ã˜Â¨Ã™â€¡ Ã˜Â®Ã˜Â±Ã›Å’Ã˜Â¯Ã˜Â§Ã˜Â±)')
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Ã™Ë†Ã˜Â¶Ã˜Â¹Ã›Å’Ã˜Âª Ã˜Â³Ã™ÂÃ˜Â§Ã˜Â±Ã˜Â´')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ã˜ÂªÃ˜Â§Ã˜Â±Ã›Å’Ã˜Â® Ã˜Â«Ã˜Â¨Ã˜Âª')

    class Meta:
        verbose_name = 'Ã˜Â³Ã™ÂÃ˜Â§Ã˜Â±Ã˜Â´'
        verbose_name_plural = 'Ã˜Â³Ã™ÂÃ˜Â§Ã˜Â±Ã˜Â´Ã¢â‚¬Å’Ã™â€¡Ã˜Â§'
        ordering = ['-created_at']

    def __str__(self):
        return f'Ã˜Â³Ã™ÂÃ˜Â§Ã˜Â±Ã˜Â´ {self.tracking_code} - {self.product.name}'


class Certificate(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='certificates')
    title = models.CharField(max_length=150, verbose_name='Ã˜Â¹Ã™â€ Ã™Ë†Ã˜Â§Ã™â€  ÃšÂ¯Ã™Ë†Ã˜Â§Ã™â€¡Ã›Å’Ã¢â‚¬Å’Ã™â€ Ã˜Â§Ã™â€¦Ã™â€¡')
    issuer = models.CharField(max_length=150, verbose_name='Ã˜ÂµÃ˜Â§Ã˜Â¯Ã˜Â±ÃšÂ©Ã™â€ Ã™â€ Ã˜Â¯Ã™â€¡')
    issue_date = models.CharField(max_length=20, blank=True, verbose_name='Ã˜ÂªÃ˜Â§Ã˜Â±Ã›Å’Ã˜Â® Ã˜ÂµÃ˜Â¯Ã™Ë†Ã˜Â±')
    link = models.URLField(blank=True, verbose_name='Ã™â€žÃ›Å’Ã™â€ ÃšÂ© ÃšÂ¯Ã™Ë†Ã˜Â§Ã™â€¡Ã›Å’Ã¢â‚¬Å’Ã™â€ Ã˜Â§Ã™â€¦Ã™â€¡')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ã˜ÂªÃ˜Â§Ã˜Â±Ã›Å’Ã˜Â® Ã˜Â§Ã›Å’Ã˜Â¬Ã˜Â§Ã˜Â¯')

    class Meta:
        verbose_name = 'ÃšÂ¯Ã™Ë†Ã˜Â§Ã™â€¡Ã›Å’Ã¢â‚¬Å’Ã™â€ Ã˜Â§Ã™â€¦Ã™â€¡'
        verbose_name_plural = 'ÃšÂ¯Ã™Ë†Ã˜Â§Ã™â€¡Ã›Å’Ã¢â‚¬Å’Ã™â€ Ã˜Â§Ã™â€¦Ã™â€¡Ã¢â‚¬Å’Ã™â€¡Ã˜Â§'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.profile.user.username}'


class CustomLink(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='custom_links')
    title = models.CharField(max_length=100, verbose_name='Ã˜Â¹Ã™â€ Ã™Ë†Ã˜Â§Ã™â€  Ã™â€žÃ›Å’Ã™â€ ÃšÂ©')
    url = models.URLField(verbose_name='Ã˜Â¢Ã˜Â¯Ã˜Â±Ã˜Â³ Ã™â€žÃ›Å’Ã™â€ ÃšÂ©')

    class Meta:
        verbose_name = 'Ã™â€žÃ›Å’Ã™â€ ÃšÂ© Ã˜Â§Ã˜Â®Ã˜ÂªÃ˜ÂµÃ˜Â§Ã˜ÂµÃ›Å’'
        verbose_name_plural = 'Ã™â€žÃ›Å’Ã™â€ ÃšÂ©Ã¢â‚¬Å’Ã™â€¡Ã˜Â§Ã›Å’ Ã˜Â§Ã˜Â®Ã˜ÂªÃ˜ÂµÃ˜Â§Ã˜ÂµÃ›Å’'

    def __str__(self):
        return f'{self.title} - {self.profile.user.username}'


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    is_active = models.BooleanField(default=False, verbose_name='Ã™Ë†Ã˜Â¶Ã˜Â¹Ã›Å’Ã˜Âª Ã™ÂÃ˜Â¹Ã˜Â§Ã™â€ž Ã˜Â¨Ã™Ë†Ã˜Â¯Ã™â€ ')
    expiry_date = models.DateTimeField(null=True, blank=True, verbose_name='Ã˜ÂªÃ˜Â§Ã˜Â±Ã›Å’Ã˜Â® Ã˜Â§Ã™â€ Ã™â€šÃ˜Â¶Ã˜Â§')
    
    def check_active(self):
        if self.is_active and self.expiry_date:
            if timezone.now() > self.expiry_date:
                self.is_active = False
                self.save()
        return self.is_active

    def __str__(self):
        return f'Ã˜Â§Ã˜Â´Ã˜ÂªÃ˜Â±Ã˜Â§ÃšÂ© {self.user.username} - {"Ã™ÂÃ˜Â¹Ã˜Â§Ã™â€ž" if self.is_active else "Ã˜ÂºÃ›Å’Ã˜Â±Ã™ÂÃ˜Â¹Ã˜Â§Ã™â€ž"}'

    class Meta:
        verbose_name = 'Ã˜Â§Ã˜Â´Ã˜ÂªÃ˜Â±Ã˜Â§ÃšÂ©'
        verbose_name_plural = 'Ã˜Â§Ã˜Â´Ã˜ÂªÃ˜Â±Ã˜Â§ÃšÂ©Ã¢â‚¬Å’Ã™â€¡Ã˜Â§'


class PaymentReceipt(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ã˜Â¯Ã˜Â± Ã˜Â§Ã™â€ Ã˜ÂªÃ˜Â¸Ã˜Â§Ã˜Â± Ã˜Â¨Ã˜Â±Ã˜Â±Ã˜Â³Ã›Å’'),
        ('approved', 'Ã˜ÂªÃ˜Â£Ã›Å’Ã›Å’Ã˜Â¯ Ã˜Â´Ã˜Â¯Ã™â€¡'),
        ('rejected', 'Ã˜Â±Ã˜Â¯ Ã˜Â´Ã˜Â¯Ã™â€¡'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receipts')
    image = models.ImageField(upload_to='receipts/', verbose_name='Ã˜ÂªÃ˜ÂµÃ™Ë†Ã›Å’Ã˜Â± Ã™ÂÃ›Å’Ã˜Â´')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Ã™Ë†Ã˜Â¶Ã˜Â¹Ã›Å’Ã˜Âª')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Ã˜ÂªÃ˜Â§Ã˜Â±Ã›Å’Ã˜Â® Ã˜Â¢Ã™Â¾Ã™â€žÃ™Ë†Ã˜Â¯')

    def __str__(self):
        return f'Ã™ÂÃ›Å’Ã˜Â´ {self.user.username} - {self.get_status_display()}'

    class Meta:
        verbose_name = 'Ã™ÂÃ›Å’Ã˜Â´ Ã™Ë†Ã˜Â§Ã˜Â±Ã›Å’Ã˜Â²Ã›Å’ (Ã˜Â§Ã˜Â´Ã˜ÂªÃ˜Â±Ã˜Â§ÃšÂ©)'
        verbose_name_plural = 'Ã™ÂÃ›Å’Ã˜Â´Ã¢â‚¬Å’Ã™â€¡Ã˜Â§Ã›Å’ Ã™Ë†Ã˜Â§Ã˜Â±Ã›Å’Ã˜Â²Ã›Å’ (Ã˜Â§Ã˜Â´Ã˜ÂªÃ˜Â±Ã˜Â§ÃšÂ©)'


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(verbose_name='Ã™â€¦Ã˜ÂªÃ™â€  Ã™Â¾Ã›Å’Ã˜Â§Ã™â€¦')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ã˜ÂªÃ˜Â§Ã˜Â±Ã›Å’Ã˜Â® Ã˜Â§Ã˜Â±Ã˜Â³Ã˜Â§Ã™â€ž')
    is_read = models.BooleanField(default=False, verbose_name='Ã˜Â®Ã™Ë†Ã˜Â§Ã™â€ Ã˜Â¯Ã™â€¡ Ã˜Â´Ã˜Â¯Ã™â€¡')

    class Meta:
        verbose_name = 'Ã™Â¾Ã›Å’Ã˜Â§Ã™â€¦'
        verbose_name_plural = 'Ã™Â¾Ã›Å’Ã˜Â§Ã™â€¦Ã¢â‚¬Å’Ã™â€¡Ã˜Â§'
        ordering = ['-created_at']

    def __str__(self):
        return f'Ã˜Â§Ã˜Â² {self.sender.username} Ã˜Â¨Ã™â€¡ {self.receiver.username}'


class JobPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_posts')
    title = models.CharField(max_length=150, verbose_name='Ã˜Â¹Ã™â€ Ã™Ë†Ã˜Â§Ã™â€  ÃšÂ©Ã˜Â§Ã˜Â±')
    description = models.TextField(verbose_name='Ã˜ÂªÃ™Ë†Ã˜Â¶Ã›Å’Ã˜Â­Ã˜Â§Ã˜Âª')
    budget = models.CharField(max_length=50, verbose_name='Ã˜Â¨Ã™Ë†Ã˜Â¯Ã˜Â¬Ã™â€¡ (Ã™â€¦Ã˜Â«Ã™â€žÃ˜Â§Ã™â€¹ Ã˜ÂªÃ™Ë†Ã˜Â§Ã™ÂÃ™â€šÃ›Å’)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ã˜ÂªÃ˜Â§Ã˜Â±Ã›Å’Ã˜Â® Ã˜Â«Ã˜Â¨Ã˜Âª')
    is_active = models.BooleanField(default=True, verbose_name='Ã™ÂÃ˜Â¹Ã˜Â§Ã™â€ž')

    class Meta:
        verbose_name = 'Ã˜Â¢ÃšÂ¯Ã™â€¡Ã›Å’ ÃšÂ©Ã˜Â§Ã˜Â±'
        verbose_name_plural = 'Ã˜Â¢ÃšÂ¯Ã™â€¡Ã›Å’Ã¢â‚¬Å’Ã™â€¡Ã˜Â§Ã›Å’ ÃšÂ©Ã˜Â§Ã˜Â±'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.user.username}'


class SiteSetting(models.Model):
    subscription_price = models.PositiveIntegerField(default=150000, verbose_name='Ã™â€šÃ›Å’Ã™â€¦Ã˜Âª Ã˜Â§Ã˜Â´Ã˜ÂªÃ˜Â±Ã˜Â§ÃšÂ© Ã™â€¦Ã˜Â§Ã™â€¡Ã˜Â§Ã™â€ Ã™â€¡ (Ã˜ÂªÃ™Ë†Ã™â€¦Ã˜Â§Ã™â€ )')

    class Meta:
        verbose_name = 'Ã˜ÂªÃ™â€ Ã˜Â¸Ã›Å’Ã™â€¦Ã˜Â§Ã˜Âª Ã˜Â³Ã˜Â§Ã›Å’Ã˜Âª'
        verbose_name_plural = 'Ã˜ÂªÃ™â€ Ã˜Â¸Ã›Å’Ã™â€¦Ã˜Â§Ã˜Âª Ã˜Â³Ã˜Â§Ã›Å’Ã˜Âª'

    def __str__(self):
        return f'Ã™â€šÃ›Å’Ã™â€¦Ã˜Âª Ã˜Â§Ã˜Â´Ã˜ÂªÃ˜Â±Ã˜Â§ÃšÂ©: {self.subscription_price} Ã˜ÂªÃ™Ë†Ã™â€¦Ã˜Â§Ã™â€ '


auditlog.register(Profile)
auditlog.register(Skill)
auditlog.register(Experience)
auditlog.register(Education)
auditlog.register(Project)
auditlog.register(Product)
auditlog.register(Order)
auditlog.register(Certificate)
auditlog.register(CustomLink)
auditlog.register(Subscription)
auditlog.register(PaymentReceipt)
auditlog.register(Message)
auditlog.register(JobPost)
auditlog.register(SiteSetting)