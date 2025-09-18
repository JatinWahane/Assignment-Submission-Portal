from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Assignment, Submission
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

# Home
def home(request):
    return render(request, "assignments/home.html")

# Authentication
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, password=password)
        return redirect("login")
    return render(request, "assignments/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("assignment_list")
    return render(request, "assignments/login.html")

def logout_view(request):
    logout(request)
    return redirect("home")

# Assignment CRUD (Teacher only)
@login_required
def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, "assignments/assignment_list.html", {"assignments": assignments})

@login_required
def assignment_create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        deadline = request.POST["deadline"]
        Assignment.objects.create(title=title, description=description, deadline=deadline, created_by=request.user)
        return redirect("assignment_list")
    return render(request, "assignments/assignment_form.html")

@login_required
def assignment_edit(request, id):
    assignment = get_object_or_404(Assignment, id=id)
    if request.method == "POST":
        assignment.title = request.POST["title"]
        assignment.description = request.POST["description"]
        assignment.deadline = request.POST["deadline"]
        assignment.save()
        return redirect("assignment_list")
    return render(request, "assignments/assignment_form.html", {"assignment": assignment})

@login_required
def assignment_delete(request, id):
    assignment = get_object_or_404(Assignment, id=id)
    assignment.delete()
    return redirect("assignment_list")

# Submissions
@login_required
def submit_assignment(request, id):
    assignment = get_object_or_404(Assignment, id=id)
    if request.method == "POST" and request.FILES["file"]:
        file = request.FILES["file"]
        Submission.objects.create(assignment=assignment, student=request.user, file=file)
        return redirect("submission_list")
    return render(request, "assignments/submit_assignment.html", {"assignment": assignment})

@login_required
def submission_list(request):
    submissions = Submission.objects.filter(student=request.user)
    return render(request, "assignments/submission_list.html", {"submissions": submissions})
