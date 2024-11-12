from django.urls import path
from . import views

app_name = 'exam_management'  # Use a namespace

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout page

    # Registration URLs
    path('register/teacher/', views.register_teacher, name='register_teacher'),  # Teacher registration
    path('register/student/', views.register_student, name='register_student'),  # Student registration

    # Dashboard URLs
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),  # Teacher dashboard
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),  # Student dashboard

    # Exam management URLs (Teacher)
    path('exam/create/', views.create_exam, name='create_exam'),  # Create exam
    path('exam/<int:exam_id>/edit/', views.edit_exam, name='edit_exam'),  # Edit exam
    path('exam/<int:exam_id>/delete/', views.delete_exam, name='delete_exam'),  # Delete exam
    path('exam/<int:exam_id>/add-question/', views.add_question, name='add_question'),  # Add questions to exam

    # Question management URL (Teacher)
    path('question/<int:question_id>/edit/', views.edit_question, name='edit_question'),  # Edit question

    # Exam participation and results (Student)
    # In your urls.py
    path('start_exam/<int:exam_id>/', views.start_exam, name='start_exam'),
    path('take_exam/<int:exam_id>/', views.take_exam, name='take_exam'),
   # path('exam/<int:exam_id>/take/', views.take_exam, name='take_exam'),  # Take an exam
    path('exam/<int:exam_id>/results/', views.exam_results, name='exam_results'),  # View results for a specific exam
    path('results/', views.view_results, name='view_results'),  # View all results for student
]