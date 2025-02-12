from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.validators import MinValueValidator
from django.db import IntegrityError
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import Count
from .models import User, LogFiles, Logs
import re
from django.db.models import Q
import re
from .helpers import summarize_errors
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Logs
from django.db.models import Count

@login_required
def dashboard(request):
    error_codes = [400, 401, 403, 404, 405, 408, 409, 410, 413, 414, 429, 500, 501, 502, 503, 504, 505, 507, 508]
    
    # Logs filtrés par codes d'erreur
    filtered_logs = Logs.objects.filter(code__in=error_codes)
    
    # Résumé des erreurs
    summary = summarize_errors(filtered_logs)
    
    # Comptage des logs par code d'erreur
    error_summary = filtered_logs.values('code').annotate(count=Count('code'))

    # Résumé des systèmes d'exploitation (OS)
    os_summary = Logs.objects.values('OS').annotate(count=Count('OS'))

    return render(request, "Wizard/dashboard.html", {
        "summary": summary,
        "error_summary": error_summary,
        "os_summary": os_summary
    })




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("dashboard"))
        else:
            return render(request, "Wizard/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Wizard/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("welcome"))


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        birthday_str = request.POST.get("birthday")
        sex = request.POST.get("sex")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        
        # Ensure required fields are provided
        if not all([email, first_name, last_name, birthday_str, sex, password, confirmation]):
            return render(request, "Wizard/register.html", {
                "message": "All fields are required."
            })

        # Validate birthday format
        try:
            birthday = datetime.strptime(birthday_str, "%Y-%m-%d").date()
        except ValueError:
            return render(request, "Wizard/register.html", {
                "message": "Invalid date format."
            })

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "Wizard/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                birthday=birthday,
                sex=sex
            )
            user.save()
        except IntegrityError:
            return render(request, "Wizard/register.html", {
                "message": "Username already taken."
            })
        except Exception as e:
            return render(request, "Wizard/register.html", {
                "message": f"An error occurred: {str(e)}"
            })

        login(request, user)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return render(request, "Wizard/register.html")
    

@login_required
def profile_view(request):
    if request.method == "POST":
        user = get_object_or_404(User, pk=request.user.pk)
        user.username = request.POST["email"]
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.birthday = datetime.strptime(request.POST["birthday"], "%Y-%m-%d").date()
        user.save()

        return HttpResponseRedirect(reverse("profile"))
    else:
        user = request.user
        email = user.username
        first_name = user.first_name
        last_name = user.last_name
        birthday = user.birthday.strftime('%Y-%m-%d')
        sex = user.sex
        return render(request, "Wizard/user.html", {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'birthday': birthday,
            'sex' : sex
        })

    

@login_required
def log_files_view(request):
    # Fetch statistics for the 'code' column
    code_stats = Logs.objects.values('code').annotate(count=Count('code')).order_by('code')
    code_labels = [entry['code'] for entry in code_stats]
    code_values = [entry['count'] for entry in code_stats]

    # Fetch statistics for the 'OS' column
    os_stats = Logs.objects.values('OS').annotate(count=Count('OS')).order_by('count')
    os_labels = [entry['OS'] for entry in os_stats]
    os_values = [entry['count'] for entry in os_stats]

    # Fetch statistics for the 'browser' column
    browser_stats = Logs.objects.values('browser').annotate(count=Count('browser')).order_by('count')
    browser_labels = [entry['browser'] for entry in browser_stats]
    browser_values = [entry['count'] for entry in browser_stats]

    # Fetch statistics for the 'method' column (extracted from the 'name' column)
    method_stats = Logs.objects.values('name').annotate(count=Count('name')).order_by('count')
    method_labels = [entry['name'] for entry in method_stats]
    method_values = [entry['count'] for entry in method_stats]

    return render(request, 'Wizard/log_files.html', {
        'code_labels': code_labels,
        'code_values': code_values,
        'os_labels': os_labels,
        'os_values': os_values,
        'browser_labels': browser_labels,
        'browser_values': browser_values,
        'method_labels': method_labels,
        'method_values': method_values,
    })


@login_required
def errors_view(request):
    # Initialize default query parameters
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    priority = request.GET.get('priority', '')

    error_codes = [400, 401, 403, 404, 405, 408, 409, 410, 413, 414, 429, 500, 501, 502, 503, 504, 505, 507, 508]


    filtered_logs = Logs.objects.filter(code__in=error_codes)
    # Fetch statistics for the error codes (unaffected by filters)
    code_stats = filtered_logs.values('code').annotate(count=Count('code')).order_by('code')
    code_labels = [entry['code'] for entry in code_stats]
    code_values = [entry['count'] for entry in code_stats]

    # Fetch statistics for the priority column (unaffected by filters)
    priority_stats = filtered_logs.values('priority').annotate(count=Count('priority')). order_by('priority')
    priority_labels = [entry['priority'] for entry in priority_stats]
    priority_values = [entry['count'] for entry in priority_stats]

    # Filter logs by date range and priority for the table
    

    # Apply date filter only if both start and end dates are provided
    if start_date and end_date:
        start_date_object = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        end_date_object = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
        filtered_logs = filtered_logs.filter(time__date__range=[start_date_object, end_date_object])

    # Apply priority filter if it is specified
    if priority:
        filtered_logs = filtered_logs.filter(priority=priority)

    return render(request, 'Wizard/errors.html', {
        'code_labels': code_labels,
        'code_values': code_values,
        'priority_labels': priority_labels,
        'priority_values': priority_values,
        'filtered_logs': filtered_logs,
        'start_date': start_date,
        'end_date': end_date,
        'priority': priority,
    })



def about_view(request):
    return render(request, 'Wizard/about.html')

def welcome(request):
    return render(request, 'Wizard/welcome.html')