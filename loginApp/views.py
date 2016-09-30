from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Users
from .models import UserProfile
from forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import redirect

def encode_url(str):
    return str.replace(' ', '_')

def decode_url(str):
    return str.replace('_', ' ')


def get_user_list(max_results=0, starts_with=''):
    u_list = []
    if starts_with:
        u_list = Users.objects.filter(name__startswith=starts_with)
    else:
        u_list = Users.objects.all()

    if max_results > 0:
        if (len(u_list) > max_results):
            u_list = u_list[:max_results]

    for u in u_list:
        u.url = encode_url(u.name)
    
    return u_list

def index(request):
    context = RequestContext(request)

    if request.session.get('last_visit'):
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)
        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
    else:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
    # Render and return the rendered response back to the user.
    return render_to_response('mtende/index.html', context)

def about(request):
    # Request the context.
    context = RequestContext(request)
    return render_to_response('mtende/about.html' , context)

def register(request):
    # Request the context.
    context = RequestContext(request)
    u_list = get_user_list()
    context_dict = {}
    context_dict['u_list'] = u_list
    # Boolean telling us whether registration was successful or not.
    # Initially False; presume it was a failure until its ok
    registered = False
    if request.method == 'POST':
        # Get raw form data - making use of both FormModels.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data
            user = user_form.save()

            #hashing the password with the set_password() method.
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            # Profile photo uploaded? If so, put it in the new UserProfile.
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
            profile.save()

            # Print registration was successful.
            registered = True

        # Invalid form(s) - just print error.
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict['user_form'] = user_form
    context_dict['profile_form']= profile_form
    context_dict['registered'] = registered
    return render_to_response(
        'mtende/register.html',
        context_dict,
        context)

def user_login(request):
    # Obtain our request's context.
    context = RequestContext(request)
    u_list = get_user_list()
    context_dict = {}
    context_dict['u_list'] = u_list
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Attempt to log the user in with the user input credentials.
        user = authenticate(username=username, password=password)
        if user is not None:
            # Check if the account is active.
            # If so, log the user in and redirect them to the profile.
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/mtende/profile')
            else:
                context_dict['disabled_account'] = True
                return render_to_response('mtende/login.html', context_dict, context)
        # Invalid login details.
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict['bad_details'] = True
            return render_to_response('mtende/login.html', context_dict, context)

    # Not a HTTP POST - most likely a HTTP GET. In this case then render the login form for the user.
    else:
        return render_to_response('mtende/login.html', context_dict, context)

# Only allow logged in users to logout - add the @login_required decorator!
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/mtende/')
@login_required
def profile(request):
    context = RequestContext(request)
    u_list = get_user_list()
    context_dict = {'cat_list': u_list}
    usr = User.objects.get(username=request.user)
    try:
        up = UserProfile.objects.get(user=usr)
    except:
        up = None
    context_dict['user'] = usr
    context_dict['userprofile'] = up
    return render_to_response('mtende/profile.html', context_dict, context)
