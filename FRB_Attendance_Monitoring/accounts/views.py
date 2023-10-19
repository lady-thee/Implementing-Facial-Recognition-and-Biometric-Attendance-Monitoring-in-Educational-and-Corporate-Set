from django.shortcuts import render, redirect, reverse
from .email_backend import EmailBackend
from django.contrib import messages
from .forms import CustomUserForm
from students.forms import StudentForm

from django.contrib.auth import login, logout
# Create your views here.


def account_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("staffDashboard"))
        else:
            return redirect(reverse("studentDashboard"))

    context = {}
    if request.method == 'POST':
        user = EmailBackend.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("staffDashboard"))
            else:
                return redirect(reverse("studentDashboard"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")

    return render(request, "login.html", context)


def account_register(request):
    form = StudentForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            student = StudentForm.save(commit=False)
            student.admin = user
            messages.success(request, "Account created. You can login now!")
            return redirect(reverse('account_login'))
        else:
            messages.error(request, "Provided data failed validation")
            # return account_login(request)
    return render(request, "account_register.html", context)


def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(
            request, "You need to be logged in to perform this action")

    return redirect(reverse("account_login"))
