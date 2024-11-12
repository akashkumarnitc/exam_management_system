from django import forms
from django.contrib.auth.models import User
from .models import Exam, Student, Teacher, Question, Result

class UserRegistrationForm(forms.ModelForm):
    user_type = forms.ChoiceField(choices=[('teacher', 'Teacher'), ('student', 'Student')])
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'password', 'user_type']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            if self.cleaned_data['user_type'] == 'teacher':
                Teacher.objects.create(user=user)
            else:
                Student.objects.create(user=user)
        return user

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'description', 'date', 'duration', 'status']
        widgets = {
            'date': forms.DateTimeInput(attrs={'placeholder': 'YYYY-MM-DD HH:MM', 'type': 'datetime-local'}),
            'duration': forms.NumberInput(attrs={'placeholder': 'Enter duration in minutes'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option', 'marks']
        widgets = {
            'correct_option': forms.Select(choices=[
                (1, 'Option 1'),
                (2, 'Option 2'),
                (3, 'Option 3'),
                (4, 'Option 4'),
            ]),
        }

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'exam', 'score', 'total_marks', 'percentage', 'graded']
        widgets = {
            'score': forms.HiddenInput(),
            'total_marks': forms.HiddenInput(),
            'percentage': forms.HiddenInput(),
            'graded': forms.HiddenInput(),
        }

    def calculate_result(self, exam, answers):
        score = 0
        total_marks = 0
        for question_id, selected_option in answers.items():
            question = Question.objects.get(id=question_id)
            total_marks += question.marks
            if int(selected_option) == question.correct_option:
                score += question.marks

        self.instance.score = score
        self.instance.total_marks = total_marks
        self.instance.percentage = (score / total_marks) * 100 if total_marks > 0 else 0
        self.instance.graded = True