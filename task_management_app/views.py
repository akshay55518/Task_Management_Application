from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task
from django.contrib.auth import get_user_model 
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            messages.error(request, "Please fill out all fields.")
            return redirect("login")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser == 1:
                request.session['id']=user.id
                return redirect('superadmin_dashboard')
            elif user.role == "Admin":
                if user.is_staff == 1:
                    request.session['id']=user.id
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, "Admin not found")
                    return redirect('login')
            elif user.role == "User":
                if user.value == 1:
                    request.session['id']=user.id
                    return redirect('user_dashboard')
                else:
                    messages.error(request, "superAdmin not approved.")
                    return redirect('login')
            else:
                messages.error(request, "Unknown role assigned to user.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, "login.html")

def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")

User = get_user_model()

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        gender = request.POST.get("gender")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("register")
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")
        user = User.objects.create(
            username=username,
            first_name=name,
            gender=gender,
            phone=phone,
            email=email,
            role="User",
            value=0,
            password=make_password(password),
        )
        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")
    return render(request, "register.html")

def superadmin_dashboard(request):
    id=request.session["id"]
    data=User.objects.filter(id=id)
    users = User.objects.exclude(username=request.user.username).filter(value=1)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority")
        due_date = request.POST.get("due-date")
        assigned_to_id = request.POST.get("assigned-to")
        if not assigned_to_id:
            users = User.objects.all()
            return render(request, 'dashboard/superadmin_dashboard.html', {'users': users, 'error': 'Please select a user for the task.'})
        assigned_to = User.objects.get(id=assigned_to_id)
        task = Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            assigned_to=assigned_to,
            priority=priority, 
        )
    tasks = Task.objects.all()
    return render(request, "dashboard/superadmin_dashboard.html", locals())

def admin_dashboard(request):
    id=request.session["id"]
    data=User.objects.filter(id=id)
    users = User.objects.exclude(username=request.user.username).filter(value=1)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        priority = request.POST.get("priority")
        due_date = request.POST.get("due-date")
        assigned_to_id = request.POST.get("assigned-to")
        if not assigned_to_id:
            users = User.objects.all()
            return render(request, 'dashboard/superadmin_dashboard.html', {'users': users, 'error': 'Please select a user for the task.'})
        assigned_to = User.objects.get(id=assigned_to_id)
        task = Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            assigned_to=assigned_to,
            priority=priority, 
        )
    tasks = Task.objects.all()
    return render(request, "dashboard/admin_dashboard.html", locals())

def user_dashboard(request):
    id=request.session["id"]
    data=User.objects.filter(id=id)
    task=Task.objects.filter(assigned_to=id)
    return render(request, "dashboard/user_dashboard.html",locals())

def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('superadmin_dashboard')

def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.status = request.POST.get('status')
        task.worked_hours = request.POST.get('worked_hours')
        task.completion_report = request.POST.get('completion_report')
        task.save()
        return redirect('user_dashboard')
    return render(request, 'update_task.html', {'task': task})

def approval(request):
    id = request.session.get("id")
    if not id:
        return redirect('login')
    data = User.objects.filter(id=id)  
    approval_needed = User.objects.exclude(id=id).filter(value=0, role="User")
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'approval_page.html', locals())

def approve_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.value = 1
        user.save()
        messages.success(request, f"User {user.username} has been approved successfully.")
        return redirect('approval')
    return redirect('approval')
    
def delete_notapproved_user(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.warning(request, f"User {user.username} has been deleted by Admin")
        return redirect('approval')
    return redirect('approval')

def delete_user(request, id):
    if request.method == "POST":
        user = get_object_or_404(User, id=id)
        if user.role != "SuperAdmin":
            user.delete()
        return redirect('approval')

def add_admin(request):
    id = request.session["id"]
    data = User.objects.filter(id=id)
    if request.method == "POST":
        username = request.POST.get("username")
        name = request.POST.get("name")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        role = request.POST.get("role")
        first_name, *last_name = name.split(' ', 1)
        value = 1
        is_staff = False
        if role == "Admin":
            value = 0
            is_staff = True
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name[0] if last_name else '',
            phone=phone,
            gender=gender,
            role=role,
            value=value,
            is_staff=is_staff,
        )
        user.set_password("12345")
        user.save()
        messages.success(request, f"{role} '{username}' registered successfully.")
        return redirect('add_admin')
    return render(request, "add_admin_User.html", {'data': data})