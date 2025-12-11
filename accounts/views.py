from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, TeacherRegistrationForm
from .models import TutorProfile, PupilProfile
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def register_student(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            PupilProfile.objects.create(
                user=user,
                location=form.cleaned_data["location"]
            )
            login(request, user)
            return redirect("home")
    else:
        form = StudentRegistrationForm()

    return render(request, "accounts/register_student.html", {"form": form})

def register_teacher(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            TutorProfile.objects.create(
                user=user,
                school=form.cleaned_data["school"],
                location=form.cleaned_data["location"],
                certification=form.cleaned_data.get("certification", ""),
                bio=form.cleaned_data.get("bio", "")
            )
            login(request, user)
            try:
                if hasattr(user, "tutor_profile"):
                    return redirect("teacher_dashboard")
                elif hasattr(user, "pupil_profile"):
                    return redirect("home")
            except:
                return redirect("home")
    else:
        form = TeacherRegistrationForm()

    return render(request, "accounts/register_teacher.html", {"form": form})

def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # REDIRECT BASED ON ROLE
            if hasattr(user, "tutor_profile"):
                return redirect("teacher_dashboard")

            elif hasattr(user, "pupil_profile"):
                return redirect("home")

            # fallback if no profile
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})

@login_required
def tutor_dashboard(request):
    return render(request, 'tutor/dashboard.html')