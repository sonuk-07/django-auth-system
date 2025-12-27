from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomAuthenticationForm, CustomUserCreationForm

def register_view(request):
    """
    User Registration View
    
    Flow:
    1. GET request: Show empty form
    2. POST request: Process form data
    3. If valid: Create user, login, redirect
    4. If invalid: Show errors
    """


    #if user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            #save user to database
            user = form.save()

            #automatically login the user after registration
            login(request, user)

            #success message 
            messages.success(request, f'Welcome {user.first_name}! Your account has been created')

            #redirect to dashboard 
            return redirect('accounts:dashboard')
        else:
            #form has errors, they will display in template
            messages.error(request, 'Please correct the errors below')
    else:
        #get request: show empty form 
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form':form})

def login_view(request):
    """
    User Login View
    
    Flow:
    1. GET: Show login form
    2. POST: Validate credentials
    3. If valid: Login and redirect
    4. If invalid: Show error
    """

    # if user is already logged in

    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data =  request.POST)
        
        if form.is_valid():
            #get email and password from form
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            #authenticate user

            user = authenticate(request, username = email, password=password)

            if user is not None:
                #login the user 
                login(request, user)
                messages.success(request, f"welcome back, {user.first_name}")

                #redirect to 'next' parameter or dashboard
                next_url= request.GET.get('next', 'accounts:dashboard')
                return redirect(next_url)
            
        else:
            messages.error(request, 'Invalid email or password')

    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})


def logout_view(request):
    """
    Logout View
    
    Simple: Just logout and redirect
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def dashboard_view(request):
    """
    Dashboard - Only accessible to logged-in users
    
    @login_required decorator:
    - If user is not logged in, redirect to login page
    - Automatically adds 'next' parameter to return after login
    """
    return render(request, 'accounts/dashboard.html', {
        'user': request.user
    })