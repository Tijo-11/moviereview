from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCreateForm, AdminSignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.decorators.cache import cache_control  
from django.conf import settings  
from .models import CustomUser  # ✅ Import CustomUser
from django.contrib.auth.decorators import user_passes_test


# ✅ Normal User Signup (Uses CustomUser)
def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'signupaccount.html', {'form': UserCreateForm()})
    
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = CustomUser.objects.create_user(
                    full_name=request.POST['full_name'],username=request.POST['username'], 
                    email=request.POST['email'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('home')

            except IntegrityError:
                return render(request, 'signupaccount.html', {
                    'form': UserCreateForm(),
                    'error': 'Username already taken. Choose a new username.'
                })
        else:
            return render(request, 'signupaccount.html', {
                'form': UserCreateForm(),
                'error': 'Passwords do not match'
            })


# ✅ Normal User Login 
@never_cache
def loginaccount(request):
    if request.method == 'GET':
        return render(request, 'loginaccount.html', {'form': AuthenticationForm()})
    
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username exists
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return render(request, 'loginaccount.html', {
                'form': AuthenticationForm(),
                'error': 'Username does not exist'
            })

        # Check if the password is correct
        if not user.check_password(password):
            return render(request, 'loginaccount.html', {
                'form': AuthenticationForm(),
                'error': 'Incorrect password'
            })

        # Check if the user is an admin
        if user.is_admin:
            return render(request, 'loginaccount.html', {
                'form': AuthenticationForm(),
                'error': 'Admins cannot log in here'
            })

        # If all checks pass, log in the user
        login(request, user)
        return redirect('home')



# ✅ Normal User Logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  
def logoutaccount(request):
    logout(request)
    return redirect('home')

# Invite-Only Admin Signup
def admin_signup(request):
    if request.method == 'GET':
        return render(request, 'adminsignup.html', {'form': AdminSignupForm()})

    else:
        secret_key = request.POST.get("secret_key")  
        if secret_key != settings.ADMIN_SIGNUP_SECRET:  # 🚨 Validate secret key
            messages.error(request, "Invalid secret key. Access denied.")
            return redirect("admin_signup")

        form = AdminSignupForm(request.POST)
        if form.is_valid():
            admin_user = form.save(commit=False)
            admin_user.is_admin = True  # 🚨 Mark user as admin
            admin_user.save()

            messages.success(request, "Admin account created successfully!")
            return redirect("adminpanel")  
        else:
            return render(request, 'adminsignup.html', {'form': AdminSignupForm()})


#  Admin Login
def admin_login(request):
    if request.method == 'GET':
        return render(request, 'adminlogin.html', {'form': AuthenticationForm()})
    
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
    # Render login page with an error message if the username is not found
            return render(request, 'loginaccount.html', {
                'form': AuthenticationForm(),
            'error': 'Invalid username or password'  # Generic error message for security
        })
            # Check if the password is incorrect or the user is an admin
        if not user.check_password(password) or not user.is_admin:
            # Render login page with a generic error message
            return render(request, 'loginaccount.html', {
                'form': AuthenticationForm(),
                'error': 'Invalid username or password'})
        # Log in the user if all checks pass
        login(request, user)
        # Redirect to the home page after successful login
        return redirect('adminpanel')




from movie.models import MovieRequest

# ✅ Check if the user is an admin
def admin_required(login_url=None):
    return user_passes_test(
        lambda user: user.is_authenticated and user.is_admin, 
        login_url=login_url
    )




# ✅ Admin Panel View (Redirect to adminlogin)
@admin_required(login_url='adminlogin')  # Redirect to admin_login if not authenticated as admin
def adminpanel(request):
    # Fetch all movie requests
    movie_requests = MovieRequest.objects.all()  # Adjust the query as needed
    # Fetch all non-admin users
    non_admin_users = CustomUser.objects.filter(is_admin=False).order_by('date_joined')  # Ordered by joining date
    movies = Movie.objects.all()  # Fetch all movies
    
    # Pass the movie requests to the admin panel template
    return render(request,
                  'adminpanel.html',
                  {'movie_requests': movie_requests,
                'non_admin_users': non_admin_users, 'movies': movies})

def block_user(request, user_id):
    # Fetch the user and block them
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False  # Set status to blocked
    user.save()
    return redirect('adminpanel')  # Redirect back to admin panel

def allow_user(request, user_id):
    # Fetch the user and allow them
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True  # Set status to allowed
    user.save()
    return redirect('adminpanel')  # Redirect back to admin panel


###Create movie and save
from movie.models import Movie

def createmovie(request):
    if request.method == "POST":
        # Retrieve data from the form
        title = request.POST.get("title")
        producer = request.POST.get("producer")
        synopsis = request.POST.get("synopsis")
        tagline = request.POST.get("tagline")
        director = request.POST.get("director")
        writers = request.POST.get("writers")
        editor = request.POST.get("editor")
        music = request.POST.get("music")
        cinematography = request.POST.get("cinematography")
        keycast = request.POST.get("keycast")
        image = request.FILES.get("image")  # For image file

        # Save the movie to the database
        Movie.objects.create(
            title=title,
            producer=producer,
            synopsis=synopsis,
            tagline=tagline,
            director=director,
            writers=writers,
            editor=editor,
            music=music,
            cinematography=cinematography,
            keycast=keycast,
            image=image,
        )
        messages.success(request, "Movie created successfully!")
        return redirect("adminpanel")  # Redirect to the admin panel
    return render(request, "createmovie.html")  # Render movie creation form





from django.shortcuts import get_object_or_404, redirect
from movie.models import Movie

# Update Movie
def updatemovie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.producer = request.POST.get('producer')
        movie.save()
        return redirect('adminpanel')
    return render(request, 'updatemovie.html', {'movie': movie})

# Delete Movie
def deletemovie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect('adminpanel')

