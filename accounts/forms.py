from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Experience, Education, Project, Certificate


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='ایمیل')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'نام کاربری'
        self.fields['password1'].label = 'رمز عبور'
        self.fields['password2'].label = 'تکرار رمز عبور'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'job_title', 'email', 'phone', 'location', 'website', 'avatar', 'linkedin', 'github', 'twitter', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and hasattr(avatar, 'size') and avatar.size > 0:
            if avatar.size > 5 * 1024 * 1024:
                raise forms.ValidationError('حجم عکس نباید بیشتر از ۵ مگابایت باشه')
            name = avatar.name.lower()
            if not (name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png') or name.endswith('.webp')):
                raise forms.ValidationError('فقط فرمت‌های JPG، PNG و WebP پشتیبانی می‌شن')
        return avatar


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level']


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'field', 'university', 'start_year', 'end_year']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'link', 'image', 'technologies']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'size') and image.size > 0:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('حجم عکس نباید بیشتر از ۵ مگابایت باشه')
            name = image.name.lower()
            if not (name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png') or name.endswith('.webp')):
                raise forms.ValidationError('فقط فرمت‌های JPG، PNG و WebP پشتیبانی می‌شن')
        return image


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['title', 'issuer', 'issue_date', 'link']