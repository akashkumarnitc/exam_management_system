from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from exams import views

urlpatterns = [
    # Home URL
    path('', views.home, name='home'),

    # Registration URLs
    path('register/teacher/', views.register_teacher, name='register_teacher'),
    path('register/student/', views.register_student, name='register_student'),
    
    # Authentication URLs
    path('login/', LoginView.as_view(template_name='registration/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(template_name='home.html'), name='logout'),

    # Exam Management URLs
    path('create_exam/', views.create_exam, name='create_exam'),
    path('add_question/<int:exam_id>/', views.add_question, name='add_question'),
    path('view_exams/', views.view_exams, name='view_exams'),
    path('edit_exam/<int:exam_id>/', views.edit_exam, name='edit_exam'),
    path('edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('delete_exam/<int:exam_id>/', views.delete_exam, name='delete_exam'),
    path('start_exam/<int:exam_id>/', views.start_exam, name='start_exam'),
    path('take_exam/<int:exam_id>/', views.take_exam, name='take_exam'),
   # path('take_exam/<int:exam_id>/', views.take_exam, name='take_exam'),
    path('view_results/', views.view_results, name='view_results'),
    
    # Dashboard URLs
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),

    # Admin URL
    path('admin/', admin.site.urls),

    # Include Django's built-in authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),

    # Include app-specific URLs for the exams app
    path('exams/', include('exams.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)