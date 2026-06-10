from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile



def login_view(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)

            return redirect("home")

    return render(
        request,
        "accounts/login.html"
    )


def register_view(request):

    if request.method == "POST":

        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        profile_picture = request.FILES.get(
            "profile_picture"
        )

        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            password=password
        )

        if profile_picture:
            user.profile.profile_picture = profile_picture
            user.profile.save()

        return redirect("login")

    return render(
        request,
        "accounts/register.html"
    )


@login_required
def logout_view(request):

    logout(request)

    return redirect("home")


@login_required
def orders(request):
    return render(request, "accounts/orders.html")
    
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):

    profile = request.user.profile

    return render(request, "accounts/profile.html", {"profile": profile})

@login_required
def edit_profile(request):

    profile = request.user.profile

    if request.method == "POST":

        request.user.first_name = request.POST.get(
            "first_name"
        )

        request.user.last_name = request.POST.get(
            "last_name"
        )

        request.user.email = request.POST.get(
            "email"
        )

        if request.FILES.get(
            "profile_picture"
        ):

            profile.profile_picture = request.FILES.get(
                "profile_picture"
            )

            profile.save()

        request.user.save()

        messages.success(
            request,
            "Profile updated successfully!"
        )

        return redirect(
            "profile"
        )

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "profile": profile
        }
    )