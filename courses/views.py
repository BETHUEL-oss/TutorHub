
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Course, CourseImage
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import (CourseForm, CourseImageForm)
from django.utils.text import slugify
from django.forms import modelformset_factory
from django_daraja.mpesa.core import MpesaClient
from django.conf import settings

# Create your views here.

class HomePageView(ListView):
    model = Course
    template_name = 'home.html'
    context_object_name = 'courses'
    #total_courses = Course.objects.filter(available=True).count()
    #queryset = Course.objects.filter(available=True)[:8]

    def get_queryset(self):
        return Course.objects.filter(available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_courses'] = Course.objects.filter(available=True).count()
        return context

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    queryset = Course.objects.filter(available=True)
    paginate_by = 10

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    slug_url_kwarg = 'slug'

@require_POST
@login_required
def add_to_cart(request, course_id):
    if not request.htmx:
        return HttpResponseBadRequest("HTMX required")
    # Simple session-based cart for MVP
    course = get_object_or_404(Course, id=course_id)
    if course.in_stock <= 1:
        return JsonResponse({'status': 'error', 'message': 'course is out of stock'}, status=400)

    cart = request.session.get('cart', {})
    current_quantity = cart.get(course_id, 0)
    new_quantity = current_quantity + 1
    if new_quantity > course.in_stock:
        return JsonResponse({'status': 'error', 'message': 'Max stock reached'}, status=400)

    cart[str(course_id)] = new_quantity
    request.session['cart'] = cart
    request.session.modified = True

    total_count = sum(cart.values())
    return JsonResponse({'status': 'added', 'total_count': total_count, 'course_quantity': new_quantity}, status=200)

def teacher_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not hasattr(request.user, "teacher_profile"):
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@teacher_required
def teacher_dashboard(request):
    courses = Course.objects.filter(teacher=request.user)
    return render(request, "tutor/teacher_dashboard.html", {"courses": courses})

@login_required
@teacher_required
def add_course(request):
    ImageFormSet = modelformset_factory(CourseImage, form=CourseImageForm, extra=3)

    if request.method == "POST":
        form = CourseForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=CourseImage.objects.none())

        if form.is_valid() and formset.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.slug = slugify(course.name)
            course.save()

            for image_form in formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.course = course
                    image.save()

            return redirect("teacher_dashboard")
    else:
        form = CourseForm()
        formset = ImageFormSet(queryset=CourseImage.objects.none())

    return render(request, "courses/add_course.html", {
        "form": form,
        "formset": formset,
    })

@login_required
@teacher_required
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)

    ImageFormSet = modelformset_factory(CourseImage, form=CourseImageForm, extra=1)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        formset = ImageFormSet(request.POST, request.FILES, queryset=course.images.all())

        if form.is_valid() and formset.is_valid():
            form.save()

            for image_form in formset:
                if image_form.cleaned_data:
                    img = image_form.save(commit=False)
                    img.course = course
                    img.save()

            return redirect("teacher_dashboard")
    else:
        form = CourseForm(instance=course)
        formset = ImageFormSet(queryset=course.images.all())

    return render(request, "courses/edit_course.html", {
        "form": form,
        "formset": formset,
        "course": course
    })

@login_required
@teacher_required
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk, teacher=request.user)

    if request.method == "POST":
        course.delete()
        return redirect("teacher_dashboard")

    return render(request, "courses/delete_course.html", {"course": course})

def mpesa_pay(request):
    if request.method == "POST":
        print("--MPESA ENVIRONMENT VALUE IS:", settings.MPESA_ENVIRONMENT)
        phone = request.POST.get("phone")
        amount = int(request.POST.get("amount"))

        client = MpesaClient()

        account_ref = "TutorHub"
        desc = "agri payment"

        callback_url = "https://callback.com/url"

        response = client.stk_push(phone, amount, account_ref, desc, callback_url)
        return render(request, "course/payform.html", {"message":"STK Push sent!"})
    return render(request, "course/payform.html")
