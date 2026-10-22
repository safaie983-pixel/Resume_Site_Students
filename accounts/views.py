from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import models
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
import urllib.request
import json

from .forms import (
    RegisterForm, ProfileForm, SkillForm, ExperienceForm, EducationForm, 
    ProjectForm, CertificateForm, PaymentReceiptForm, JobPostForm
)
from .models import (
    Profile, Skill, Experience, Education, Project, Certificate, 
    Subscription, PaymentReceipt, Message, JobPost
)
from .pdf_utils import render_to_pdf


def calculate_profile_completion(profile):
    total_fields = 12
    filled = 0
    if profile.full_name: filled += 1
    if profile.job_title: filled += 1
    if profile.bio: filled += 1
    if profile.email: filled += 1
    if profile.phone: filled += 1
    if profile.location: filled += 1
    if profile.avatar: filled += 1
    if profile.skills.exists(): filled += 1
    if profile.experiences.exists(): filled += 1
    if profile.educations.exists(): filled += 1
    if profile.projects.exists(): filled += 1
    if profile.certificates.exists(): filled += 1
    return int((filled / total_fields) * 100)


def home(request):
    query = request.GET.get('q', '').strip()
    if query:
        users = User.objects.filter(is_active=True).filter(
            models.Q(username__icontains=query) | models.Q(profile__full_name__icontains=query)
        ).distinct()
    else:
        users = User.objects.filter(is_active=True).order_by('-date_joined')[:12]
    return render(request, 'home.html', {'users': users, 'query': query})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    next_url = request.GET.get('next', 'home') 
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    profile = request.user.profile
    subscription, created_sub = Subscription.objects.get_or_create(user=request.user)
    is_sub_active = subscription.check_active()
    
    context = {
        'profile': profile,
        'skills': profile.skills.all(),
        'experiences': profile.experiences.all(),
        'educations': profile.educations.all(),
        'projects': profile.projects.all(),
        'certificates': profile.certificates.all(),
        'subscription': subscription,
        'is_sub_active': is_sub_active,
        'stats': {
            'skills_count': profile.skills.count(),
            'experiences_count': profile.experiences.count(),
            'educations_count': profile.educations.count(),
            'projects_count': profile.projects.count(),
            'certificates_count': profile.certificates.count(),
            'profile_completion': calculate_profile_completion(profile),
        }
    }
    return render(request, 'dashboard.html', context)


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False); skill.profile = request.user.profile; skill.save()
            return redirect('dashboard')
    else: form = SkillForm()
    return render(request, 'add_item.html', {'form': form, 'title': 'افزودن مهارت جدید'})

@login_required
def add_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False); exp.profile = request.user.profile; exp.save()
            return redirect('dashboard')
    else: form = ExperienceForm()
    return render(request, 'add_item.html', {'form': form, 'title': 'افزودن تجربه کاری جدید'})

@login_required
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False); edu.profile = request.user.profile; edu.save()
            return redirect('dashboard')
    else: form = EducationForm()
    return render(request, 'add_item.html', {'form': form, 'title': 'افزودن تحصیلات جدید'})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False); project.profile = request.user.profile; project.save()
            return redirect('dashboard')
    else: form = ProjectForm()
    return render(request, 'add_item.html', {'form': form, 'title': 'افزودن پروژه جدید'})

@login_required
def add_certificate(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            cert = form.save(commit=False); cert.profile = request.user.profile; cert.save()
            return redirect('dashboard')
    else: form = CertificateForm()
    return render(request, 'add_item.html', {'form': form, 'title': 'افزودن گواهی‌نامه جدید'})

@login_required
def delete_skill(request, pk): Skill.objects.filter(pk=pk, profile=request.user.profile).delete(); return redirect('dashboard')
@login_required
def delete_experience(request, pk): Experience.objects.filter(pk=pk, profile=request.user.profile).delete(); return redirect('dashboard')
@login_required
def delete_education(request, pk): Education.objects.filter(pk=pk, profile=request.user.profile).delete(); return redirect('dashboard')
@login_required
def delete_project(request, pk): Project.objects.filter(pk=pk, profile=request.user.profile).delete(); return redirect('dashboard')
@login_required
def delete_certificate(request, pk): Certificate.objects.filter(pk=pk, profile=request.user.profile).delete(); return redirect('dashboard')


def public_profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile = user_obj.profile
    context = {
        'profile_user': user_obj,
        'profile': profile,
        'skills': profile.skills.all(),
        'experiences': profile.experiences.all(),
        'educations': profile.educations.all(),
        'projects': profile.projects.all(),
        'certificates': profile.certificates.all(),
    }
    return render(request, 'public_profile.html', context)


def download_resume_pdf(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile = user_obj.profile
    context = {
        'profile_user': user_obj,
        'profile': profile,
        'skills': profile.skills.all(),
        'experiences': profile.experiences.all(),
        'educations': profile.educations.all(),
        'projects': profile.projects.all(),
        'certificates': profile.certificates.all(),
    }
    pdf = render_to_pdf('resume_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="resume-{username}.pdf"'
        return response
    return HttpResponse('خطا در ساخت PDF', status=500)


# ==================== بخش اشتراک ====================

def get_dollar_price_toman():
    try:
        req = urllib.request.Request("https://api.nobitex.ir/v2/orderbook/USDTIRT", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return int(float(data['lastTradePrice']) / 10)
    except Exception:
        return 271000

@login_required
def subscription_page(request):
    subscription, created = Subscription.objects.get_or_create(user=request.user)
    is_active = subscription.check_active()
    dollar_price = get_dollar_price_toman()
    total_price = int(dollar_price * 1.5)
    receipt_form = PaymentReceiptForm()
    
    context = {
        'subscription': subscription,
        'is_active': is_active,
        'dollar_price': dollar_price,
        'total_price': total_price,
        'receipt_form': receipt_form,
    }
    return render(request, 'subscription.html', context)


@login_required
def upload_receipt(request):
    if request.method == 'POST':
        form = PaymentReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.user = request.user
            receipt.save()
            messages.success(request, 'فیش واریزی شما با موفقیت ثبت شد و در انتظار تایید مدیر است.')
            return redirect('subscription_page')
    return redirect('subscription_page')


# ==================== بخش چت (پیام‌رسان) ====================

@login_required
def inbox(request):
    # بررسی فعال بودن اشتراک
    sub, _ = Subscription.objects.get_or_create(user=request.user)
    if not sub.check_active():
        messages.warning(request, 'برای استفاده از بخش پیام‌رسان، باید اشتراک فعال داشته باشید.')
        return redirect('subscription_page')

    # پیدا کردن تمام کاربرانی که با این کاربر چت کرده‌اند
    sent_msgs = Message.objects.filter(sender=request.user).values_list('receiver', flat=True)
    received_msgs = Message.objects.filter(receiver=request.user).values_list('sender', flat=True)
    
    user_ids = set(list(sent_msgs) + list(received_msgs))
    chat_users = User.objects.filter(id__in=user_ids)

    # گرفتن لیست تمام کاربران دیگر برای شروع چت جدید
    all_users = User.objects.exclude(id=request.user.id)

    context = {
        'chat_users': chat_users,
        'all_users': all_users,
    }
    return render(request, 'inbox.html', context)


@login_required
def chat_room(request, username):
    # بررسی فعال بودن اشتراک
    sub, _ = Subscription.objects.get_or_create(user=request.user)
    if not sub.check_active():
        messages.warning(request, 'برای استفاده از بخش پیام‌رسان، باید اشتراک فعال داشته باشید.')
        return redirect('subscription_page')

    other_user = get_object_or_404(User, username=username)
    
    # گرفتن پیام‌های بین این دو کاربر
    chat_messages = Message.objects.filter(
        models.Q(sender=request.user, receiver=other_user) |
        models.Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')

    # علامت زدن پیام‌های دریافتی به عنوان خوانده شده
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('chat_room', username=other_user.username)

    context = {
        'other_user': other_user,
        'chat_messages': chat_messages,
    }
    return render(request, 'chat_room.html', context)