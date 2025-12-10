from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Courses, CoursesImage
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CoursesForm, CoursesImageForm
from django.utils.text import slugify
from django.forms import modelformset_factory
from django_daraja.mpesa.core import MpesaClient
from django.conf import settings

# Create your views here.

class HomePageView(ListView):
    model = Courses
    template_name = 'home.html'
    context_object_name = 'courses'
    # total_courses = Courses.objects.filter(available=True).count()
    queryset = Courses.objects.filter(available=True)[:8]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # The query now runs inside a method, after the app is fully loaded
        context['total_courses'] = Courses.objects.filter(available=True).count()
        return context

class CoursesListView(ListView):
    model = Courses
    template_name = 'courses/courses_list.html'
    context_object_name = 'courses'
    queryset = Courses.objects.filter(available=True)
    paginate_by = 10

class CoursesDetailView(DetailView):
    model = Courses
    template_name = 'courses/courses_detail.html'
    context_object_name = 'courses`'
    slug_url_kwarg = 'slug'

@require_POST
@login_required
def add_to_cart(request, courses_id):
    if not request.htmx:
        return HttpResponseBadRequest("HTMX required")
    # Simple session-based cart for MVP
    courses = get_object_or_404(Courses, id=courses_id)
    if not courses.available:
        return JsonResponse({'status': 'error', 'message': 'Course is out of stock'}, status=400)

    cart = request.session.get('cart', {})
    current_quantity = cart.get(courses_id, 0)
    new_quantity = current_quantity + 1
    if new_quantity > courses.available:
        return JsonResponse({'status': 'error', 'message': 'Course available to be taken'}, status=400)

    cart[str(courses_id)] = new_quantity
    request.session['cart'] = cart
    request.session.modified = True

    total_count = sum(cart.values())
    return JsonResponse({'status': 'added', 'total_count': total_count, 'course_quantity': new_quantity}, status=200)

def tutor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not hasattr(request.user, "tutor_profile"):
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@tutor_required
def tutor_dashboard(request):
    courses = Courses.objects.filter(tutor=request.user)
    return render(request, "tutors/tutor_dashboard.html", {"courses": courses})

@login_required
@tutor_required
def add_courses(request):
    ImageFormSet = modelformset_factory(CoursesImage, form=CoursesImageForm, extra=3)

    if request.method == "POST":
        form = Courses(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Courses.objects.none())

        if form.is_valid() and formset.is_valid():
            courses = form.save(commit=False)
            courses.tutor = request.user
            courses.slug = slugify(courses.name)
            courses.save()

            for image_form in formset:
                if image_form.cleaned_data:
                    image = image_form.save(commit=False)
                    image.courses = courses
                    image.save()

            return redirect("farmer_dashboard")
    else:
        form = CoursesForm()
        formset = ImageFormSet(queryset=Courses.objects.none())

    return render(request, "courses/add_courses.html", {
        "form": form,
        "formset": formset,
    })

@login_required
@tutor_required
def edit_courses(request, pk):
    product = get_object_or_404(Courses, pk=pk, farmer=request.user)

    ImageFormSet = modelformset_factory(CoursesImage, form=CoursesImageForm, extra=1)

    if request.method == "POST":
        form = Courses(request.POST, instance=product)
        formset = ImageFormSet(request.POST, request.FILES, queryset=product.images.all())

        if form.is_valid() and formset.is_valid():
            form.save()

            for image_form in formset:
                if image_form.cleaned_data:
                    img = image_form.save(commit=False)
                    img.product = product
                    img.save()

            return redirect("farmer_dashboard")
    else:
        form = Courses(instance=product)
        formset = ImageFormSet(queryset=product.images.all())

    return render(request, "courses/edit_courses.html", {
        "form": form,
        "formset": formset,
        "courses": Courses
    })

@login_required
@tutor_required
def delete_courses(request, pk):
    product = get_object_or_404(Courses, pk=pk, farmer=request.user)

    if request.method == "POST":
        product.delete()
        return redirect("tutor_dashboard")

    return render(request, "courses/delete_courses.html", {"courses": Courses})

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
        return render(request, "courses/payform.html", {"message":"STK Push sent!"})
    return render(request, "courses/payform.html")