from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .models import Exam, Student, Teacher, Result, Question
from .forms import UserRegistrationForm, ExamForm, QuestionForm
from django.http import JsonResponse
def home(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'teacher'):
            return redirect('teacher_dashboard')
        elif hasattr(request.user, 'student'):
            return redirect('student_dashboard')
        else:
            return render(request, 'home.html', {'error': "Unknown user role."})
    return render(request, 'home.html')

# Register as Teacher
def register_teacher(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Teacher.objects.create(user=user)
            messages.success(request, "Registration successful! You can log in now.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register_teacher.html', {'form': form})

# Register as Student
def register_student(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user)
            messages.success(request, "Registration successful! You can log in now.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register_student.html', {'form': form})

# Login View with Role-Based Redirection
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'teacher'):
                    return redirect('teacher_dashboard')
                elif hasattr(user, 'student'):
                    return redirect('student_dashboard')
                else:
                    messages.error(request, "Unknown user role.")
            else:
                messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Please provide both username and password.")
    return render(request, 'registration/login.html')

# Teacher Dashboard
@login_required
def teacher_dashboard(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    exams = Exam.objects.filter(teacher=teacher).annotate(question_count=Count('questions'))
    return render(request, 'teacher_dashboard.html', {'exams': exams})

# Student Dashboard
@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)

    # Get all exams
    all_exams = Exam.objects.all()
    
    # Get exams already taken by the student
    taken_exams = Result.objects.filter(student=student).values_list('exam', flat=True)

    # Separate available and previous exams
    available_exams = all_exams.exclude(id__in=taken_exams)
    previous_exams = all_exams.filter(id__in=taken_exams)

    return render(request, 'student_dashboard.html', {
        'available_exams': available_exams,
        'previous_exams': previous_exams,
    })

@login_required
def create_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.teacher = request.user.teacher
            exam.save()
            messages.success(request, "Exam created successfully!")
            return redirect('add_question', exam_id=exam.id)
    else:
        form = ExamForm()
    return render(request, 'create_exam.html', {'form': form})

@login_required
def view_exams(request):
    if hasattr(request.user, 'teacher'):
        exams = Exam.objects.filter(teacher=request.user.teacher).annotate(question_count=Count('questions'))
        user_role = 'teacher'
    elif hasattr(request.user, 'student'):
        exams = Exam.objects.all()
        user_role = 'student'
    else:
        exams = []
        user_role = None
        messages.error(request, "You don't have access to view exams.")
        return redirect('home')

    return render(request, 'view_exams.html', {'exams': exams, 'user_role': user_role})

@login_required
def edit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam updated successfully!")
            return redirect('view_exams')
    else:
        form = ExamForm(instance=exam)

    return render(request, 'edit_exam.html', {'form': form, 'exam': exam})

@login_required
def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':
        exam.delete()
        messages.success(request, "Exam deleted successfully!")
        return redirect('view_exams')

    return render(request, 'confirm_delete.html', {'exam': exam})

@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    student = get_object_or_404(Student, user=request.user)

    # Check if the student has already taken this exam
    if Result.objects.filter(student=student, exam=exam).exists():
        messages.error(request, "You have already taken this exam.")
        return redirect('view_results')  # Redirect to results or any appropriate page

    if request.method == 'POST':
        answers = {key: value for key, value in request.POST.items() if key.startswith('question_')}
        score = 0
        total_questions = exam.questions.count()

        for question_id, selected_choice in answers.items():
            question = get_object_or_404(Question, id=int(question_id.split('_')[1]))
            if selected_choice == str(question.correct_option):
                score += question.marks

        # Create a new result only if the exam hasn't been taken
        result = Result(student=student, exam=exam, score=score, total_marks=total_questions)
        result.save()
        messages.success(request, f'You scored {score} out of {total_questions}!')
        return redirect('view_results')

    # Total duration in seconds
    total_duration = exam.duration * 60  # Convert minutes to seconds

    questions = exam.questions.all()
    return render(request, 'take_exam.html', {
        'exam': exam,
        'questions': questions,
        'total_duration': total_duration,  # Pass the total duration in seconds
    })

def auto_submit_exam(request, exam, student):
    score = 0
    total_questions = exam.questions.count()
    result = Result(student=student, exam=exam, score=score, total_marks=total_questions)
    result.save()
    messages.info(request, "Your exam has been auto-submitted.")
    return redirect('exam_results', exam_id=exam.id)

@login_required
def add_question(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()
            messages.success(request, "Question added successfully!")

            if 'add_another' in request.POST:
                return redirect('add_question', exam_id=exam.id)
            else:
                return redirect('view_exams')
    else:
        form = QuestionForm()
    return render(request, 'add_question.html', {'form': form, 'exam': exam})

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.user.teacher != question.exam.teacher:
        messages.error(request, "You don't have permission to edit this question.")
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question updated successfully!")
            return redirect('view_exams')
    else:
        form = QuestionForm(instance=question)

    return render(request, 'edit_question.html', {'form': form, 'question': question})

@login_required
def exam_results(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    student = get_object_or_404(Student, user=request.user)
    result = Result.objects.filter(student=student, exam=exam).first()

    if result:
        correct_answers = result.score
        percentage = (correct_answers / result.total_marks) * 100 if result.total_marks else 0
        return render(request, 'exam_results.html', {
            'result': result,
            'exam': exam,
            'percentage': percentage,
            'correct_answers': correct_answers,
        })
    else:
        messages.error(request, "No result found for this exam.")
        return redirect('student_dashboard')

@login_required
def view_results(request):
    student = get_object_or_404(Student, user=request.user)
    results = Result.objects.filter(student=student)
    return render(request, 'view_results.html', {'results': results})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
    
@login_required
def start_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    return render(request, 'start_exam.html', {
        'exam': exam,
    })