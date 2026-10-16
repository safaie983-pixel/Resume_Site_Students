from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import models
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RegisterForm, ProfileForm, SkillForm, ExperienceForm, EducationForm, ProjectForm, CertificateForm
from .models import Skill, Experience, Education, Project, Certificate
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
        users = User.objects.filter(
            is_active=True
        ).filter(
            models.Q(username__icontains=query) |
            models.Q(profile__full_name__icontains=query) |
            models.Q(profile__job_title__icontains=query) |
            models.Q(profile__skills__name__icontains=query) |
            models.Q(profile__experiences__title__icontains=query) |
            models.Q(profile__experiences__company__icontains=query) |
            models.Q(profile__educations__field__icontains=query) |
            models.Q(profile__educations__university__icontains=query) |
            models.Q(profile__projects__title__icontains=query) |
            models.Q(profile__projects__technologies__icontains=query) |
            models.Q(profile__certificates__title__icontains=query) |
            models.Q(profile__certificates__issuer__icontains=query)
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
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    profile = request.user.profile
    skills = profile.skills.all()
    experiences = profile.experiences.all()
    educations = profile.educations.all()
    projects = profile.projects.all()
    certificates = profile.certificates.all()
    context = {
        'profile': profile,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'projects': projects,
        'certificates': certificates,
        'stats': {
            'skills_count': skills.count(),
            'experiences_count': experiences.count(),
            'educations_count': educations.count(),
            'projects_count': projects.count(),
            'certificates_count': certificates.count(),
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
            skill = form.save(commit=False)
            skill.profile = request.user.profile
            skill.save()
            return redirect('dashboard')
    else:
        form = SkillForm()
    return render(request, 'add_item.html', {'form': form, 'title': 'افزودن مهارت جدید'})


@login_required
def add_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.profile = request.user.profile
            exp.save()
            return redirect('dashboard')
    else:
        form = ExperienceForm()
    return render(request, 'add_item.html', {'form': form, 'title': 'افزودن تجربه کاری جدید'})


@login_required
def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.profile = request.user.profile
            edu.save()
            return redirect('dashboard')
    else:
        form = EducationForm()
    return render(request, 'add_item.html', {'form': form, 'title': 'افزودن تحصیلات جدید'})


@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = request.user.profile
            project.save()
            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'add_item.html', {'form': form, 'title': 'افزودن پروژه جدید'})


@login_required
def add_certificate(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.profile = request.user.profile
            cert.save()
            return redirect('dashboard')
    else:
        form = CertificateForm()
    return render(request, 'add_item.html', {'form': form, 'title': 'افزودن گواهی‌نامه جدید'})


@login_required
def delete_skill(request, pk):
    skill = Skill.objects.filter(pk=pk, profile=request.user.profile).first()
    if skill:
        skill.delete()
    return redirect('dashboard')


@login_required
def delete_experience(request, pk):
    exp = Experience.objects.filter(pk=pk, profile=request.user.profile).first()
    if exp:
        exp.delete()
    return redirect('dashboard')


@login_required
def delete_education(request, pk):
    edu = Education.objects.filter(pk=pk, profile=request.user.profile).first()
    if edu:
        edu.delete()
    return redirect('dashboard')


@login_required
def delete_project(request, pk):
    project = Project.objects.filter(pk=pk, profile=request.user.profile).first()
    if project:
        project.delete()
    return redirect('dashboard')


@login_required
def delete_certificate(request, pk):
    cert = Certificate.objects.filter(pk=pk, profile=request.user.profile).first()
    if cert:
        cert.delete()
    return redirect('dashboard')


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
        filename = f'resume-{username}.pdf'
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    return HttpResponse('خطا در ساخت PDF', status=500)