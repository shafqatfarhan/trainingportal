from django.http import HttpResponse,  HttpResponseRedirect
from django.shortcuts import render, redirect
from trainingportal.forms import LoginForm, ProfileForm, UserForm
from django.views.generic import View
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
import pdb

def home(request):
    data ={}
    return render(request, 'trainingportal/home.html', data)

def logout_view(request):
    logout(request)
    return redirect(home)

class LoginView(View):
    template_name = 'trainingportal/login.html'
    form_class = LoginForm
    #initial = {'username': 'BRO!!'}
    # success_url = '/thanks/'

    def get(self, request, *args, **kwargs):
        login_form = self.form_class()#self.form_class(initial=self.initial)
        return render(request, self.template_name, {'login_form': login_form})

    def post(self, request, *args, **kwargs):
        login_form = self.form_class(request.POST)
        if login_form.is_valid():
            try:
                user = authenticate(
                    request,
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password']
                )
                if user:
                    #request.session["remote_session_key"] = user.session_key
                    login(request, user)
                    response = redirect(home)
                    return response
                else:
                    return render(request, self.template_name, {
                        'login_form': login_form,
                        'login_failed': True
                    })

            except:
                return render(request, self.template_name, {'login_form': login_form})

        return render(request, self.template_name, {'login_form': login_form})


def register(request):
    ''' handles requests for registeration form and its submission '''
    data = {}
    user_form = None
    profile_form = None

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # user = UserRegistration(
            #     first_name=form.cleaned_data['firstname'],
            #     last_name=form.cleaned_data['lastname'],
            #     password=form.cleaned_data['password'],
            #     designation=form.cleaned_data['designation'],
            #     email_id=form.cleaned_data['email']
            # )
            user = User.objects.create_user(
                user_form.cleaned_data['username'],
                user_form.cleaned_data['email'],
                user_form.cleaned_data['password']
            )
            #user = user_form.save()
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.save()
            profile_form.save(user)
            try:
                login_user = authenticate(
                    request,
                    username=user_form.cleaned_data['username'],
                    password=user_form.cleaned_data['password']
                )
                if login_user:
                    login(request, login_user)
                return redirect(home)
            except:
                return redirect(home)
    data["user_form"] = user_form or UserForm()
    data["profile_form"] = profile_form or ProfileForm()

    return render(request, 'trainingportal/registration.html', data)

@login_required
def contact_us(request):
    return render(request, 'trainingportal/contact.html')
