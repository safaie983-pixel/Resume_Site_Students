from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/edit/', views.edit_profile, name='edit_profile'),
    
    # بخش آیتم‌های رزومه
    path('dashboard/add-skill/', views.add_skill, name='add_skill'),
    path('dashboard/add-experience/', views.add_experience, name='add_experience'),
    path('dashboard/add-education/', views.add_education, name='add_education'),
    path('dashboard/add-project/', views.add_project, name='add_project'),
    path('dashboard/add-certificate/', views.add_certificate, name='add_certificate'),
    
    # بخش حذف آیتم‌ها
    path('dashboard/delete-skill/<int:pk>/', views.delete_skill, name='delete_skill'),
    path('dashboard/delete-experience/<int:pk>/', views.delete_experience, name='delete_experience'),
    path('dashboard/delete-education/<int:pk>/', views.delete_education, name='delete_education'),
    path('dashboard/delete-project/<int:pk>/', views.delete_project, name='delete_project'),
    path('dashboard/delete-certificate/<int:pk>/', views.delete_certificate, name='delete_certificate'),
    
    # بخش اشتراک
    path('subscription/', views.subscription_page, name='subscription_page'),
    path('subscription/upload/', views.upload_receipt, name='upload_receipt'),
    
    # بخش چت (پیام‌رسان)
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<str:username>/', views.chat_room, name='chat_room'),

    # بخش آگهی‌های کار (فریلنسری)
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/add/', views.add_job, name='add_job'),
    path('jobs/delete/<int:pk>/', views.delete_job, name='delete_job'),

    # بخش مینی‌سایت (SaaS)
    path('mini-site/manage/', views.manage_mini_site, name='manage_mini_site'),
    path('mini-site/delete/<int:pk>/', views.delete_custom_link, name='delete_custom_link'),
    path('site/<str:username>/', views.public_mini_site, name='public_mini_site'),

    # بخش پروفایل عمومی
    path('u/<str:username>/', views.public_profile, name='public_profile'),
    path('u/<str:username>/pdf/', views.download_resume_pdf, name='download_resume_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)