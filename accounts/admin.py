from django.contrib import admin
from .models import Profile, Skill, Experience, Education


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
    list_display = ('user', 'full_name', 'job_title', 'location', 'created_at')
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