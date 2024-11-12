from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Teacher: {self.user.username}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Student: {self.user.username}"

class Exam(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"Exam: {self.title}"

    def clean(self):
        """Ensure the exam date is in the future."""
        if self.date < timezone.now():
            raise ValidationError('The exam date must be in the future.')

class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.IntegerField()  # Correct option index (1 to 4)
    marks = models.IntegerField(help_text="Marks awarded for the correct answer")  # Marks for the question

    def __str__(self):
        return f"Question for {self.exam.title}: {self.question_text[:50]}..."

    def clean(self):
        """Validate that correct_option is between 1 and 4."""
        if not (1 <= self.correct_option <= 4):
            raise ValidationError('Correct option must be a number between 1 and 4.')

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)  # Total score achieved by the student
    total_marks = models.IntegerField(default=0)  # Total possible marks for the exam
    percentage = models.FloatField(default=0.0)  # Score percentage
    graded = models.BooleanField(default=True)  # Indicates if the exam is graded
    total_questions = models.IntegerField(default=0) 
    class Meta:
        unique_together = ('student', 'exam')  # Ensures a student has only one result per exam

    def __str__(self):
        return f"Result: {self.student.user.username} - {self.exam.title}: {self.score}/{self.total_marks} ({self.percentage}%)"

    def calculate_result(self, answers):
        """
        Calculate the score based on the student's answers.
        :param answers: Dictionary where keys are question IDs and values are chosen options.
        """
        self.score = 0
        self.total_marks = 0
        for question in self.exam.questions.all():
            self.total_marks += question.marks
            if answers.get(question.id) == question.correct_option:
                self.score += question.marks
        self.percentage = (self.score / self.total_marks) * 100 if self.total_marks > 0 else 0
        self.save()