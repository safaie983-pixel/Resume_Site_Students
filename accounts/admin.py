from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import (
    Profile, Skill, Experience, Education, Project, Certificate, 
    CustomLink, Subscription, PaymentReceipt, Message, JobPost, SiteSetting
)


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'job_title', 'location', 'theme', 'created_at')
    search_fields = ('user__username', 'full_name', 'job_title')
    inlines = [SkillInline, ExperienceInline, EducationInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile', 'level')
    list_filter = ('level',)
    search_fields = ('name',)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'profile', 'start_date', 'end_date')
    search_fields = ('title', 'company')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'field', 'university', 'profile')
    search_fields = ('degree', 'field', 'university')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile', 'technologies', 'created_at')
    search_fields = ('title', 'technologies')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'profile', 'issue_date')
    search_fields = ('title', 'issuer')


@admin.register(CustomLink)
class CustomLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'profile')
    search_fields = ('title', 'url')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active', 'expiry_date')
    list_filter = ('is_active',)
    search_fields = ('user__username',)


@admin.action(description='تأیید فیش‌های انتخاب شده و فعال‌سازی اشتراک ۳۰ روزه')
def approve_receipts(modeladmin, request, queryset):
    for receipt in queryset:
        if receipt.status != 'approved':
            receipt.status = 'approved'
            receipt.save()

            sub, created = Subscription.objects.get_or_create(user=receipt.user)
            sub.is_active = True
            
            now = timezone.now()
            if sub.expiry_date and sub.expiry_date > now:
                sub.expiry_date += timedelta(days=30)
            else:
                sub.expiry_date = now + timedelta(days=30)
            
            sub.save()
    modeladmin.message_user(request, f'{queryset.count()} فیش با موفقیت تأیید و اشتراک کاربران فعال شد.')


@admin.register(PaymentReceipt)
class PaymentReceiptAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'uploaded_at')
    list_filter = ('status', 'uploaded_at')
    search_fields = ('user__username',)
    actions = [approve_receipts]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content_short', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'content')

    def content_short(self, obj):
        return obj.content[:30] + '...' if len(obj.content) > 30 else obj.content
    content_short.short_description = 'متن پیام'


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'budget', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'user__username')


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('subscription_price',)
    
    # برای اینکه فقط یک رکورد تنظیمات داشته باشیم و ادمین نتونه رکورد جدید بسازه
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return True